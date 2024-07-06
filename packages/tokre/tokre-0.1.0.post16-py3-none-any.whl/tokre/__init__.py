import os

_tokenizer = None
_workspace = None
_openai_api_key = os.environ.get('OPENAI_API_KEY', None)

import ray
ray.init(ignore_reinit_error=True)

def tot_cpus():
    return int(ray.available_resources()['CPU'])

from .tokre_core.get_nfa import check, parse_tree_to_nfa
from .tokre_core.parse import parse, recursively_add_definitions, escape
from .tokre_core.faster_matcher import Pattern, compile
from .synth_feat import SynthFeat
from .setup_workspace import setup
from .utils import hash_tokenizer

from .tok_labelling.create_tok_label import create_tok_label


def encode(text):
    global _tokenizer
    if _tokenizer is None:
        raise ValueError("Tokenizer not initialized. Call `tokre.setup()` first.")
    return _tokenizer.encode(text)
enc = encode

def decode(tokens):
    global _tokenizer
    if _tokenizer is None:
        raise ValueError("Tokenizer not initialized. Call `tokre.setup()` first.")
    return _tokenizer.decode(tokens)
dec = decode

def tok_strs(s):
    return [dec(tok_id) for tok_id in enc(s)]


def get_workspace():
    global _workspace
    if _workspace is None:
        raise ValueError("Workspace not initialized. Call `tokre.setup()` with `workspace` specified first.")
    return _workspace

