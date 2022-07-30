"""
"""
import types

import pytest

from subscriptable_path import Path as SPath
from subscriptable_path import PurePosixPath
from subscriptable_path import PureWindowsPath


#  @pytest.mark.parametrize("flavor", [PureWindowsPath, PurePosixPath])
@pytest.mark.parametrize(
    "flavor, path_str, idx, want",
    [
        (PurePosixPath, "/1/2/3/4/5/6/7", 0, "/"),
        (PurePosixPath, "/1/2/3/4/5/6/7", 1, "1"),
        (PurePosixPath, "/1/2/3/4/5/6/7", 3, "3"),
        (PurePosixPath, "/1/2/3/4/5/6/7", -1, "7"),
        (PurePosixPath, "/1/2/3/4/5/6/7", slice(1), "/"),
        (PurePosixPath, "/1/2/3/4/5/6/7", slice(3), "/1/2"),
        (PurePosixPath, "/1/2/3/4/5/6/7", slice(2, 4), "2/3"),
        (PurePosixPath, "/1/2/3/4/5/6/7", slice(1, 6, 2), "1/3/5"),
        (PureWindowsPath, "C:\\1\\2\\3", 0, "C:\\"),
        (PureWindowsPath, "C:/1/2/3", 0, "C:\\"),
        (PureWindowsPath, "C:/1/2/3", slice(1), "C:\\"),
        (PureWindowsPath, "C:/1/2/3", slice(3), "C:\\1\\2"),
    ],
)
def test__getitem__(flavor, path_str, idx, want):
    p = flavor(path_str)
    got = p[idx]
    assert got == want


@pytest.mark.parametrize(
    "flavor, path_str, want",
    [
        (PurePosixPath, "/", 1),
        (PurePosixPath, "/1", 2),
        (PurePosixPath, "/1/2/3/4/5/6/7", 8),
        (PureWindowsPath, "C:/1/2/3/4/5/6/7", 8),
        (PureWindowsPath, "C:\\1", 2),
        (PureWindowsPath, "C:\\", 1),
        (PureWindowsPath, "C:/", 1),
    ],
)
def test__len__(flavor, path_str, want):
    p = flavor(path_str)
    assert len(p) == want


#  def test__length_hint__(path_str, want):
#      pass


@pytest.mark.parametrize(
    "flavor, path_str, idx, new_val, want_str",
    [
        (PurePosixPath, "/1/2/3", 1, "a", "/a/2/3"),
        (PurePosixPath, "/1/2/3", 3, "a", "/1/2/a"),
        (PurePosixPath, "/1/2/3", -1, "a", "/1/2/a"),
        (PurePosixPath, "/1/2/3", 0, "a", "/a/1/2/3"),
        (PureWindowsPath, "C:\\1\\2\\3", 1, "a", "C:\\a\\2\\3"),
        (PureWindowsPath, "C:/1/2/3", 1, "a", "C:\\a\\2\\3"),
        (PureWindowsPath, "C:\\1\\2\\3", 3, "a", "C:\\1\\2\\a"),
        (PureWindowsPath, "C:\\1\\2\\3", -1, "a", "C:\\1\\2\\a"),
        (PureWindowsPath, "C:\\1\\2\\3", 0, "a", "C:\\a\\1\\2\\3"),
    ],
)
def test__setitem__(flavor, path_str, idx, new_val, want_str):
    p = flavor(path_str)
    p[idx] = new_val
    assert str(p) == want_str


def test__setitem__raises():
    p = SPath("/1/2/3")
    with pytest.raises(IndexError):
        p[4] = "foo"


@pytest.mark.parametrize(
    "flavor, path_str, idx, want_str",
    [
        (PurePosixPath, "/1/2/3", 1, "/2/3"),
        (PurePosixPath, "/1/2/3", 3, "/1/2"),
        (PurePosixPath, "/1/2/3", -1, "/1/2"),
        (PurePosixPath, "/1/2/3", 0, "1/2/3"),
        (PureWindowsPath, "C:/1/2/3", 0, "1\\2\\3"),
        (PureWindowsPath, "C:/1/2/3", 1, "C:\\2\\3"),
    ],
)
def test__delitem__(flavor, path_str, idx, want_str):
    p = flavor(path_str)
    del p[idx]
    assert str(p) == want_str


@pytest.mark.parametrize(
    "flavor, path_str, want",
    [
        (PurePosixPath, "/1/2/3", ["/", "1", "2", "3"]),
        (PurePosixPath, "1/2/3", ["1", "2", "3"]),
        (PureWindowsPath, "C:\\1\\2\\3", ["C:\\", "1", "2", "3"]),
        (PureWindowsPath, "1\\2\\3", ["1", "2", "3"]),
    ],
)
def test__iter__(path_str, flavor, want):
    spath = flavor(path_str)
    got = iter(spath)
    assert isinstance(got, types.GeneratorType)
    assert list(got) == want


@pytest.mark.parametrize(
    "flavor, path_str, want_str",
    [
        (PurePosixPath, "/1/2/3", "/3/2/1"),
        (PurePosixPath, "1/2/3", "3/2/1"),
        (PureWindowsPath, "C:/1/2/3", r"C:\3\2\1"),
        (PureWindowsPath, "C:\\1\\2\\3", "C:\\3\\2\\1"),
        (PureWindowsPath, "1\\2\\3", "3\\2\\1"),
    ],
)
def test__reversed__(flavor, path_str, want_str):
    spath = flavor(path_str)
    reversed(spath)
    assert str(spath) == want_str


@pytest.mark.parametrize(
    "flavor, path_str, elem, want",
    [
        (PurePosixPath, "/1/2/3", "2", True),
        (PurePosixPath, "/1/2/3", "4", False),
        (PureWindowsPath, "C:\\1\\2\\3", "2", True),
        (PureWindowsPath, "C:\\1\\2\\3", "4", False),
        (PureWindowsPath, "C:/1/2/3", "4", False),
    ],
)
def test__contains__(flavor, path_str, elem, want):
    p = flavor(path_str)
    got = elem in p
    assert got is want
