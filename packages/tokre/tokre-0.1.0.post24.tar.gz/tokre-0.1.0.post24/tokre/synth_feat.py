import torch
import torch.nn as nn
import torch.nn.functional as F

from .tokre_core.get_nfa import GroupData

import json

import datetime

import tokre
from typing import Optional
import ray
from textwrap import dedent

import random
from tqdm import tqdm

import torch.optim as optim
from schedulefree import AdamWScheduleFree
from tqdm import tqdm

class SynthFeat(nn.Module):
    def __init__(self, pattern, match_aggr: str='longest', prefix: Optional[str]=None, feat_tag: Optional[str]=None, lr=1e-2, disable_parallel=False):
        super().__init__()
        assert isinstance(pattern, str)
        assert match_aggr in ['longest', 'shortest']

        self.pattern = pattern
        self.matcher = tokre.compile(pattern, prefix=prefix)
        self.parse_tree_w_tok_ids = tokre.parse(self.pattern, tok_ids=True, suppress_info=True)
        self.parse_tree = tokre.parse(self.pattern, suppress_info=True)
        self.match_aggr=match_aggr
        self.feat_tag = feat_tag

        self.model = construct_synth_feat(self.parse_tree_w_tok_ids)

        self.var_explained=None
        self.prefix = prefix

        self.lr = lr
        self.optimizer = AdamWScheduleFree(self.parameters(), lr=self.lr, warmup_steps=100)

        self.disable_parallel=disable_parallel
    
    def forward(self, matches):
        return [self.model(match) for match in matches]
    
    def train(self, acts, tok_ids, n_actors=None, batch_size=1):
        train_data = list(self.get_train_data(tok_ids, acts, n_actors=n_actors))
        pbar = tqdm(range(0, len(train_data), batch_size))

        avg_loss = 0

        for i in pbar:
            batch = train_data[i:i+batch_size]
            batch_groups, batch_acts = zip(*batch)
            batch_acts = torch.stack(batch_acts)
            preds = self(batch_groups)
            preds = torch.stack(preds)
            loss = ((preds - batch_acts)**2).mean()
            loss.backward()
            self.optimizer.step()
            self.optimizer.zero_grad()

            if i % 200 == 0:
                avg_loss = avg_loss*0.9 + loss.item()*0.1

                pbar.set_description(f'Loss: {avg_loss:.2f}')


    def filter(self, tok_ids):
        return self.matcher.filter(tok_ids)

    def log(self, logfile: str):
        data = {
            'pattern': self.pattern,
            'match_aggr': self.match_aggr,
        }
        if self.feat_tag is not None:
            data['feat_tag'] = self.feat_tag
        if self.var_explained is not None:
            data['var_explained'] = self.var_explained
        if self.prefix is not None:
            data['prefix'] = self.prefix
    
        # Add a timestamp
        data['timestamp'] = datetime.datetime.now().isoformat()
        
        log_dir = tokre.get_workspace() / 'hypothesis_logs'
        log_dir.mkdir(parents=True, exist_ok=True)
        # Convert to JSON string
        json_data = json.dumps(data)

        with (log_dir / logfile).open('a') as f:
            f.write(json_data + '\n')
    
    def get_groups_per_doc(self, tok_ids, n_actors=None, batch_size=50, max_per_doc=False):
        if self.disable_parallel is True:
            groups_per_doc = [self.matcher.findall(doc_ids, return_group=True) for doc_ids in tqdm(tok_ids, desc='Loading tok_ids with matcher.findall')]
        else:
            groups_per_doc = self.matcher.findall_parallel(tok_ids, n_actors=n_actors, batch_size=batch_size, return_group=True)
        
        groups_per_doc = [filter_duplicate_matches(doc_groups, match_aggr=self.match_aggr) for doc_groups in groups_per_doc]
        if max_per_doc is not False:
            groups_per_doc = [random.sample(doc_groups, min(max_per_doc, len(doc_groups))) for doc_groups in groups_per_doc]
        return groups_per_doc

    def get_train_data(self, tok_ids, acts, n_actors=None, batch_size=50, max_per_doc=15):
        groups_per_doc = self.get_groups_per_doc(tok_ids, n_actors=n_actors, batch_size=batch_size, max_per_doc=max_per_doc)
        flattened_acts = []
        for doc_idx, doc_groups in enumerate(groups_per_doc):
            for group in doc_groups:
                try:
                    assert 0 <= doc_idx < acts.shape[0], f"Invalid doc_idx: {doc_idx}, acts shape: {acts.shape}"
                    assert 0 <= group.end - 1 < acts.shape[1], f"Invalid group.end - 1: {group.end - 1}, acts shape: {acts.shape}"
                    flattened_acts.append(acts[doc_idx, group.end-1])
                except Exception as e:
                    print(f"Error processing group: doc_idx={doc_idx}, group.end={group.end}")
                    print(f"acts shape: {acts.shape}")
                    print(f"Exception: {e}")
                    raise  # Re-raise the exception after printing debug information
        
        flattened_groups = [group for doc_groups in groups_per_doc for group in doc_groups]
        
        return zip(flattened_groups, flattened_acts)
    
    def get_acts(self, tok_ids, n_actors=None, match_batch_size=50, pred_batch_size=50):
        # groups_per_doc = self.matcher.findall_parallel(tok_ids, n_actors=n_actors, batch_size=match_batch_size, return_group=True)
        # groups_per_doc = [filter_duplicate_matches(doc_groups, match_aggr=self.match_aggr) for doc_groups in groups_per_doc]
        if n_actors is None:
            n_actors = tokre.tot_cpus()

        groups_per_doc = self.get_groups_per_doc(tok_ids, n_actors=n_actors, batch_size=match_batch_size)
        doc_group_pairs = [(doc_idx, group) for doc_idx, groups in enumerate(groups_per_doc) for group in groups]
        
        synth_acts = torch.zeros_like(tok_ids, dtype=torch.float)

        actors = [ParallelModel.remote(self.model) for _ in range(n_actors)]
        batched_pred_futures = [
                    actors[i%len(actors)].batched_pred.remote(
                            doc_group_pairs[i*pred_batch_size:(i+1)*pred_batch_size]
                        )
                        
                        for i in range((len(doc_group_pairs)//pred_batch_size)+1)
                ]
        batched_per_match_preds = ray.get(batched_pred_futures)
        per_match_preds = [pred for batch in batched_per_match_preds for pred in batch]
        
        for (doc_idx_1, group), (doc_idx_2, pred) in zip(doc_group_pairs, per_match_preds):
            assert doc_idx_1 == doc_idx_2
            synth_acts[doc_idx_1, group.end - 1] = pred
        return synth_acts

    def get_bin_acts(self, tok_ids, n_actors=None, match_batch_size=50):
        if n_actors is None:
            n_actors = tokre.tot_cpus()

        groups_per_doc = self.get_groups_per_doc(tok_ids, n_actors=n_actors, batch_size=match_batch_size)
        doc_group_pairs = [(doc_idx, group) for doc_idx, groups in enumerate(groups_per_doc) for group in groups]
        
        bin_acts = torch.zeros_like(tok_ids, dtype=torch.float)
        
        for doc_idx, group in doc_group_pairs:
            bin_acts[doc_idx, group.end - 1] = 1.
        return bin_acts

    

    # def __call__(self, tok_ids, **kwargs):
    #     return self.get_acts(tok_ids, **kwargs)


@ray.remote
class ParallelModel:
    def __init__(self, model):
        self.model = model
    def pred(self, group_data):
        with torch.no_grad():
            return self.model(group_data)
    def batched_pred(self, doc_group_pairs):
        with torch.no_grad():
            return [(doc_idx, self.model(group_data).item()) for (doc_idx, group_data) in doc_group_pairs]
    


class Atom(nn.Module):
    def __init__(self, name, idx, regex_type):
        super().__init__()
        self.name = name
        self.idx = idx
        self.regex_type = regex_type
        self.device = torch.device('cpu')
        self.dtype = torch.float32
    
    def to(self, dtype=None, device=None):
        if dtype is not None:
            self.dtype = dtype
        if device is not None:
            self.device = device
        if device is None and dtype is None:
            assert False, 'please specify at least one argument of `device` or `dtype`'

    
    def forward(self, group_data):
        assert isinstance(group_data, GroupData)
        assert group_data.name == self.name, f'{group_data.name} and {self.name}'
        assert group_data.idx == self.idx, f'{group_data.idx} and {self.idx}'

        return torch.tensor(1., device=self.device, dtype=self.dtype)


class LearnableAtom(nn.Module):
    def __init__(self, name, idx, regex_type):
        '''
        Alternative to Atom class when the entire parse_tree is just a single atom
        Includes a learnable bias
        '''
        super().__init__()
        self.name = name
        self.idx = idx
        self.regex_type = regex_type

        self.bias = nn.Parameter(torch.ones(1)[0])
    
    def forward(self, group_data):
        assert isinstance(group_data, GroupData)
        assert group_data.name == self.name, f'{group_data.name} and {self.name}'
        assert group_data.idx == self.idx, f'{group_data.idx} and {self.idx}'

        return self.bias

class AbsPos(nn.Module):
    def __init__(self, name, idx):
        '''
        Use [pos] inside your tokre script. Injects absolute position into the synthetic feat at the location of [pos]
        '''
        super().__init__()
        self.name = name
        self.idx = idx
        self.pos_bias = nn.Parameter(torch.ones(128+1)/129)
    
    def forward(self, group_data):
        assert isinstance(group_data, GroupData)
        assert group_data.name == self.name, f'{group_data.name} and {self.name}'
        assert group_data.idx == self.idx, f'{group_data.idx} and {self.idx}'

        assert group_data.start is not None and group_data.end is not None
        assert len(group_data.children) == 0

        return self.pos_bias[group_data.start]
    
    def __repr__(self):
        return dedent('''
            AbsPos(
                pos_bias: (129,)
            )
            ''')



class OrPhrase(nn.Module):
    def __init__(self, name, idx, children):
        super().__init__()
        self.name = name
        self.idx = idx
        self._children = nn.ModuleList(children)

        n_options = len(children)
        self.weight = nn.Parameter(torch.ones(n_options,))
        self.bias = nn.Parameter(torch.zeros(n_options,))
    def forward(self, group_data):
        assert isinstance(group_data, GroupData)
        assert group_data.name == self.name, f'{group_data.name} and {self.name}'
        assert group_data.idx == self.idx, f'{group_data.idx} and {self.idx}'

        assert len(group_data.children) == 1,\
            'or_phrase group_data should have only one child because only one child is selected per or_phrase'
        
        child_group_data = group_data.children[0]
        child_idx = child_group_data.idx
        child = self._children[child_idx]
        
        return self.weight[child_idx]*child(child_group_data) + self.bias[child_idx]

    def __getitem__(self, idx):
        return self._children[idx]

class Repeat(nn.Module):
    def __init__(self, name, idx, max_repeat, child):
        super().__init__()
        self.name = name
        self.idx = idx
        self.max_repeat = max_repeat
        self.child = child

        if self.max_repeat != float('inf'):
            length = min(max_repeat, 128)
            self.weight = nn.Parameter(torch.ones(length)/(length**1.4))

        # first element is no repeats
        self.bias = nn.Parameter(torch.zeros(min(max_repeat+1, 128+1)))
        self.global_bias = nn.Parameter(torch.ones(1,)[0])
    
    def forward(self, group_data):
        assert isinstance(group_data, GroupData)
        assert group_data.name == self.name, f'{group_data.name} and {self.name}'
        assert group_data.idx == self.idx, f'{group_data.idx} and {self.idx}'

        if self.max_repeat == float('inf'):
            # ignore the values and just include the global bias
            return self.global_bias#self.bias[len(group_data.children)]
        else:
            if len(group_data.children) == 0:
                return self.bias[-1] + self.global_bias
            else:
                child_values = torch.stack([self.child(child_data) for child_data in group_data.children])
                return torch.dot(child_values, self.weight[:len(child_values)]) + torch.sum(self.bias[:len(group_data.children)], dim=0) + self.global_bias


class Phrase(nn.Module):
    def __init__(self, name, idx, children):
        super().__init__()
        assert len(children) >= 1, 'phrases should have at least one child'

        self.name = name
        self.idx = idx
        
        self._children = nn.ModuleList(children)

        length = len(children)
        self.weight = nn.Parameter(torch.ones(length)/length)
        self.bias = nn.Parameter(torch.zeros(1)[0])

        self.bilinear = nn.Parameter(torch.randn(length, length).abs()/length**2)
    
    def forward(self, group_data):
        assert group_data.name == self.name, f'{group_data.name} and {self.name}'
        assert group_data.idx == self.idx, f'{group_data.idx} and {self.idx}'
        assert len(group_data.children) == len(self._children)
        

        child_vals = torch.stack([child(child_data) for child, child_data in zip(self._children, group_data.children)])
        dot = torch.dot(self.weight, child_vals)
        mix = torch.einsum('ij,i,j->', self.bilinear, child_vals, child_vals)

        return mix + dot + self.bias

    def __getitem__(self, child_idx):
        return self._children[child_idx]



class IdentityPassthrough(nn.Module):
    def __init__(self, name, idx, child):
        super().__init__()
        self.name = name
        self.idx = idx

        self.child = child
    def forward(self, group_data):
        assert group_data.name == self.name, f'{group_data.name} and {self.name}'
        assert group_data.idx == self.idx, f'{group_data.idx} and {self.idx}'
        assert len(group_data.children) == 1

        return self.child(group_data.children[0])


def construct_synth_feat(parse_tree, root: bool=True, learnable_atoms: bool=False):
    # parse_tree: parse tree for the synth feat.
    # root: True if parse_tree is a root node. If True, make sure log_hypothesis is not None and if the tree is an atom that it's learnable.
    # log_hypothesis: optional Hypothesis. Required if provided tree node is specified as root in the args
    # learnable_atoms: Forces top-level atoms to be learnable, even if root is False.
    #   Not really intended for user use.
    #   Used only for IdentityPassthrough because it doesn't have any parameters.
    #   EG if the tree is phrase(atom, phrase(...)), that atom won't be converted to LearnableAtom.
    #   But if the tree is only a single atom, this fn will return LearnableAtom

    if parse_tree.data in {'toks', 'wildcard', 'tokenset', 'var_ref'}:
        # parse_tree is an atom
        if learnable_atoms is True or root is True:
            model = LearnableAtom(name=parse_tree.name, idx=parse_tree.idx, regex_type=parse_tree.data)
        elif learnable_atoms is False and root is False:
            model = Atom(name=parse_tree.name, idx=parse_tree.idx, regex_type=parse_tree.data)
        else:
            assert False, 'This if/else branch should not be reachable.'

    elif parse_tree.data == 'or_phrase':
        model = OrPhrase(name=parse_tree.name, idx=parse_tree.idx, children=[construct_synth_feat(child, root=False) for child in parse_tree.children])
    elif parse_tree.data == 'repeat':
        child, min_repeat, max_repeat = parse_tree.children
        model = Repeat(name=parse_tree.name, idx=parse_tree.idx, max_repeat=max_repeat, child=construct_synth_feat(child, root=False))
    elif parse_tree.data == 'phrase':
        model = Phrase(name=parse_tree.name, idx=parse_tree.idx, children=[construct_synth_feat(child, root=False) for child in parse_tree.children])
    elif parse_tree.data == 'repeated_definition':
        ref_name, child_tree, start, end, direction = parse_tree.children
        assert start is None and end is None and direction == 1, 'unimplemented'
        model = IdentityPassthrough(name=parse_tree.name, idx=parse_tree.idx, child=construct_synth_feat(child_tree, root=False, learnable_atoms=root))
    elif parse_tree.data == 'named_capture':
        ref_name, child_tree = parse_tree.children
        model = IdentityPassthrough(name=parse_tree.name, idx=parse_tree.idx, child=construct_synth_feat(child_tree, root=False, learnable_atoms=root))

    elif parse_tree.data == 'pos':
        assert len(parse_tree.children) == 0
        model = AbsPos(name=parse_tree.name, idx=parse_tree.idx)
    else:
        assert False, f'parse_tree.data is an invalid value: {parse_tree.data}'
    
    model.parse_tree = parse_tree
    return model

def filter_duplicate_matches(matches, match_aggr='longest'):
    assert match_aggr in {'longest', 'shortest'}
    matches_by_idx = {}

    for match in matches:
        if match.end in matches_by_idx:
            logged_match = matches_by_idx[match.end]
            # this match is longer
            if len(match) > len(logged_match) and match_aggr == 'longest':
                matches_by_idx[match.end] = match
            if len(match) < len(logged_match) and match_aggr == 'shortest':
                matches_by_idx[match.end] = match
        else:
            matches_by_idx[match.end] = match

    matches = list(matches_by_idx.values())

    return matches