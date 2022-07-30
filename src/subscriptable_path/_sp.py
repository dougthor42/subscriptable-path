"""
"""
from pathlib import Path  # noqa: F401
from pathlib import PurePath
from pathlib import PurePosixPath  # noqa: F401
from pathlib import PureWindowsPath  # noqa: F401
from typing import Iterator
from typing import Union


def _del_slots(self: PurePath) -> None:
    """Delete the slots used by PurePath so that they are remade on-demand."""
    for slot in PurePath.__slots__:  # type: ignore[attr-defined]
        try:
            delattr(self, slot)
        except AttributeError:
            pass


def _make_path(self, new_parts) -> None:
    """
    Update this PurePath object and make it think it's a new path.
    """
    # Hack. We can't edit this path object directly, so we create a new one
    # and basically do what _from_parts does.
    new = self.__class__(*new_parts)
    # Need to clear out any existing slots so they get remade on-demand.
    _del_slots(self)
    # what cls._from_parts does:
    self._parts = new.parts
    self._drv = new._drv
    self._root = new._root


# methods defined in the same order as the docs.
# https://docs.python.org/3/reference/datamodel.html#emulating-container-types
def _len__(self) -> int:
    return len(self.parts)


def _length_hint__(self) -> int:
    return NotImplemented


def _getitem__(self, idx: Union[int, slice]) -> str:
    if not isinstance(idx, (int, slice)):
        raise TypeError(f"must be integer or slice, not {type(idx)}")

    if isinstance(idx, slice):
        p = self.__class__(*self.parts[idx])
        return str(p)

    return self.parts[idx]


def _setitem__(self, idx: int, value: str) -> None:
    """
    Replace a part of the path.

    Special case: setting index 0 preservies root and instead *inserts* the
    new value.

    >>> a = Path("/foo/bar")
    >>> a[0] = "baz"
    >>> a
    Path("/baz/foo/bar")
    """
    original_root = self.parts[0]
    new_parts = list(self.parts)
    new_parts[idx] = value

    # special case: setting index 0 *preserves* root.
    if idx == 0:
        new_parts.insert(0, original_root)

    _make_path(self, new_parts)


def _delitem__(self, idx: int) -> None:
    new_parts = list(self.parts)
    del new_parts[idx]

    _make_path(self, new_parts)


def _iter__(self) -> Iterator[str]:
    yield from self.parts


def _reversed__(self) -> None:
    """
    Reverse the path.

    If the path is absolute, root is preserved.
    """
    new_parts = list(self.parts)
    if self.is_absolute():
        original_root = new_parts.pop(0)

    new_parts.reverse()

    if self.is_absolute():
        new_parts.insert(0, original_root)

    _make_path(self, new_parts)


def _contains__(self, item: str) -> bool:
    return item in self.parts


PurePath.__len__ = _len__  # type: ignore[attr-defined]
PurePath.__length_hint__ = _length_hint__  # type: ignore[attr-defined]
PurePath.__getitem__ = _getitem__  # type: ignore[misc]
PurePath.__setitem__ = _setitem__  # type: ignore[index]
PurePath.__delitem__ = _delitem__  # type: ignore[attr-defined]
PurePath.__iter__ = _iter__  # type: ignore[attr-defined]
PurePath.__reversed__ = _reversed__  # type: ignore[attr-defined]
PurePath.__contains__ = _contains__  # type: ignore[operator]
