"""Contains tests for functions stored in the standalone_methods package."""

import pytest
import numpy as np
from typing import Any
from ataraxis_data_structures.standalone_methods import (
    ensure_list,
    chunk_iterable,
    check_condition,
    find_closest_indices,
    find_event_boundaries,
    compare_nested_tuples,
)


def error_format(message: str) -> str:
    """Formats the input message to match the default Console format and escapes it using re, so that it can be used to
    verify raised exceptions.

    This method is used to set up pytest 'match' clauses to verify raised exceptions.

    Args:
        message: The message to format and escape, according to standard Ataraxis testing parameters.

    Returns:
        Formatted and escape message that can be used as the 'match' argument of pytest.raises() method.
    """
    return re.escape(textwrap.fill(message, width=120, break_long_words=False, break_on_hyphens=False))


@pytest.mark.parametrize(
    "input_item, expected",
    [
        ([1, 2, 3], [1, 2, 3]),
        ((1, 2, 3), [1, 2, 3]),
        ({1, 2, 3}, [1, 2, 3]),
        (np.array([1, 2, 3]), [1, 2, 3]),
        (1, [1]),
        (1.0, [1.0]),
        ("a", ["a"]),
        (True, [True]),
        (None, [None]),
        (np.int32(1), [1]),
    ],
)
def test_ensure_list(input_item: Any, expected: list) -> None:
    """Verifies the functioning of the ensure_list() method for all supported scenarios.

    Tests the following inputs:
        - 0 lists
        - 1 tuples
        - 2 sets
        - 3 numpy arrays
        - 4 ints
        - 5 floats
        - 6 strings
        - 7 bools
        - 8 Nones
        - 9 Numpy scalars
    """
    assert ensure_list(input_item) == expected


def test_ensure_list_error() -> None:
    """Verifies that ensure_list() correctly handles unsupported input types."""
    with pytest.raises(TypeError, match="Unable to convert input item to a Python list"):
        # noinspection PyTypeChecker
        ensure_list(object())


@pytest.mark.parametrize(
    "iterable, chunk_size, expected",
    [
        ([1, 2, 3, 4, 5], 2, [(1, 2), (3, 4), (5,)]),
        (np.array([1, 2, 3, 4, 5]), 2, [np.array([1, 2]), np.array([3, 4]), np.array([5])]),
        ((1, 2, 3, 4, 5), 3, [(1, 2, 3), (4, 5)]),
    ],
)
def test_chunk_iterable(iterable: Any, chunk_size: int, expected: list) -> None:
    """Verifies the functioning of the chunk_iterable() method for various input types and chunk sizes.

    Tests the following scenarios:
        - 0 List input with even chunks and a remainder
        - 1 NumPy array input with even chunks and a remainder
        - 2 Tuple input with uneven chunks
    """
    result = list(chunk_iterable(iterable, chunk_size))
    assert len(result) == len(expected)
    for r, e in zip(result, expected):
        if isinstance(r, np.ndarray):
            assert np.array_equal(r, e)
        else:
            assert r == e


def test_chunk_iterable_error() -> None:
    """Verifies that chunk_iterable() correctly handles unsupported input types."""
    with pytest.raises(TypeError, match="Unsupported iterable type encountered when chunking iterable"):
        list(chunk_iterable(1, 2))


@pytest.mark.parametrize(
    "checked_value, condition_value, condition_operator, expected",
    [
        (5, 3, ">", True),
        (5, 3, "<", False),
        (5, 5, ">=", True),
        (5, 5, "<=", True),
        (5, 5, "==", True),
        (5, 3, "!=", True),
        ([1, 2, 3], 2, ">", (False, False, True)),
        ([1, 2, 3], 2, "<", (True, False, False)),
        ([1, 2, 3], 2, ">=", (False, True, True)),
        ([1, 2, 3], 2, "<=", (True, True, False)),
        ([1, 2, 3], 2, "==", (False, True, False)),
        ([1, 2, 3], 2, "!=", (True, False, True)),
        (np.array([1, 2, 3]), 2, ">", np.array([False, False, True])),
        (np.array([1, 2, 3]), 2, "<", np.array([True, False, False])),
        (np.array([1, 2, 3]), 2, ">=", np.array([False, True, True])),
        (np.array([1, 2, 3]), 2, "<=", np.array([True, True, False])),
        (np.array([1, 2, 3]), 2, "==", np.array([False, True, False])),
        (np.array([1, 2, 3]), 2, "!=", np.array([True, False, True])),
        (np.int32(5), 3, ">", np.bool_(True)),
        (np.int32(5), 3, "<", np.bool_(False)),
        (np.int32(5), 5, ">=", np.bool_(True)),
        (np.int32(5), 5, "<=", np.bool_(True)),
        (np.int32(5), 5, "==", np.bool_(True)),
        (np.int32(5), 3, "!=", np.bool_(True)),
    ],
)
def test_check_condition(checked_value: Any, condition_value: Any, condition_operator: str, expected: Any) -> None:
    """Verifies the functioning of the check_condition() method for all supported operators and various input types.

    Tests the following scenarios:
        - 0-5: Python scalar comparisons with all operators (>, <, >=, <=, ==, !=)
        - 6-11: List comparisons with all operators
        - 12-17: NumPy array comparisons with all operators
        - 18-23: NumPy scalar comparisons with all operators

    For each input type (Python scalar, list, NumPy array, NumPy scalar), all six supported operators are tested:
    '>', '<', '>=', '<=', '==', '!='.
    """
    # noinspection PyTypeChecker
    result = check_condition(checked_value, condition_value, condition_operator)
    if isinstance(result, np.ndarray):
        assert np.array_equal(result, expected)
    else:
        assert result == expected


def test_check_condition_error() -> None:
    """Verifies that check_condition() correctly handles invalid operators and unsupported input types."""
    with pytest.raises(KeyError, match="Unsupported operator symbol"):
        # noinspection PyTypeChecker
        check_condition(1, 1, "invalid")

    with pytest.raises(TypeError, match="Unsupported checked_value"):
        # noinspection PyTypeChecker
        check_condition(object(), 1, ">")


@pytest.mark.parametrize(
    "target_array, source_array, expected",
    [
        ([1, 5, 10], [2, 4, 6, 8], (0, 1, 3)),
        (np.array([1, 5, 10]), np.array([2, 4, 6, 8]), np.array([0, 1, 3])),
    ],
)
def test_find_closest_indices(target_array: Any, source_array: Any, expected: Any) -> None:
    """Verifies the functioning of the find_closest_indices() method for list and NumPy array inputs.

    Tests the following scenarios:
        - 0 List inputs
        - 1 NumPy array inputs
    """
    result = find_closest_indices(target_array, source_array)
    if isinstance(result, np.ndarray):
        assert np.array_equal(result, expected)
    else:
        assert result == expected


@pytest.mark.parametrize(
    "trace, make_offsets_exclusive, allow_no_events, expected",
    [
        ([0, 1, 1, 0, 1, 1, 1, 0], True, True, ((1, 3), (4, 7))),
        ([0, 1, 1, 0, 1, 1, 1, 0], False, True, ((1, 2), (4, 6))),
        ([0, 0, 0], True, True, ()),
    ],
)
def test_find_event_boundaries(
        trace: Any, make_offsets_exclusive: bool, allow_no_events: bool, expected: tuple
) -> None:
    """Verifies the functioning of the find_event_boundaries() method for various input scenarios.

    Tests the following scenarios:
        - 0 Multiple events with exclusive offsets
        - 1 Multiple events with non-exclusive offsets
        - 2 No events, allowed
    """
    result = find_event_boundaries(
        trace, make_offsets_exclusive=make_offsets_exclusive, allow_no_events=allow_no_events
    )
    assert result == expected


def test_find_event_boundaries_error() -> None:
    """Verifies that find_event_boundaries() correctly handles invalid inputs and disallowed no-event scenarios."""
    with pytest.raises(ValueError, match="Unsupported NumPy array 'trace' input detected"):
        find_event_boundaries(np.array([[1, 2], [3, 4]]))

    with pytest.raises(RuntimeError, match="Unable to find any event boundaries"):
        find_event_boundaries([0, 0, 0], allow_no_events=False)


@pytest.mark.parametrize(
    "x, y, expected",
    [
        (((1, 2), (3, 4)), ((1, 2), (3, 4)), True),
        (((1, 2), (3, 4)), ((1, 2), (3, 5)), False),
        ((("a", "b"), ("c",)), (("a", "b"), ("c",)), True),
        ((("a", "b"), ("c",)), (("a", "b"), ("d",)), False),
    ],
)
def test_compare_nested_tuples(x: tuple, y: tuple, expected: bool) -> None:
    """Verifies the functioning of the compare_nested_tuples() method for various nested tuple scenarios.

    Tests the following scenarios:
        - 0 Identical nested tuples with numbers
        - 1 Different nested tuples with numbers
        - 2 Identical nested tuples with strings and different inner tuple lengths
        - 3 Different nested tuples with strings and different inner tuple lengths
    """
    assert compare_nested_tuples(x, y) == expected


def test_compare_nested_tuples_error() -> None:
    """Verifies that compare_nested_tuples() correctly handles non-tuple inputs."""
    with pytest.raises(TypeError, match="Unsupported type encountered when comparing tuples"):
        # noinspection PyTypeChecker
        compare_nested_tuples([1, 2], (1, 2))
