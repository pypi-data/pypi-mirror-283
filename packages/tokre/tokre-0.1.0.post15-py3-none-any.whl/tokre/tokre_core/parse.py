import lark
from lark import Lark, Transformer, Tree, v_args

import tokre



grammar = r"""
    ?start: lines
    
    DIGIT : "0".."9"
    
    SPECIAL: /[\^$|&*+{}()<>?\[\]\\.\n=;#]/
    BEGIN: /\^/
    
    END: /\$/
    WILDCARD: "."
    ESCAPED: "\\" WILDCARD | "\\" SPECIAL | "\\" BEGIN | "\\" END | "\\" CHAR
    wildcard: "."

    CHAR: /[^\^$\\|&*+{}()<>\[\]?.=;\n]/
    esc_newline.5: "\\n"
    char: esc_newline | ESCAPED | CHAR
    
    
    _SPACE: " "
    _TAB: "\t"
    _PAD: (_SPACE | _TAB)+
    _NEWLINE: "\n"
    _SEMICOLON: ";"
    _EQ: "="
    
    
    # tab: "\t"
    # space: " "
    # _pad: (space | tab)+
    ?padded{a}: _PAD? a _PAD?
    
    neg_sign: "-"
    int: neg_sign DIGIT+ | DIGIT+
    ?nat : neg_sign DIGIT+ | DIGIT+ # include negative numbers to throw more informative error
    
    # atom_phrase: (or | and | atom+ | char_sequence)
    
    
    char_phrase: BEGIN? (char)+ END? | BEGIN END? | BEGIN? END

    and_phrase: (phrase) ("&" phrase)+
    or_phrase: (phrase) ("|" phrase)+

    ?tokenset_char: ESCAPED | /[^\n\^|{}0-9]/
    TOKENSET_NOT: "^"
    TOKENSET_SPLIT: "|"
    tokenset_interior: TOKENSET_NOT? (tokenset_char+ | (TOKENSET_SPLIT | tokenset_char+)+)
    tokenset: "{{" tokenset_interior "}}" | "{" tokenset_interior "}"

    ?atom: group | lookaround | variable | repeat | tokenset | wildcard  
    ?phrase: (atom | or_phrase | and_phrase | wildcard | (char_phrase? (atom char_phrase?)*)) _PAD?
    
    # semantic_tok_definition: padded{var_name} _EQ semantic_tok_label
    definition: padded{var_name} _EQ phrase
    
    

    # ?lines: (definition | phrase)? (((_NEWLINE | ";") phrase | definition) | (_NEWLINE | ";"))*
    ?lines: _NEWLINE* ( definition | phrase) ((_NEWLINE | ";")+ ( definition | phrase))*

    ?group: "(" phrase ")"

    # NOT_SYMBOL: /\^/
    # ?not_group: "(" NOT_SYMBOL (or_phrase | and_phrase) ")"

    lookbehind: "(?<=" phrase ")"
    lookahead: "(?=" phrase ")"
    neg_lookbehind: "(?<!" phrase ")"
    neg_lookahead: "(?!" phrase ")"
    ?lookaround: lookbehind | lookahead | neg_lookbehind | neg_lookahead

    # semantic_tok_label_char: /[^\n\[\]]/
    # semantic_tok_label: "[[" semantic_tok_label_char+ "]]"
    
    VAR_CHAR: /[^<>=:\\\^$&*+{}\[\]()0-9\n]/
    
    var_name: VAR_CHAR+
    
    named_capture: "[" padded{var_name} "=" phrase"]"
    var_ref: "[" padded{var_name} "]"

    
    slice: "[" [int] ":" [int] "]"
    slice_var_ref: "[" _PAD? var_name slice _PAD? "]"
    index_var_ref: "[" _PAD? var_name "[" int "]" _PAD? "]"

    ?variable: var_ref | slice_var_ref | index_var_ref | named_capture
    
    repeat_bounds: "{" _PAD? [nat] "," _PAD? [nat]"}"
    repeat_bounded: atom repeat_bounds

    repeat_lone_number: "{" _PAD? nat _PAD? "}"
    repeat_exact: atom repeat_lone_number
    repeat_star: atom "*"
    repeat_plus: atom "+"
    optional: atom "?"

    ?repeat: repeat_exact | repeat_star | repeat_plus | optional | repeat_bounded
"""

special_tokre_chars = r"\^$|&*+{}()<>?[].=;"+"\n"

def escape(s):
    """
    Escapes special characters in a string for use in tokre patterns.
    
    Args:
    s (str): The input string to escape.
    
    Returns:
    str: The escaped string.
    """
    special_chars_wo_newline = r"\^$|&*+{}()<>?[].=;"
    s = ''.join('\\' + c if c in special_chars_wo_newline else c for c in s)
    s = s.replace("\n", "\\n")
    return s


def convert_int_to_tree(z):
    return Tree("int", [str(z)])


def convert_nat_to_tree(n):
    return Tree("nat", [str(n)])


def get_group(items):
    assert isinstance(items, list)
    if len(items) == 0:
        assert False
    if len(items) == 1:
        return items[0]
    else:
        return Tree("group", items)


from lark import Token


def get_num(num_elem):
    if isinstance(num_elem, Token):
        return int(num_elem)
    return int("".join([d.value for d in num_elem.children]))


class Preprocessor(Transformer):
    def phrase(self, items):
        if len(items) == 0:
            return lark.visitors.Discard
        return Tree("phrase", items)

    def RULE(self, children):
        return


class NumberTransformer(Transformer):
    @v_args(inline=True)
    def DIGIT(self, num):
        return int(num)

    def nat(self, items):
        assert (
            items[0] != "-"
        ), "Negative sign before a natural number. Probably inside a repetition? EG x{1, -2} or y{-3})"
        return int("".join([str(x) for x in items]))

    @v_args(inline=True)
    def neg_sign(self):
        return "-"

    def int(self, items):
        return int("".join([str(x) for x in items]))


class RepeatTransformer(Transformer):
    @v_args(inline=True)
    def repeat_lone_number(self, num):
        return num

    def repeat_exact(self, items):
        num = items[-1]
        return Tree("repeat", [get_group(items[:-1]), num, num])

    def repeat_star(self, items):
        return Tree("repeat", [get_group(items), 0, float("inf")])

    def repeat_plus(self, items):
        return Tree("repeat", [get_group(items), 1, float("inf")])

    def optional(self, items):
        return Tree("repeat", [get_group(items), 0, 1])

    @v_args(inline=True)
    def repeat_bounds(self, start, end):
        if start is None:
            start = 0
        if end is None:
            end = float("inf")
        return (start, end)

    def repeat_bounded(self, items):
        atom = items[0]
        start, end = items[1]
        return Tree("repeat", [atom, start, end])


def bounds_assertions(bounds):
    assert isinstance(bounds[0], int) or bounds[0] is None
    assert isinstance(bounds[1], int) or bounds[1] is None
    if isinstance(bounds[0], int) and isinstance(bounds[1], int):
        assert not (bounds[0] < 0 and bounds[1] > 0), "unimplemented"
        if bounds[0] >= 0 and bounds[1] >= 0:
            assert bounds[1] >= bounds[0]
        if bounds[0] < 0 and bounds[1] < 0:
            assert bounds[0] <= bounds[-1]


class SliceTransformer(Transformer):
    @v_args(inline=True)
    def index_var_ref(self, name, num):
        if num == -1:
            return Tree("var_ref", [name, -1, None, 1])
        else:
            return Tree("var_ref", [name, num, num + 1, 1])

    @v_args(inline=True)
    def slice(self, start, end):
        return (start, end)

    def var_name(self, items):
        name = "".join([x.value for x in items])
        return name

    @v_args(inline=True)
    def var_ref(self, name):
        return Tree("var_ref", [name, None, None, 1])

    @v_args(inline=True)
    def slice_var_ref(self, name, bounds):
        if bounds[0] == 0:
            bounds = (None, bounds[1])

        bounds_assertions(bounds)
        return Tree("var_ref", [name, *bounds, 1])


class CharTransformer(Transformer):
    def CHAR(self, items):
        return items

    def PAD(self, items):
        return " "

    def ESCAPED(self, items):
        if (items[0] == "\\") and (items[1] == "n"):
            return items  # leave as is
        else:
            return items[1:]

    def SPACE(self, items):
        return " "


class StringTransformer(Transformer):
    def __init__(self, replace_w_tok_ids=False):
        super().__init__()

    def char_phrase(self, items):
        if len(items) >= 1:
            start = items[0] == "^"
            end = items[-1] == "$"
            if start:
                items = items[1:]
            if end:
                items = items[:-1]

        assert all([x.data == "char" for x in items])
        assert all([len(x.children) == 1 for x in items])

        # this includes double newlines
        s = "".join([x.children[0].replace("\\n", "\n") for x in items])

        # if leading whitespace, strip it and add a single space
        if len(s) > 0 and s[0] == " ":
            s = s.lstrip(" \t")
            s = " " + s

        # if trailing whitespace, strip it
        if len(s) > 0 and s[-1] in [" "]:
            s = s.rstrip(" \t")

        # toks = tok_see(s, printout=False) if len(s) > 0 else []
        toks = (
            [tokre.decode([tok_id]) for tok_id in tokre.encode(s)] if len(s) > 0 else []
        )
        toks = preprocess_toks(toks)

        if len(toks) == 0:
            return lark.visitors.Discard

        return Tree("toks", [toks, start, end])


class CombineOrPhrases(Transformer):
    def or_phrase(self, items):
        result = []
        for item in items:
            if item.data == "or_phrase":
                result.extend(item.children)
            else:
                result.append(item)
        return Tree("or_phrase", result)


class CollapseDefinitionNodes(Transformer):
    def repeated_definition(self, children):
        assert len(children) == 5
        if children[-3] is None and children[-2] is None and children[-1] == 1:
            return children[1]


class CollapseNestedPhrases(Transformer):
    def phrase(self, items):
        result = []
        for item in items:
            if item.data == "phrase":
                result.extend(item.children)
            else:
                result.append(item)
        return Tree("phrase", result)


# class ReverseTransformer(Transformer):
#     def phrase(self, items):
#         # assert False, 'bug here'
#         return Tree('phrase', items[::-1])
#     def toks(self, items):
#         toks, begin, end = items[0], items[1], items[2]
#         return Tree('toks', [toks[::-1], end, begin])
#     @v_args(inline=True)
#     def var_ref(self, var_name, start, end, direction):
#         new_start, new_end = end, start
#         new_start = (-new_start) if new_start is not None else None
#         new_end = (-new_end) if new_end is not None else None

#         return Tree('var_ref', [var_name, new_start, new_end, -direction])
#     # def lookbehind(self, items):
#     #     print('entering lookbehind reversal, untested')
#     #     print(items)
#     #     print()
#     #     return Tree('lookahead', items[::-1])


# reverser = ReverseTransformer()

# mb bugged
# def reverse_tree(tree):
#     assert isinstance(tree, Tree) and not isinstance(tree, Token)
#     print('maybe bugged reverse tree')
#     return Tree(tree.data, [reverser.transform(child) for child in tree.children])


def preprocess_toks(toks: list[str]):
    assert isinstance(toks, list)
    assert all([isinstance(tok, str) for tok in toks])
    # toks = [f'{t}' for t in toks]
    toks = [t.replace(" ", "⋅").replace("\n", "↵") for t in toks]
    return toks


class ReverserTransformer(Transformer):
    def phrase(self, items):
        return Tree("phrase", items[::-1])

    def toks(self, items):
        toks, begin, end = items[0], items[1], items[2]
        return Tree("toks", [toks[::-1], end, begin])

    @v_args(inline=True)
    def var_ref(self, var_name, start, end, direction):
        new_start, new_end = end, start
        new_start = (-new_start) if new_start is not None else None
        new_end = (-new_end) if new_end is not None else None

        return Tree("var_ref", [var_name, new_start, new_end, -direction])


class LookbehindTransformer(Transformer):
    def lookbehind(self, items):
        return Tree("look_and_return", [Tree("backwards", [Tree("reversed", items)])])

    def lookahead(self, items):
        return Tree("look_and_return", [items])

    def neg_lookbehind(self, items):
        return Tree(
            "neg_look_and_return", [Tree("backwards", [Tree("reversed", items)])]
        )

    def neg_lookahead(self, items):
        return Tree("neg_look_and_return", [items])


class ApplyReversed(Transformer):
    def reversed(self, items):
        return [ReverserTransformer().transform(it) for it in items[::-1]]


class TokensetTransformer(Transformer):
    def tokenset_interior(self, items):
        if str(items[0]) == "^":
            items = items[1:]
            not_ = True
        else:
            not_ = False
        return items, not_

    def tokenset(self, items):
        tokens, not_ = items[0]
        # split by tokens with type 'TOKENSET_SPLIT'
        grouped_chars = [[]]
        for i, tok in enumerate(tokens):
            if isinstance(tok, Token) and tok.type == "TOKENSET_SPLIT":
                grouped_chars.append([])
            else:
                grouped_chars[-1].append(tok)

        toks = []
        for group in grouped_chars:
            toks.extend(
                [tokre.decode([tok_id]) for tok_id in tokre.encode("".join(group))]
            )

        toks = preprocess_toks(toks)

        return Tree("tokenset", [toks, not_])


def toks_to_tok_ids(toks: list[str]):
    assert isinstance(toks, list)
    assert all([isinstance(tok, str) for tok in toks])
    # toks = [f'{t}' for t in toks]
    raw_toks = [t.replace("⋅", " ").replace("↵", "\n") for t in toks]
    # tok_ids = [enc(t, add_begin=False, padding=False)[0][0].item() for t in raw_toks]
    tok_ids = [tokre.encode(t)[0] for t in raw_toks]
    return tok_ids


class ConvertTokensToTokIds(Transformer):
    def tokenset(self, items):
        assert len(items) == 2
        toks, not_ = items
        tok_ids = toks_to_tok_ids(toks)
        return Tree("tokenset", [tok_ids, not_])

    def toks(self, items):
        assert len(items) == 3
        toks, start, end = items
        tok_ids = toks_to_tok_ids(toks)
        return Tree("toks", [tok_ids, start, end])


def recursively_add_definitions(tree, defns=None):
    if defns is None:
        defns = {}
    if isinstance(tree, Tree):
        if tree.data == "lines":
            transformed_children = []
            for child in tree.children:
                if child.data == "definition":
                    defn_name, child_tree = child.children
                    defns[defn_name] = recursively_add_definitions(
                        child_tree, defns=deepcopy(defns)
                    )
                else:
                    # ignore empty lines
                    if child.data == "phrase" and len(child.children) == 0:
                        continue
                    transformed_children.append(
                        recursively_add_definitions(child, defns=deepcopy(defns))
                    )
            tree = Tree("phrase", transformed_children)
        elif tree.data == "var_ref" and tree.children[0] in defns:
            name, start, finish, direction = tree.children
            tree = Tree(
                "repeated_definition",
                [name, deepcopy(defns[name]), start, finish, direction],
            )
        else:
            new_children = [
                recursively_add_definitions(child, defns=defns)
                for child in tree.children
            ]
            return Tree(tree.data, new_children)

    return tree


parser = Lark(grammar, start="start", lexer="dynamic", parser="earley")


def add_names_and_idx(tree, name="", idx=0):
    # adds a unique name to each node and an idx attribute corresponding to
    # the node's idx/order among the children of its parent

    # assert not hasattr(tree, "name"), tree
    # assert not hasattr(tree, "idx"), tree

    if name == "":
        name = tree.data
    else:
        name = name + "." + tree.data
    name = name + f"_{idx}"
    tree.name = name
    tree.idx = idx
    child_idx = 0
    for child in tree.children:
        if isinstance(
            child, Tree
        ):  # and not (tree.data == 'phrase' and child.data == 'toks'):
            add_names_and_idx(child, name=name, idx=child_idx)
            child_idx += 1


def print_parsed(parsed, indent=""):
    if isinstance(parsed, Tree):
        print(indent + parsed.data)
        indent = indent + "  "
        for child in parsed.children:
            print_parsed(child, indent=indent)


from copy import deepcopy
from typing import Optional
import json


def extract_var_refs(tree):
    if hasattr(tree, "data") and tree.data == "var_ref":
        ref_name = tree.children[0]
        return [ref_name]
    else:
        if hasattr(tree, "children"):
            ref_names = [
                ref_name
                for child in tree.children
                for ref_name in extract_var_refs(child)
            ]
            ref_names = list(set((ref_names)))
            return ref_names
        else:
            return []


def get_dependencies(tree):
    workspace = tokre.get_workspace()
    dependencies = {}

    var_refs = extract_var_refs(tree)
    dependencies["_base"] = var_refs

    new_refs = deepcopy(var_refs)

    while new_refs:
        var_ref = new_refs.pop()
        if var_ref in dependencies:
            continue

        var_ref_path = workspace / f"{var_ref}.json"
        if not var_ref_path.is_file():
            continue

        with var_ref_path.open("r") as f:
            pattern = json.load(f)["pattern"]
            dependent_refs = extract_var_refs(tokre.parse(pattern, is_dependency=True))
            dependencies[var_ref] = dependent_refs
            new_refs.extend(dependent_refs)

    return dependencies


def topological_sort(dependencies):
    visited = set()
    stack = []

    def dfs(node):
        if node in stack:
            raise ValueError(f"Cyclical dependency detected at {node}")
        if node not in visited:
            visited.add(node)
            for dep in dependencies.get(node, []):
                dfs(dep)
            stack.append(node)

    for node in dependencies:
        if node not in visited:
            dfs(node)

    return stack


def parse(s, defns: dict = None, tok_ids=False, is_dependency=False, suppress_info=False):
    if defns is None:
        defns = {}
    # if defns is stored elsewhere, we don't want to mutate it in this function.
    defns = deepcopy(defns)

    assert "BEGIN" not in defns, "[BEGIN] is reserved for [BEGIN] token"
    assert (
        "pos" not in defns
    ), "[pos] is reserved for injecting absolute position into token modules"
    assert (
        "tok" not in defns
    ), "[tok] is reserved for injecting prev token info into token modules"


    defns.update(
        {"BEGIN": Tree("toks", [["[BEGIN]"], None, None]), "pos": Tree("pos", [])}
    )

    parsed = parser.parse(s)

    parsed = Preprocessor().transform(parsed)

    parsed = NumberTransformer().transform(parsed)
    parsed = RepeatTransformer().transform(parsed)

    parsed = SliceTransformer().transform(parsed)
    parsed = CharTransformer().transform(parsed)
    parsed = StringTransformer().transform(parsed)
    parsed = LookbehindTransformer().transform(parsed)
    parsed = TokensetTransformer().transform(parsed)

    parsed = CombineOrPhrases().transform(parsed)

    # parsed = RemoveNones().transform(parsed)

    if not is_dependency:
        imports = topological_sort(get_dependencies(parsed))[:-1]
        if len(imports) > 0:
            workspace = tokre.get_workspace()
            imported_defns = []
            for dep_name in imports:
                dep_path = workspace / f"{dep_name}.json"
                if dep_path in workspace.iterdir():
                    assert (
                        dep_path.is_file()
                    ), f"This imported .json is surprisingly not a file: {dep_path}"
                    with dep_path.open("r") as f:
                        dep_script = json.load(f)["pattern"]
                        dep_parsed = tokre.parse(dep_script, is_dependency=True)
                        if dep_parsed.data == "lines":
                            lines = parsed.children
                            imported_defns.extend(
                                [line for line in lines if line.data == "definition"]
                            )
                            non_defns = [
                                line for line in lines if line.data != "definition"
                            ]
                            if len(non_defns) == 1:
                                combined_lines = non_defns[0]
                            else:
                                combined_lines = Tree(
                                    "phrase",
                                    [
                                        line
                                        for line in lines
                                        if line.data != "definition"
                                    ],
                                )
                            imported_defns.append(
                                Tree("definition", [dep_name, combined_lines])
                            )
                        else:
                            imported_defns.append(
                                Tree("definition", [dep_name, dep_parsed])
                            )

            if imported_defns and not suppress_info:
                print("imported:", imported_defns)

            if parsed.data == "lines":
                parsed.children = imported_defns + parsed.children
            else:
                parsed = Tree("lines", imported_defns + [parsed])

    if not is_dependency:
        parsed = recursively_add_definitions(parsed, defns=defns)
        parsed = CollapseDefinitionNodes().transform(parsed)
        parsed = CollapseNestedPhrases().transform(parsed)

    if tok_ids:
        parsed = ConvertTokensToTokIds().transform(parsed)

    add_names_and_idx(parsed)

    return parsed


if __name__ == "__main__":
    tests = {
        "repeat": r"(test){1, 10}",
        "numbers outside of brackets": r"123",
        "test": r"test",
        "space test": r" test",
        "numbers inside of brackets": r"  bb  [test[2]] ",
        "repeat": r"[test]{1, 2}",
        "repeat exact": r"(test){1}",
        "repeat star": r"(test)*",
        "repeat plus": r"(test)+",
        "optional": "( test )?\nTest",
        "definition": "a = b\n[a]{2}",
        "var ref": r"b\n",
        "index var ref": r"test=test; [test[2]]",
        "slice var ref": r"[  test[2:3]  ]",
        "slice var ref 2": r"[test[:3]]",
        "slice var ref 3": r"[test[2:]]",
        "slice var ref 4": r"[test[:]]",
        "or": r"(test | test2)",
        "and": r"(test2 | (. & test3 (?=test)))",
        "group": r"(test)",
        "char sequence": r" a b c",
        " or without parens": r" test | test2",
        " and without parens": r" test & test2",
        # 'final': ' this is a test of the parser\.'
    }

    tests = {
        # 'lookbehind': '^[test= time](?<= Once upon a [test[:3]])'
        "start_test": "^ test"
    }

    for name, test in tests.items():
        # parsed = parser.parse(test)

        # parsed = NumberTransformer().transform(parsed)
        # parsed = RepeatTransformer().transform(parsed)
        # parsed = SliceTransformer().transform(parsed)
        # parsed = CharTransformer().transform(parsed)
        # parsed = StringTransformer().transform(parsed)
        # print(parsed)

        parsed = parse(test)

        # s = parsed.pretty()
        # print(name+':', test)
        # print(s)
        # print()
        # toks = tok_see('A test of the parser', printout=False)
        # print(toks)
        # print(parsed)
