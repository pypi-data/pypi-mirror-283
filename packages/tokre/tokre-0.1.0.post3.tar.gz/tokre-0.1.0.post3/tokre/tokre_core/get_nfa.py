# type State = str
# type char = str (of length 1)
# type Transitions = dict[char, set[State]]
# type NFA = dict[State, Transitions]

import os
import random
import string
from copy import deepcopy
from dataclasses import dataclass
from typing import List, Optional

from tokre.tokre_core.parse import *

os.environ["TOKENIZERS_PARALLELISM"] = "false"


START_STATE = "START_STATE"
EXIT_STATE = "EXIT_STATE"
WILDCARD = "WILDCARD"

REPLAY_RECORDING_PREFIX = "REPLAY_RECORDING"
START_RECORDING_PREFIX = "START_RECORDING"
END_RECORDING_PREFIX = "END_RECORDING"

START_LOOKBEHIND_PREFIX = "START_LOOKBEHIND"
END_LOOKBEHIND_PREFIX = "END_LOOKBEHIND"

START_LOOKAHEAD_PREFIX = "START_LOOKAHEAD"
END_LOOKAHEAD_PREFIX = "END_LOOKAHEAD"

ASSERT_BEGIN_PREFIX = "ASSERT_BEGIN"
ASSERT_END_PREFIX = "ASSERT_END"

START_GROUP_DATA = "START_GROUP_DATA"
END_GROUP_DATA = "END_GROUP_DATA"

all_prefixes = [
    START_STATE,
    EXIT_STATE,
    REPLAY_RECORDING_PREFIX,
    START_RECORDING_PREFIX,
    END_RECORDING_PREFIX,
    START_LOOKBEHIND_PREFIX,
    END_LOOKBEHIND_PREFIX,
    START_LOOKAHEAD_PREFIX,
    END_LOOKAHEAD_PREFIX,
    ASSERT_BEGIN_PREFIX,
    ASSERT_END_PREFIX,
    START_GROUP_DATA,
    END_GROUP_DATA,
]


@dataclass
class GroupData:
    name: str
    idx: int
    id: Optional[str]
    start: Optional[int] = None
    end: Optional[int] = None
    children: List["GroupData"] = None

    def __len__(self):
        return self.end - self.start


@dataclass
class Match:
    match_str: Optional[str]
    start: int
    end: int
    group_data: Optional[GroupData]

    def __len__(self):
        return self.end - self.start


def randstr(N=7):
    return "".join(
        random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase)
        for _ in range(N)
    )


from typing import Union


def rename_state(nfa, state, new_state: Optional[str] = None):
    """
    statefully renames a state in the nfa
    if new_state is not provided, generates a random string for the new_state


    [various nfa states] -- state -- [various nfa states]
        is statefully transformed in the nfa to
    [various  nfa states] -- new_state -- [various nfa states]

    returns new_state
    """

    new_state = randstr() if new_state is None else new_state

    if state in nfa:
        nfa[new_state] = deepcopy(nfa[state])
        del nfa[state]

    for cur_state, transitions in nfa.items():
        for obs, dests in transitions.items():
            assert isinstance(dests, set), dests
            if state in dests:
                nfa[cur_state][obs] = set(dests).union({new_state}) - {state}

    return new_state


def add_eps_transition(nfa, start, end):
    """
    statefully adds this transition to the nfa:
        `start` --|eps|--> `end`
    """
    if start not in nfa:
        nfa[start] = {}
    if "" not in nfa[start]:
        nfa[start][""] = set()
    nfa[start][""].add(end)


def add_transition(nfa, start, obs, end):
    """
    statefully adds this transition to the nfa:
        `start` --|obs|--> `end`
    """
    if start not in nfa:
        nfa[start] = {}
    if obs not in nfa[start]:
        nfa[start][obs] = set()
    nfa[start][obs].add(end)


def rename_bounds(nfa, start=None, exit=None):
    start, exit = rename_state(nfa, START_STATE, start), rename_state(
        nfa, EXIT_STATE, exit
    )
    return start, exit


def add_outer_layer(nfa, renamed_start=None, renamed_exit=None):
    """
    statefully replaces START with renamed_start, EXIT with renamed_exit in nfa
    if renamed_start, renamed_exit arguments are not provided in input, generates random strings for them.

        START --[start edges]-- [nfa body] --[exit edges]-- EXIT
    is mutated/statefully transformed to
        START --|eps|-->
            renamed_start --[start edges]-- [nfa body] --[exit edges]-- renamed_exit
        --|eps|--> EXIT

    returns renamed_start, renamed_exit
    """

    # also randomly generates renamed_start, renamed_exit if they're None
    renamed_start, renamed_exit = rename_bounds(nfa, renamed_start, renamed_exit)

    add_eps_transition(nfa, START_STATE, renamed_start)
    add_eps_transition(nfa, renamed_exit, EXIT_STATE)

    return renamed_start, renamed_exit


def extend_end(nfa, new_exit):
    """
    [nfa states] --[exit edges]--> EXIT
        is statefully transformed to
    [nfa states] --[exit edges]--> new_exit --|eps|--> EXIT
    """
    rename_state(nfa, EXIT_STATE, new_exit)
    add_eps_transition(nfa, new_exit, EXIT_STATE)
    return new_exit


def extend_start(nfa, new_start):
    """
    START --[start edges]--> [nfa states]
        is statefully transformed to
    START --|eps|--> new_start --[start edges]--> [nfa states]
    """
    rename_state(nfa, START_STATE, new_start)
    add_eps_transition(nfa, START_STATE, new_start)
    return new_start


def add_group_handling(tree, nfa):
    """
    statefully transforms nfa:
        - START replaced with group_start(tree.name, tree.idx, id)
        - EXIT replaced with group_exit(tree.name, tree.idx, id)
        - then entire nfa is wrapped with new START/EXIT


    START --[start edges]--> [nfa states] --[exit edges]--> EXIT

        is transformed to:

    START --|eps|-->
      group_start(..) --[start edges]--> [nfa states] --[exit edges]--> group_exit(..)
    --|eps|--> EXIT
    """

    assert hasattr(tree, "name")
    assert hasattr(tree, "idx")

    id = randstr()
    new_start = f"{START_GROUP_DATA}:{tree.name}:{tree.idx}:{id}"
    new_exit = f"{END_GROUP_DATA}:{tree.name}:{tree.idx}:{id}"
    add_outer_layer(nfa, renamed_start=new_start, renamed_exit=new_exit)


def concat(nfa1, nfa2):
    """
    nfa1
        START_1 --[nfa1 body]--> EXIT_1
    nfa2
        START_2 --[nfa2 body]--> EXIT_2

    returns
        START_1 --[nfa1 body]--> renamed_exit_1 --|eps| --> renamed_start_2 --[nfa2 body] --> EXIT_2
    """
    nfa1, nfa2 = deepcopy(nfa1), deepcopy(nfa2)

    renamed_exit_1 = rename_state(nfa1, EXIT_STATE)
    renamed_start_2 = rename_state(nfa2, START_STATE)

    add_eps_transition(nfa1, renamed_exit_1, renamed_start_2)

    nfa1.update(nfa2)

    return nfa1


def blank_nfa():
    # START_STATE --|eps|--> EXIT_STATE
    return {START_STATE: {"": {EXIT_STATE}}}


TOKENSET_PREFIX = "TOKENSET_STATE"
TOKENSET_KEY = "TOKENSET_KEY"


def tokenset_nfa(tokens, is_negated):
    """
    First generates random str called `tokset_id`.

    returns nfa with these transitions:
        START --|eps|--> tokenset_state(is_negated, tokset_id)
        tokenset_state(is_negated, tokset_id) --|wildcard|--> EXIT
        tokenset_key_state(tokset_id) --> set(tokens)

    The transition from tokenset_key_state to set(tokens) isn't a normal transition,
    it's an auxiliary thing stored in the nfa dictionary for efficient tokenset checking.
    """

    nfa = blank_nfa()
    tokset_id = randstr()

    tokenset_state = f"{TOKENSET_PREFIX}:{is_negated}:{tokset_id}"
    rename_state(nfa, EXIT_STATE, tokenset_state)

    tokenset_key_state = f"{TOKENSET_KEY}:{tokset_id}"
    nfa[tokenset_key_state] = {"": set(tokens)}
    nfa[tokenset_state] = {"WILDCARD": {EXIT_STATE}}
    return nfa


def toks_nfa(toks, begin=False, end=False):
    """
    toks: list of toks
    begin: whether or not the toks started with ^
    end: whether or not toks ended with $
    """

    nfa = blank_nfa()
    for tok in toks:
        assert isinstance(tok, str) or isinstance(tok, int), tok
        old_end = rename_state(nfa, EXIT_STATE)
        nfa[old_end] = {tok: {EXIT_STATE}}

    if begin:
        begin_state = f"{ASSERT_BEGIN_PREFIX}:{randstr()}"
        extend_start(nfa, begin_state)
    if end:
        end_state = f"{ASSERT_END_PREFIX}:{randstr()}"
        extend_end(nfa, end_state)

    return nfa


def wildcard_nfa():
    """
    returns
        START --|eps|--> state --|WILDCARD|--> EXIT_STATE

    I'm confused why it doesn't return
        START --|WILDCARD|--> EXIT_STATE
    Room for refactoring? I think I did this for some reason which is worrying.
    """
    nfa = blank_nfa()
    old_end = rename_state(nfa, EXIT_STATE)
    nfa[old_end] = {WILDCARD: {EXIT_STATE}}
    return nfa


def repeated_definition_nfa(name, tree, start, finish, direction):
    # if direction == -1:
    #     tree = reverse_tree(tree)
    assert direction != -1, "unimplemented"
    assert start == finish == None

    return parse_tree_to_nfa(tree)


def lines_nfa(children, defns=None):
    if defns is None:
        defns = {}

    nfa = blank_nfa()
    for line in children:
        if line.data == "definition":
            name, child = line.children
            child.defns = defns

            defns[name] = child
        else:
            child_nfa = parse_tree_to_nfa(line, defns=defns)
            nfa = concat(nfa, child_nfa)

    return nfa


def phrase_nfa(children, defns=None):
    """
    children: list of parse trees

    - generates an nfa for each of the children
    - concatenates the child nfas
    - returns the resultant nfa
    """
    nfa = blank_nfa()
    for child in children:
        child_nfa = parse_tree_to_nfa(child, defns=defns)
        nfa = concat(nfa, child_nfa)
    return nfa


def or_nfa(children, defns=None):
    """
    children: list of parse trees

    returns nfa with these transitions for each child:
        START --|eps|--> CHILD_START--[child nfa]-->EXIT
    """
    nfa = {START_STATE: {"": set()}}
    for child in children:
        child_nfa = parse_tree_to_nfa(child, defns=defns)
        child_start = rename_state(child_nfa, START_STATE)
        nfa[START_STATE][""].add(child_start)
        nfa.update(child_nfa)
    return nfa


def star_nfa(child, defns=None):
    """
    child: parse tree

    returns new nfa
        child_start --[child body]-- child_exit
        START --|eps|--> child_start
        child_start --|eps|--> EXIT
        child_exit --|eps|--> child_start

           ε              ε
     START───►child_start───►EXIT
                 │     ▲
    ┌────────────┘     └────────┐
    │  ┌┬──────────────┬┐       │
    └──┼│child nfa body│┼─► child_exit
       └┴──────────────┴┘

    """
    nfa = parse_tree_to_nfa(child, defns=defns)

    child_start, child_exit = rename_bounds(nfa)

    add_eps_transition(nfa, child_start, EXIT_STATE)
    add_eps_transition(nfa, child_exit, child_start)
    add_eps_transition(nfa, START_STATE, child_start)

    return nfa


def repeat_nfa(child, min_repeat, max_repeat, defns=None):
    nfa = blank_nfa()
    # just concatenate instances of the child nfa up to the min repeat amount
    for _ in range(min_repeat):
        nfa = concat(nfa, parse_tree_to_nfa(child, defns=defns))

    if max_repeat == float("inf"):
        # if max repeat is inf, concat with a star nfa
        nfa = concat(nfa, star_nfa(child))
    else:
        # else a finite number of remaining nfas.
        cur_exit = rename_state(nfa, EXIT_STATE)
        add_eps_transition(nfa, cur_exit, EXIT_STATE)

        for _ in range(max_repeat - min_repeat):
            child_nfa = parse_tree_to_nfa(child, defns=defns)
            child_start, child_exit = rename_bounds(child_nfa)
            add_eps_transition(nfa, cur_exit, child_start)
            add_eps_transition(nfa, child_exit, EXIT_STATE)
            cur_exit = child_exit
            nfa.update(child_nfa)

    return nfa


def add_recording_layer(nfa, record_name=None):
    if record_name is None:
        record_name = randstr()
    id = randstr()
    new_start = f"{START_RECORDING_PREFIX}:{record_name}:{id}"
    new_exit = f"{END_RECORDING_PREFIX}:{record_name}:{id}"
    add_outer_layer(nfa, new_start, new_exit)
    return record_name


def named_capture_nfa(record_name, child, defns=None):
    nfa = parse_tree_to_nfa(child, defns=defns)
    add_recording_layer(nfa, record_name)

    return nfa


# def reverse_nfa(nfa):
#     # to do:
#     # swap $ and ^
#     # swap lookbehind and lookahead?
#     # swap
#     # nfa: dict[State, transitions]


def var_ref_nfa(name, start_idx, end_idx, direction, defns=None):
    assert direction != -1, "untested or unimplemented"
    if defns is None:
        defns = {}
    nfa = blank_nfa()
    if name in defns:
        return parse_tree_to_nfa(defns[name], defns=defns)

    replay_state = f"{REPLAY_RECORDING_PREFIX}:{name}:{start_idx}:{end_idx}:{direction}:{randstr()}"
    extend_end(nfa, replay_state)
    return nfa


def lookbehind_nfa(child, defns=None):
    defns = {} if defns is None else defns
    nfa = parse_tree_to_nfa(child, defns=defns)

    record_name = f"record_lookbehind_{randstr()}"
    add_recording_layer(nfa, record_name)

    id = randstr()
    add_outer_layer(
        nfa, f"{START_LOOKBEHIND_PREFIX}:{id}", f"{END_LOOKBEHIND_PREFIX}:{id}"
    )

    replay_nfa = var_ref_nfa(record_name, None, None, direction=1, defns=defns)

    nfa = concat(nfa, replay_nfa)

    return nfa


def parse_tree_to_nfa(tree, defns=None, allow_module_incompatible_groups=False):
    if defns == None:
        defns = {}

    nfa = {}
    if isinstance(tree, Tree):
        if tree.data in {
            "phrase",
            "or_phrase",
            "repeat",
            "toks",
            "wildcard",
            "tokenset",
            "repeated_definition",
            "pos",
            "named_capture",
            "var_ref"
        }:
        
            if tree.data == "phrase":
                nfa = phrase_nfa(tree.children, defns=defns)
            if tree.data == "or_phrase":
                nfa = or_nfa(tree.children, defns=defns)
            if tree.data == "repeat":
                nfa = repeat_nfa(*tree.children, defns=defns)
            if tree.data == "toks":
                nfa = toks_nfa(*tree.children)
            if tree.data == "wildcard":
                nfa = wildcard_nfa()
            if tree.data == "tokenset":
                assert len(tree.children) == 2
                nfa = tokenset_nfa(*tree.children)
            if tree.data == "repeated_definition":
                nfa = repeated_definition_nfa(*tree.children)
            if tree.data == "named_capture":
                nfa = named_capture_nfa(*tree.children, defns=defns)
            if tree.data == "var_ref":
                nfa = var_ref_nfa(*tree.children, defns=defns)
            if tree.data == "pos":
                nfa = blank_nfa()

            add_group_handling(tree, nfa)

        elif tree.data in {"lines", "lookbehind"}:
            assert (
                allow_module_incompatible_groups is True
            ), f"regex group {tree.data} doesn't currently work with tokre prediction modules. (pytorch modules in tokre.modules)"
            if tree.data == "lines":
                return lines_nfa(tree.children, defns=defns)
            elif tree.data == "lookbehind":
                assert len(tree.children) == 1
                return lookbehind_nfa(tree.children[0], defns=defns)
            else:
                raise ValueError(f'Unrecognized tree.data: {tree.data}')

        else:
            assert False, f"unrecognized tree in parse_tree_to_nfa: {tree}"

    return nfa


from .parse import parse



def get_nfa(pattern_str):
    parse_tree = parse(pattern_str)
    nfa = parse_tree_to_nfa(parse_tree)
    return nfa


def same_list(l1, l2):
    return all([a == b for a, b in zip(l1, l2)]) and len(l1) == len(l2)


def get_replay_info(state):
    assert state.startswith(REPLAY_RECORDING_PREFIX)
    recording_name, rec_start, rec_end, rec_dir = state.split(":")[1:-1]

    rec_dir = int(rec_dir)
    rec_start = None if rec_start == "None" else int(rec_start)
    rec_end = None if rec_end == "None" else int(rec_end)
    if rec_start is not None and rec_end is not None and rec_start > rec_end:
        rec_start, rec_end = rec_end, rec_start

    rec_slice = slice(rec_start, rec_end, rec_dir)
    return recording_name, rec_slice


from copy import copy


class Set:
    def __init__(self, data=None, parent=None):
        self.parent = parent
        self.parent_calls = 0
        self.data = set()
        self.parent_calls_before_merge = 5

    def add(self, item):
        self.data.add(item)

    def __in__(self, item):
        if item in self.data:
            return True
        elif self.parent is not None:
            self.parent_calls += 1
            if self.parent_calls >= self.parent_calls_before_merge:
                self.data = self.data + self.parent.all_data
                self.parent = None
                return self.__in__(item)
            else:
                return self.parent.__in__(item)
        return False

    @property
    def all_data(self):
        if self.parent is None:
            return self.data
        return self.data + self.parent.all_data

    def copy(self):
        return Set(parent=self)


class Dict:
    def __init__(self, data=None, parent=None):
        self.parent = parent
        self.parent_calls = 0
        self.data = data if data is not None else {}
        self.parent_calls_before_merge = 5

    def add(self, key, value):
        self.data[key] = value

    def __getitem__(self, key):
        if key in self.data:
            return self.data[key]
        elif self.parent is not None:
            self.parent_calls += 1
            if self.parent_calls >= self.parent_calls_before_merge:
                self.data = {**self.data, **self.parent.all_data}
                self.parent = None
                return self.__getitem__(key)
            else:
                return self.parent[key]
        else:
            raise KeyError(f"{key} not found")

    def __contains__(self, key):
        # copilot generated
        if key in self.data:
            return True
        elif self.parent is not None:
            self.parent_calls += 1
            if self.parent_calls >= self.parent_calls_before_merge:
                self.data = {**self.data, **self.parent.all_data}
                self.parent = None
                return self.__contains__(key)
            else:
                return key in self.parent
        return False

    def __setitem__(self, key, value):
        self.data[key] = value

    def __delitem__(self, key):
        del self.data[key]

    def __iter__(self):
        return iter(self.data)

    @property
    def all_data(self):
        if self.parent is None:
            return self.data
        return {**self.data, **self.parent.all_data}

    def copy(self):
        return Dict(self)


def check(toks, nfa, any_prefix=True, any_suffix=True, return_group=False):
    assert isinstance(toks, list)

    all_matches = []
    pennies = [
        {
            "state": START_STATE,
            "i": i,
            "eps_seen_states": set(),
            "active_recordings": {"string": i},
            "completed_recordings": {},
            "active_lookbehinds": [],
            "group_data": [],
        }
        for i in range(len(toks))
        if any_prefix or i == 0
    ]
    while pennies:
        penny = pennies.pop()
        state = penny["state"]

        if state.startswith(START_LOOKBEHIND_PREFIX):
            lookbehind_id = state.split(":")[1]
            penny["active_lookbehinds"].append(
                {"id": lookbehind_id, "start_idx": penny["i"]}
            )

        if state.startswith(END_LOOKBEHIND_PREFIX):
            lookbehind_id = state.split(":")[1]
            assert (
                "active_lookbehinds" in penny
            ), "Bug: this state shouldn't be attainable"
            assert (
                penny["active_lookbehinds"][-1]["id"] == lookbehind_id
            ), "Bug: this state shouldn't be attainable"
            lookbehind = penny["active_lookbehinds"].pop()
            penny["i"] = lookbehind["start_idx"]

        lookbehind = len(penny.get("active_lookbehinds", [])) % 2 == 1
        next_idx = penny["i"] if lookbehind is False else penny["i"] - 1
        if next_idx >= 0 and next_idx < len(toks):
            next_tok = toks[next_idx]
        else:
            next_tok = False

        state_transitions = nfa.get(state, {})

        if state.startswith(ASSERT_END_PREFIX):
            if penny["i"] != len(toks):
                continue
        if state.startswith(ASSERT_BEGIN_PREFIX):
            if penny["i"] != 0:
                continue

        if state.startswith(START_GROUP_DATA):
            _, name, idx, id = state.split(":")
            group_data = GroupData(
                name=name, idx=int(idx), id=id, start=penny["i"], end=None, children=[]
            )
            penny["group_data"].append(group_data)

        if state.startswith(END_GROUP_DATA):
            _, name, idx, id = state.split(":")

            assert len(penny["group_data"]) > 0
            last_opened_group = penny["group_data"][-1]
            assert last_opened_group.name == name
            assert last_opened_group.idx == int(idx)
            assert last_opened_group.id == id

            if len(penny["group_data"]) >= 2:
                group_data = penny["group_data"].pop(-1)
                assert isinstance(penny["group_data"][-1], GroupData)
                group_data.end = penny["i"]
                penny["group_data"][-1].children.append(group_data)

        if state == EXIT_STATE:
            if any_suffix or penny["i"] == len(toks):
                start, end = penny["active_recordings"]["string"], penny["i"]
                penny["completed_recordings"]["string"] = [toks[start:end], start, end]
                assert len(penny["group_data"]) == 1, penny["group_data"]

                group_data = penny["group_data"].pop()
                group_data.end = end
                
                match_str = None
                # if isinstance(toks[0], str):
                #     match_str = "".join(toks[start:end])
                # elif isinstance(toks[0], int):
                #     match_str = tokre.decode(toks[start:end])
                # else:
                #     assert False
                

                if return_group is True:
                    all_matches.append(deepcopy(group_data))
                else:
                    match = Match(
                        match_str=match_str,
                        start=start,
                        end=end,
                        group_data=deepcopy(group_data),
                    )
                    all_matches.append(match)
                continue  # drop this penny and move to next

        if state.startswith(REPLAY_RECORDING_PREFIX):
            recording_name, rec_slice = get_replay_info(state)

            if recording_name not in penny["completed_recordings"]:
                continue
            record_val, start, end = new_penny["completed_recordings"][recording_name]
            record_val = record_val[rec_slice]

            if same_list(
                toks[new_penny["i"] : new_penny["i"] + len(record_val)], record_val
            ):
                penny["i"] += len(record_val)
                # penny["transitions"].append((state, record_val, state))
            else:
                continue

        if state.startswith(START_RECORDING_PREFIX):
            recording_name = state.split(":")[1]
            penny["active_recordings"][recording_name] = penny["i"]

        if state.startswith(END_RECORDING_PREFIX):
            recording_name = state.split(":")[1]

            start, end = penny["active_recordings"][recording_name], penny["i"]
            penny["completed_recordings"][recording_name] = [
                toks[start:end],
                start,
                end,
            ]
            del penny["active_recordings"][recording_name]

        if state.startswith(TOKENSET_PREFIX):
            is_negated = state.split(":")[1] == "True"
            tokset_id = state.split(":")[2]
            tokenset = nfa[f"{TOKENSET_KEY}:{tokset_id}"][""]
            assert isinstance(next_tok, int) or isinstance(next_tok, str) or isinstance(next_tok, bool)
            
            if (next_tok in tokenset and not is_negated) or (next_tok not in tokenset and is_negated):
                # penny["i"] += 1 if not lookbehind else -1
                # penny['eps_seen_states'] = set()
                pass
            else:
                continue

        transitions = [
            (next_tok, next_state)
            for k, next_states in state_transitions.items()
            for next_state in next_states
            if (k == next_tok or k == WILDCARD) and next_tok is not False
        ]
        eps_transitions = [
            ("", next_state)
            for next_state in state_transitions.get("", set())
            if next_state not in penny["eps_seen_states"]
        ]
        transitions.extend(eps_transitions)

        for key, next_state in transitions:

            if len(transitions) == 1:
                new_penny = penny
            elif key == "":
                new_penny = copy(penny)
                new_penny["eps_seen_states"] = deepcopy(penny["eps_seen_states"])
                new_penny["active_recordings"] = deepcopy(penny["active_recordings"])
                new_penny["completed_recordings"] = deepcopy(
                    penny["completed_recordings"]
                )
                new_penny["active_lookbehinds"] = deepcopy(penny["active_lookbehinds"])
                new_penny["group_data"] = deepcopy(penny["group_data"])
            else:
                new_penny == copy(penny)
                for k in set(penny.keys()) - {"eps_seen_states"}:
                    new_penny[k] = deepcopy(penny[k])
                new_penny["eps_seen_states"] = set()

            if key == "":
                new_penny["eps_seen_states"].add(penny["state"])
            else:
                new_penny["eps_seen_states"] = set()
                new_penny["i"] += 1 if not lookbehind else -1

            new_penny["state"] = next_state

            pennies.append(new_penny)
    else:
        return all_matches


def set_to_list(nfa):
    return {
        state: {obs: list(dests) for obs, dests in transitions.items()}
        for state, transitions in nfa.items()
    }


from functools import partial
from multiprocessing import Pool


def match_all(script, docs, defns=None, see_tree=True):
    if defns is None:
        defns = {}
    tree = parse(script, defns=defns)

    if see_tree is True:
        print(tree.pretty())

    nfa = parse_tree_to_nfa(tree, defns=defns)

    check_with_nfa = partial(check, nfa=nfa)

    with Pool(5) as p:
        res = p.map(check_with_nfa, docs)

    res = {i: it for i, it in enumerate(res) if len(it) > 0}
    return res


import numpy as np



def filter_duplicate_matches(matches, aggr="longest"):

    assert aggr in {"longest", "shortest"}
    matches_by_idx = {}

    for match in matches:
        if match.end in matches_by_idx:
            logged_match = matches_by_idx[match.end]
            # this match is longer
            if len(match) > len(logged_match) and aggr == "longest":
                matches_by_idx[match.end] = match
            if len(match) < len(logged_match) and aggr == "shortest":
                matches_by_idx[match.end] = match
        else:
            matches_by_idx[match.end] = match

    matches = list(matches_by_idx.values())

    return matches


# script = r''' Once upon(?<= Once upon) a time'''


if __name__ == "__main__":
    script = r"""
.*(?<= Benny)
"""

    story = """Once upon a time, in a colorful world filled with magic, there lived a small, cheerful bear named Benny. Benny was a sunny-yellow bear with a big, friendly smile and the softest fur imaginable. He lived in a cozy cave at the edge of the Whimsical Woods, a place where the trees were candy-colored and the rivers sparkled like diamonds.

    One sunny morning, Benny decided he wanted to have a picnic. So, he put on his favorite red hat, packed his picnic basket with delicious honey sandwiches, juicy berries, and a big bottle of lemonade, and set out on an adventure.

    As he strolled through the Whimsical Woods, he sang a happy tune, greeting all his friends along the way. There was Gabby the Giraffe, with her long, long neck; Toby the Turtle, slow and wise; and Lila the Ladybug, small and quick, fluttering around like a tiny red kite.

    "Hello, friends!" Benny called out cheerily. "I'm going on a picnic. Would you like to join me?"

    "Oh, yes, please!" they all said, for who could resist a picnic with a friend like Benny?

    They found the perfect spot in a clearing."""

    parsed = parse(script)
    # see_parse(parsed)
    nfa = parse_tree_to_nfa(parsed)
    print(parsed.pretty())

    out = check(tok_see(story, printout=False), nfa)
    for s in out[0:3]:
        print(s)
    print(len(out))

    if len(out) == 0:
        print("no matches")
