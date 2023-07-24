# Setup

1. clone the repo
2. run `poetry install`
3. run `poetry shell` 
4. run `python main.py`

# Destroy

You can just add `destroy` as an argument.

```
python main.py destroy
```

# Findings

You'll see that the explicitly defined `int` types are now `float` types.


```
  ╭──────────────────────────────── ! WARNING ! ─────────────────────────────────╮
    │                                                                              │
    │  value of test_value is 42.0                                                 │
    │  type of test_value is <class 'float'>                                       │
    │  expected type of test_value is int                                          │
    ╰──────────────────────────────────────────────────────────────────────────────╯
    ╭──────────────────────────────── ! WARNING ! ─────────────────────────────────╮
    │                                                                              │
    │  value of test_dictionary["test_int_value"] is 42.0                          │
    │  type of test_dictionary["test_int_value"] is <class 'float'>                │
    │  expected type of test_dictionary["test_int_value"] is int                   │
    ╰──────────────────────────────────────────────────────────────────────────────╯```