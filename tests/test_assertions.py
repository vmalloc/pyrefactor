from pyrefactor.assertions import toggle_assert_style


def test_assert_equals():
    for assert_form, method_form in [
            ("assert x == y", "self.assertEquals(x, y)"),
            ("assert x == y, msg", "self.assertEquals(x, y, msg)"),
            ]:
        assert toggle_assert_style(assert_form) == method_form
        assert toggle_assert_style(method_form) == assert_form

def test_errors(invalid_syntax):
    assert toggle_assert_style(invalid_syntax) == invalid_syntax
