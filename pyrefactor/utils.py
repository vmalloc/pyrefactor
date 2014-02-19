import ast
import functools
import itertools

def preserves_trailing_whitespaces(func):
    @functools.wraps(func)
    def new_func(s):
        trailing = "".join(itertools.takewhile(lambda s: s.isspace(), s[::-1]))[::-1]
        returned = func(s)
        return returned.rstrip() + trailing
    return new_func

def get_expr(s):
    tree = ast.parse(s)
    [expr] = tree.body
    return expr.value
