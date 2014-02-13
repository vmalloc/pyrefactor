# dictstyles

Quickly change dictionary styles:

```python
>>> from dictstyles.styles import toggle_style

>>> toggle_style("dict(a=1, b=2)")
{'a': 1, 'b': 2}
```

Also can be used from command-line:

```
$ echo "dict(a=1, b=2)" | toggle_dict_style
{'a': 1, 'b': 2}
```
