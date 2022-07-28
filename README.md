# Subscriptable Path

A subclass of Python's pathlib objects that allow subscripting/indexing.

I was recently working with some `pathlib.Path` stuff and found that I
wanted to get the `n`th folder in a deep path. Naively, I tried:

```python
>>> from pathlib import Path
>>> a = Path("/foo/bar/baz/a/b/c/d.txt")
>>> a[4]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'PosixPath' object is not subscriptable
```

Harrumph.

This project aims to make such a thing possible:

```python
>>> from subscriptable_path import SubscriptablePath as SPath
>>> a = SPath("/foo/bar/baz/a/b/c/d.txt")
>>> a[4]
"a"
>>> a[-2]
"c"
>>> a[2:4]  # Slices
"bar/baz"
>>> del a[2]
>>> a
SubscriptablePath("/foo/baz/a/b/c/d.txt")  # note "baz" is missing
```

Basically: almost anything you can do on a list, you can do on a `SubscriptablePath`.
At least that's the goal...


## Installation and Usage


## Development

1.  Clone the repo: `git clone https://github.com/dougthor42/subscriptable-path`
2.  Move into that dir: `cd subscriptable-path`
3.  Create a virtual environment: `python -m venv .venv`
4.  Activate it: `. .venv/bin/activate`
5.  Install python packages:
    1.  `pip install -U pip setuptools wheel`
    2.  `pip install -r requirements.txt -r requirements-dev.txt`
    3.  `pip install -e .`
6.  Run tests to verify: `pytest`
7.  Ready to develop


## Changelog

See [CHANGELOG.md](./CHANGELOG.md).
