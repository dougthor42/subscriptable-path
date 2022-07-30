# Subscriptable Path

A subclass of Python's pathlib objects that allow subscripting/indexing.

I was recently working with some `pathlib.Path` stuff and found that I
wanted to get the `n`th folder in a deep path. Naively, I tried:

```pycon
>>> from pathlib import Path
>>> a = Path("/foo/bar/baz/a/b/c/d.txt")
>>> a[4]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'PosixPath' object is not subscriptable
```

Harrumph.

This project aims to make such a thing possible. See [Usage](#usage) for details.


## Installation

This is a pure python package with no dependencies. Installing is easy:

```
pip install subscriptable_path
```


## Usage

> **Note:** Initial versions modify `pathlib.PurePath` directly, as those classes
> are a bit of a pain to subclass (because of tricks with `__new__`). This means
> that importing this module will affect every usage of `pathlib.PurePath`.
> Future work will adjust this API so that you can use `pathlib.PurePath` and
> `SubscriptablePath` simultaneously.
>
> The goal is to create a SubscriptablePath object that can be imported and
> replace the `pathlib.Path` object or can be used alongside. Eg:
>
> ```python
> from subscribtable_path import SubscriptablePath as Path  # drop-in replacement
> from subscriptable_path import SubscriptablePath as SPath  # use alongside
> ```

It's easiest to show usage with examples:

```pycon
>>> from subscriptable_path import Path

# Instantiate a Path object, just like `pathlib.Path`:
>>> path = Path("/mnt/foo/bar/1/2/3")

# Get a component of the path:
>>> path[2]
"foo"
>>> path[0]
"/"
>>> path[-1]
"3"

# Slices are also supported for __getitem__
>>> path[1:3]
"mnt/foo"

# Check the path length:
>>> len(path)
7

# Adjust a particular component, modifying the object
>>> path[2] = "hello"
>>> path
Path("/mnt/hello/bar/1/2/3")

# Delete a part of the path, modifying the object
>>> del path[2]
>>> path
Path("/mnt/bar/1/2/3")

# loop through the items in the path
>>> for name in path:
...     print(name)
...
"/"
"mnt"
"bar"
"1"
"2"
"3"

# Reverse the path:
# Note that if the path is absolute, the root is kept.
>>> reversed(path)
>>> path
Path("/3/2/1/bar/mnt")

>>> rel_path = Path("1/2/3")
>>> reversed(rel_path)
>>> rel_path
Path("3/2/1")

# And check if an item is in the path:
>>> "foo" in path
False
>>> "bar" in path
True
>>> "ba" in path
False
```


## Development

1.  Clone the repo: `git clone https://github.com/dougthor42/subscriptable-path`
2.  Move into that dir: `cd subscriptable-path`
3.  Create a virtual environment: `python -m venv .venv`
4.  Activate it: `. .venv/bin/activate`
5.  Install python packages:
    1.  `pip install -U pip setuptools wheel`
    2.  `pip install -r requirements-dev.txt`
    3.  `pip install -e .`
6.  Run tests to verify: `pytest`
7.  Install pre-commit hooks: `pre-commit install`
7.  Ready to develop


### Deployment

> TODO: Move to fully automated deployment with GitHub Actions.

1.  Update the version in `pyproject.toml`
2.  Create a new git tag: `git tag v<version>`.
3.  `python -m build`
4.  pip install twine
5.  twine upload dist/*


## Changelog

See [CHANGELOG.md](./CHANGELOG.md).
