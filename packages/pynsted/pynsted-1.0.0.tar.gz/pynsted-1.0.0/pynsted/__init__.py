"""Getting nested values from dictionaries."""

import gc
from typing import Any, Protocol, TypeVar, cast, runtime_checkable

_PynstedT = TypeVar("_PynstedT")


def _pynsted_get(
    self: dict[Any, Any], path: list[Any], default: None | _PynstedT = None
) -> None | _PynstedT:
    """Get nested value from the dictionary.

    Access nested value in dictionary, given the path to it. If at some
    moment the path can no longer be followed, return default value.

    :param self: the instance of the dictionary
    :param path: the path to the value
    :param default: the default value if the path cannot be followed
    :returns: nested dictionary value or default value if the path
              cannot be followed
    """
    cur = self
    for key in path:
        if not isinstance(cur, dict) or key not in cur:
            return default
        cur = cur[key]
    return cast(None | _PynstedT, cur)


# Hackety-hack
_pynsted_dict = gc.get_referents(dict.__dict__)[0]
_pynsted_dict["getn"] = _pynsted_get


@runtime_checkable
class SupportsGetn(Protocol):  # pylint: disable=too-few-public-methods
    """Protocol for dictionaries with getn() method."""

    def getn(
        self, path: list[Any], default: None | _PynstedT = None
    ) -> None | _PynstedT:
        """Get nested value from the dictionary.

        Access nested value in dictionary, given the path to it. If at
        some moment the path can no longer be followed, return default
        value.

        :param self: the instance of the dictionary
        :param path: the path to the value
        :param default: the default value if the path cannot be followed
        :returns: nested dictionary value or default value if the path
                  cannot be followed
        """
