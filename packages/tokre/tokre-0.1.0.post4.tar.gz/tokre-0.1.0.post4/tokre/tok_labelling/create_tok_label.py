import itertools
import json
import os
import random
from functools import lru_cache
from typing import Optional

import numpy as np

import tokre
from tokre.tok_labelling.query_openai import query_openai
from tokre.utils import (assert_snake_case, format_nest, get_vocab_size,
                         threaded_map)


@lru_cache()
def get_all_toks():
    tok_ids = np.arange(get_vocab_size(tokre._tokenizer))
    toks = [tokre.decode([tok_id]) for tok_id in tok_ids]
    return toks

def extract_stripped_toks(toks):
    return list(set([t.strip() for t in toks]))

def extract_space_toks(toks):
    # returns tokens that start with a space
    toks = [t for t in toks if t.strip() != '']
    return list(set([t for t in toks if t[0] == ' ']))

def extract_no_space_toks(toks):
    toks = [t for t in toks if t.strip() != '']
    return list(set([t for t in toks if t[0] != ' '])) 

def extract_capitalized_toks(toks):
    # returns tokens that are capitalized
    toks = [t for t in toks if t.strip() != '']
    return list(set([t for t in toks if t.strip()[0].isupper()]))

def extract_not_capitalized_toks(toks):
    # returns tokens that are not capitalized
    toks = [t for t in toks if t.strip() != '']
    return list(set([t for t in toks if t.strip()[0].islower()]))


prompt_template = '''Given the list of strings below, identify which strings match the following description:
{description}
To log the strings that match the description, call log_{label}_strings([...identified strings]). Copy strings exactly as they appear.

Here is the list of strings for you to process: {batch}'''

functions_template = [
    {
    "name": "log_{label}_strings",
    "description": "",
    "parameters": {
        "type": "object",
        "properties": {
            "identified_{label}_strings": {
                "type": "array",
                "description": "{description}",
                "items": {
                    "type": "string",
                }
            },
        },
    },
    "required": ["log_{label}_strings"],
    },
]


def extract_toks_from_batch(tok_batch: list[str], label: str, description: str, model='gpt-4o'):
    out = query_openai(
                messages=[{
                    'role': 'system',
                    'content': prompt_template.format(label=label, description=description, batch=tok_batch),
                }],
                model=model,
                functions=format_nest(functions_template, label=label, description=description),
                function_call={'name': f"log_{label}_strings"},
                temperature=0.7)

    try:
        fn_call_args_str = out.function_call.arguments
    except Exception as e:
        print(f'Exception: {e}')
        print('No function call found.')
    try:
        fn_call_args = json.loads(
           fn_call_args_str
        )
    except Exception as e:
        print(f'Exception: {e}')
        print(f'Failed to load with json: {fn_call_args_str}')
        return []
    if f'identified_{label}_strings' not in fn_call_args:
        print(f'`identified_{label}_strings` not found in fn_call_args: {fn_call_args}')
        return []
    candidate_toks = fn_call_args[f"identified_{label}_strings"]

    return [tok for tok in candidate_toks if tok in tok_batch]



def create_tok_label(label, desc, batch_size=50, model='gpt-4o', filters:Optional[list[str]]=None, stripped_labelling=True, n_passes: int=1, inclusion_threshold: int=1):
    '''
    label: str = snake_case short representation of the label
    desc: str = description of tokens that fit the label.
    filters: list[str] = list of flags used to filter tokens before labelling
        Available filters are ['space', 'no_space', 'capitalized', 'no_capitalized']
    stripped_labelling: bool = whether to strip tokens before feeding to the language model.
    n_passes: int = number of times the LM sees the token.
    inclusion_threshold: int = the number of times the LM thinks the token fits the description before it's included in the final set (see n_passes argument to this fn)
    
    EG
    create_tok_label(label='past_tense_verb', desc='Strings that are past-tense verbs.')
    create_tok_label(label='adjective', desc='Strings that are adjectives.')
    '''
    assert_snake_case(label)

    assert 1 <= inclusion_threshold <= n_passes

    filters = [] if filters is None else filters

    if len(filters) > 0:
        assert isinstance(filters, list)
        assert all([isinstance(k, str) for k in filters])
        assert all([flag in {'space', 'no_space', 'capitalized', 'no_capitalized'} for flag in filters])
        assert not ('space' in filters and 'no_space' in filters), 'mutually exclusive filters options'
        assert not ('capitalized' in filters and 'no_capitalized' in filters), 'mutually exclusive filters options'
        assert not (stripped_labelling is True and 'no_space' in filters),\
                'stripped_labelling wouldn\'t change fn behavior here, so if you\'d like no_space please set stripped_labelling to False. This assertion here is to reduce complexity.'
    
    ws_path = tokre.get_workspace()
    # ls = os.listdir(ws_path)
    # if label+'.json' in ls:
    #     with open(f'{ws_path}/{label}.json', 'r') as f:
    #         existing_desc = json.load(f).get('create_tok_label_kwargs', {}).get('desc', 'No description found.')
    #     inp = input(f'{label}.json already found in {ws_path}/ with tok label description:\n{existing_desc}\nOverwrite this file?')
    #     if inp.strip().lower() not in {'y', 'yes'}:
    #         print('Aborting tok labelling.')
    #         return
    #     else:
    #         pass

    all_toks = get_all_toks()
    valid_toks = get_all_toks()

    if 'space' in filters:
        valid_toks = extract_space_toks(valid_toks)
    if 'no_space' in filters:
        valid_toks = extract_no_space_toks(valid_toks)
    if 'capitalized' in filters:
        valid_toks = extract_capitalized_toks(valid_toks)
    if 'no_capitalized' in filters:
        valid_toks = extract_not_capitalized_toks(valid_toks)

    if stripped_labelling is True:
        valid_toks = extract_stripped_toks(valid_toks)

    counts = np.zeros(len(all_toks), dtype=int)

    for pass_idx in range(n_passes):
        random.shuffle(valid_toks)
        batches = [valid_toks[i:i+batch_size] for i in range(0, len(valid_toks), batch_size)]
        pbar_desc = f'{label}, pass {pass_idx+1}/{n_passes}'
        identified_strings = list(itertools.chain.from_iterable(threaded_map(extract_toks_from_batch, batches, pbar_desc=pbar_desc, n_threads=10, kwargs={'label': label, 'description': desc, 'model': model})))
        for string in identified_strings:
            if stripped_labelling is True:
                if 'no_space' not in filters and ' '+string in all_toks:
                    counts[all_toks.index(' '+string)] += 1

                if 'space' not in filters and string in all_toks:
                    counts[all_toks.index(string)] += 1
            else:
                if string in all_toks:
                    counts[all_toks.index(string)] += 1

    identified_tok_ids = np.nonzero((counts >= inclusion_threshold).astype(int))[0]
    identified_toks = np.array(all_toks)[identified_tok_ids].tolist()
    
    fname = ws_path / f'{label}.json'
    
    result = {
        'pattern': r'{'+'|'.join(identified_toks)+r'}',
        'create_tok_label_kwargs': {
            'label': label,
            'desc': desc,
            'filters': filters,
            'stripped_labelling': stripped_labelling,
            'n_passes': n_passes,
            'inclusion_threshold': inclusion_threshold,
        },
        'tok_label_toks': identified_toks,
    }

    with open(fname, 'w') as f:
        json.dump(result, f, indent=2)

    return identified_toks


    

