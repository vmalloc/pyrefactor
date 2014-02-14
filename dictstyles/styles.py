import ast
import functools
import itertools

from ._unparse import unparse


def _preserves_trailing_whitespaces(func):
    @functools.wraps(func)
    def new_func(s):
        trailing = "".join(itertools.takewhile(lambda s: s.isspace(), s[::-1]))[::-1]
        returned = func(s)
        return returned.rstrip() + trailing
    return new_func


def toggle_style(s):
    if s.startswith("{"):
        return curly_to_dict(s)
    return dict_to_curly(s)

@_preserves_trailing_whitespaces
def curly_to_dict(s):
    expr = _get_expr(s)
    returned = ast.Call()
    returned.func = ast.Name()
    returned.func.id = 'dict'
    returned.args = []
    returned.keywords = []
    for key, value in zip(expr.keys, expr.values):
        if not isinstance(key, ast.Str):
            return s
        keyword = ast.keyword(arg=key.s, value=value)
        returned.keywords.append(keyword)
    returned.starargs = None
    returned.kwargs = None
    return unparse(returned)

@_preserves_trailing_whitespaces
def dict_to_curly(s):
    expr = _get_expr(s)
    returned = ast.Dict()
    returned.keys = []
    returned.values = []
    for keyword in expr.keywords:
        returned.keys.append(ast.Str(s=keyword.arg))
        returned.values.append(keyword.value)
    return unparse(returned)

def _get_expr(s):
    tree = ast.parse(s)
    [expr] = tree.body
    return expr.value
