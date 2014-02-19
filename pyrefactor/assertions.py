import ast

from ._unparse import unparse
from .utils import preserves_trailing_whitespaces, get_expr, noop_on_syntax_errors

@noop_on_syntax_errors
@preserves_trailing_whitespaces
def toggle_assert_style(s):
    returned = expr = ast.parse(s).body[0]
    if isinstance(expr, ast.Assert):
        returned = _assert_to_assert_method(expr)

    elif isinstance(expr.value, ast.Call) and isinstance(expr.value.func, ast.Attribute) and expr.value.func.value.id == "self":
        returned = _assert_method_to_assert(expr.value)

    return unparse(returned)

def _assert_to_assert_method(expr):
    if isinstance(expr.test, ast.Compare):
        [op] = expr.test.ops
        if isinstance(op, ast.Eq):
            args = [expr.test.left, expr.test.comparators[0]]
            if expr.msg is not None:
                args.append(expr.msg)
            return _construct_method("assertEquals", args)
    return expr

def _assert_method_to_assert(expr):
    if expr.func.attr != "assertEquals":
        return expr

    returned = ast.Assert()
    returned.test = ast.Compare()
    returned.test.left=expr.args[0]
    returned.test.ops = [ast.Eq()]
    returned.test.comparators = [expr.args[1]]
    returned.msg = expr.args[2] if len(expr.args) > 2 else None
    return returned

def _construct_method(name, args):
    assertion = ast.Call()
    assertion.func = ast.Attribute(ast.Name("self", ast.Load()), name, ast.Load())
    assertion.args = list(args)
    assertion.keywords = []
    assertion.starargs = assertion.kwargs = None

    returned = ast.Expression()
    returned.value = assertion
    return returned
