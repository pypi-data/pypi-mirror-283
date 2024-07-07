import unicodedata
from functools import lru_cache

import torch
import numpy as np
import regex as re

import tokre
from .parse import parse, special_tokre_chars
from .get_nfa import parse_tree_to_nfa, check

from typing import List, Union

from tqdm import tqdm

import ray


def is_valid_char(code_point):
    try:
        char = chr(code_point)
        # If the character is printable, has a name, and is not a special char, it is valid.
        if char.isprintable() and unicodedata.name(char, None) and char not in special_tokre_chars:
            return True
    except ValueError:
        pass
    return False

@lru_cache
def valid_unicode_characters():
    valid_unicode_characters = []
    for code_point in range(0x110000):  # Unicode code points range from 0 to 0x10FFFF
        if is_valid_char(code_point):
            valid_unicode_characters.append(chr(code_point))
    return valid_unicode_characters

VALID_CHARS = np.array(valid_unicode_characters())

def tok_ids_to_pyregex_str(tok_ids):
    
    if isinstance(tok_ids, np.ndarray) or isinstance(tok_ids, list):
        tok_ids = torch.tensor(tok_ids)
    elif isinstance(tok_ids, torch.Tensor):
        tok_ids = tok_ids.cpu()
    print('tok_ids', tok_ids.shape)
    print('type tok_ids', type(tok_ids))
    print('tok_ids[0]', tok_ids[0])
    return ''.join(VALID_CHARS[tok_ids])

def _tree_to_pyregex_str(tree, root=True):
    if tree.data == 'or_phrase':
        pat_str = '('+'|'.join([_tree_to_pyregex_str(ch, root=False) for ch in tree.children])+')'
    elif tree.data == 'toks':
        pat_str = tok_ids_to_pyregex_str(tree.children[0])
    elif tree.data == 'repeat':
        min, max = tree.children[-2], tree.children[-1]
        children = [_tree_to_pyregex_str(child, root=False) for child in tree.children[:-2]]
        if str(max) == 'inf':
            max = 128
        pat_str = '('+''.join(children)+r'){'+str(min)+r','+str(max)+r'}'
    elif tree.data == 'phrase':
        pat_str = ''.join([_tree_to_pyregex_str(ch, root=False) for ch in tree.children])
    elif tree.data == 'wildcard':
        # pat_str = '.'
        pat_str='[^'+VALID_CHARS[-4]+']' #not [BEGIN]
    elif tree.data == 'tokenset':
        assert len(tree.children) == 2
        tokenset, negation = tree.children

        tokenset_str = tok_ids_to_pyregex_str(tokenset)

        if negation == True:
            pat_str = '[^'+tokenset_str+']'
        else:
            pat_str = '['+tokenset_str+']'
    elif tree.data == 'var_ref':
        var_name, start, end, direction = tree.children
        assert direction == 1, 'backwards var_ref is unimplemented'
        assert start is None, 'unimplemented'
        assert end is None, 'unimplemented'
        pat_str = f'(?P={var_name})'
    elif tree.data == 'named_capture':
        var_name, child_tree = tree.children
        pat_str = f'(?P<{var_name}>{_tree_to_pyregex_str(child_tree)})'

    elif tree.data == 'look_and_return':
        if tree.children[0].data == 'backwards' and tree.children[0].children[0].data == 'reversed':
            # lookbehind
            pat_str = _tree_to_pyregex_str(tree.children[0].children[0].children[0], root=False)
            pat_str = f'(?<={pat_str})'
        if tree.children[0].data != 'backwards':
            # lookahead
            pat_str = f'(?={_tree_to_pyregex_str(children[0], root=False)})'
    elif tree.data == 'repeated_definition':
        ref_name, child_tree, start, end, direction = tree.children
        assert direction == 1, 'backwards repeated_definition is unimplemented'
        assert start is None, 'unimplemented'
        assert end is None, 'unimplemented'
        pat_str = _tree_to_pyregex_str(child_tree, root=False)
    elif tree.data == 'pos':
        pat_str = ''
    else:
        assert False, tree

    if root is True:
        return '('+pat_str+')'
    else:
        return pat_str

from .get_nfa import GroupData, Match

def _shift_group_indices_forward(group_data, shift_amt):
    '''
    Recursively shifts indices of group data forward
    '''
    assert isinstance(group_data, GroupData)
    assert isinstance(shift_amt, int)
    
    assert isinstance(group_data.start, int)
    assert isinstance(group_data.end, int)

    group_data.start += shift_amt
    group_data.end += shift_amt

    for child in group_data.children:
        _shift_group_indices_forward(child, shift_amt)
    
@ray.remote
class PatternActor:
    def __init__(self, pattern):
        assert isinstance(pattern, Pattern)
        self.pattern = pattern
    def findall(self, doc_ids, return_group=True):
        return self.pattern.findall(doc_ids, return_group=return_group)
    def batched_findall(self, docs, return_group=True):
        return [self.findall(doc_ids, return_group=return_group) for doc_ids in docs]


class Pattern:
    '''
    Faster matcher for a tokre pattern. Filters sequences of tokens with the unofficial python regex library
    and then passes them into tokre to get the final matches.
    '''
    def __init__(self, pattern, prefix=None):
        self.pattern = pattern

        self.parse_tree = parse(pattern, tok_ids=True)
        self.tokre_nfa = parse_tree_to_nfa(self.parse_tree)

        self.prefix = prefix
        
        self.pyregex_prefix_str = '' if self.prefix is None else '(?<=(?:'+_tree_to_pyregex_str(parse(self.prefix, tok_ids=True))+')(?P=tokre_match))'
        self.pyregex_str = _tree_to_pyregex_str(self.parse_tree)

        self.pyregex_pattern = re.compile(f'(?P<tokre_match>{self.pyregex_str}){self.pyregex_prefix_str}')

        # Will be set if findall_parallel is called
        self.actors = None # [PatternActor.remote(self) for _ in range(tokre.tot_cpus())]

    def findall(self, toks, debug=False, return_group=False):
        if isinstance(toks, torch.Tensor) or isinstance(toks, np.ndarray):
            toks = toks.tolist()
        assert isinstance(toks, list)
        assert len(toks) >= 1
        if isinstance(toks[0], str):
            toks = [tokre.encode(tok_str)[0] for tok_str in toks]
        pyregex_doc = tok_ids_to_pyregex_str(toks)
        pyregex_matches = list(re.finditer(self.pyregex_pattern, pyregex_doc, overlapped=True))
        pyregex_spans = [(m.start('tokre_match'), m.end('tokre_match')) for m in pyregex_matches]

        contiguous_tok_spans = []

        if pyregex_spans:
            cur_start, cur_end = pyregex_spans[0][0], pyregex_spans[0][1]
            for span in pyregex_spans[1:]:
                if span[0] < span[1]:
                    cur_end = max(span[1], cur_end)
                else:
                    contiguous_tok_spans.append((cur_start, cur_end))
                    cur_start, cur_end = span[0], span[1]
            contiguous_tok_spans.append((cur_start, cur_end))
        
        tokre_matches = []
        for tok_span in contiguous_tok_spans:
            span_tokre_matches = check(toks[tok_span[0]:tok_span[1]], self.tokre_nfa, return_group=return_group)
            
            for match in span_tokre_matches:
                if debug:
                    print()
                if return_group is False:
                    match.start += tok_span[0]
                    match.end += tok_span[0]
                    _shift_group_indices_forward(match.group_data, shift_amt=tok_span[0])
                else:
                    _shift_group_indices_forward(match, shift_amt=tok_span[0])
            tokre_matches.extend(span_tokre_matches)

        return tokre_matches

    def findall_parallel(self, tok_ids, n_actors=None, batch_size=50, return_group=True):
        n_actors = tokre.tot_cpus() if n_actors is None else n_actors

        if self.actors is None or (isinstance(self.actors, list) and len(self.actors) < n_actors):
            self.actors = [PatternActor.remote(self) for _ in range(n_actors)]
        
        # futures = {i: self.actors[i % n_actors].findall.remote(doc_ids) for i, doc_ids in enumerate(tok_ids)}
        futures = {
                    i: self.actors[i%n_actors].batched_findall.remote(tok_ids[i*batch_size:(i+1)*batch_size], return_group=return_group)
                        for i in range(0, tok_ids.shape[0]//batch_size + 1)
                  }

        results = [None] * ((tok_ids.shape[0] // batch_size) + 1)

        with tqdm(total=len(futures), desc="Collecting matches") as pbar:
            while futures:
                done, _ = ray.wait(list(futures.values()))
                for future in done:
                    idx = next(key for key, value in futures.items() if value == future)
                    results[idx] = ray.get(future)
                    del futures[idx]
                    pbar.update(1)
        
        results = [doc_matches for batch in results for doc_matches in batch]
        return results


    def is_active(self, doc_ids):
        pyregex_doc = tok_ids_to_pyregex_str(doc_ids)
        match = re.search(self.pyregex_pattern, pyregex_doc)
        return bool(match)
    
    def active_mask(self, tok_ids):
        return [self.is_active(doc_ids) for doc_ids in tok_ids]


    def filter(self, tok_ids):
        mask = self.active_mask(tok_ids)
        return tok_ids[np.array(mask)]
    

    def tokre_acts(self, tok_ids: Union[List[int], np.ndarray]):
        if isinstance(tok_ids[0], int):
            # we assume docs is a 1d iterable of ints
            assert all([isinstance(tok_id, int) for tok_id in tok_ids])
            # call tokre_acts batched then undo batching and return
            return self.tokre_acts(np.array([tok_ids]))[0]
        
        final_tokre_acts = np.zeros(np.array(tok_ids).shape, dtype=int)

        for doc_idx, doc_ids in enumerate(tok_ids):
            tokre_matches = self.findall(doc_ids)
            for match in tokre_matches:
                final_tokre_acts[doc_idx, match.end-1] = 1
        
        return final_tokre_acts

    def __call__(self, tok_ids):
        return self.tokre_acts(tok_ids)

def compile(pattern, prefix=None):
    return Pattern(pattern=pattern, prefix=prefix)