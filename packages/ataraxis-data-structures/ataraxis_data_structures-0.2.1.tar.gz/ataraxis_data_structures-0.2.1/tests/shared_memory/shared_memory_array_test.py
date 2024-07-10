import pytest
import re
import textwrap
import numpy as np
from multiprocessing import Process
from ataraxis_data_structures import SharedMemoryArray


@pytest.fixture
def sample_array():
    return np.array([1, 2, 3, 4, 5], dtype=np.int32)


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


def test_create_array(sample_array):
    """Verifies the functionality of the SharedMemoryArray class create_array() method.

    Tested configurations:
        - 0: Creating a SharedMemoryArray with a valid numpy array
        - 1: Verifying the name, shape, datatype, and connection status of the created array
        - 2: Verifying the data integrity of the created array
    """
    sma = SharedMemoryArray.create_array("test_array", sample_array)
    assert sma.name == "test_array"
    assert sma.shape == sample_array.shape
    assert sma.datatype == sample_array.dtype
    assert sma.is_connected
    np.testing.assert_array_equal(sma.read_data((0, 5)), sample_array)


def test_repr(sample_array):
    """Verifies the functionality of the SharedMemoryArray class __repr__() method.

    Tested configurations:
        - 0: Creating a SharedMemoryArray and verifying its string representation
    """
    sma = SharedMemoryArray.create_array("test_repr", sample_array)
    expected_repr = (
        f"SharedMemoryArray(name='test_repr', shape={sample_array.shape}, "
        f"datatype={sample_array.dtype}, connected=True)"
    )
    assert repr(sma) == expected_repr


@pytest.mark.parametrize(
    "buffer_name, index, convert, expected",
    [
        ('test_read_1', 0, True, 1),
        ('test_read_2', -1, True, 5),
        ('test_read_3', (0, 3), True, [1, 2, 3]),
        ('test_read_4', (1,), True, [2, 3, 4, 5]),
        ('test_read_5', (-3, -1), True, [3, 4]),
        ('test_read_6', (0, 1), True, 1),
        ('test_read_7', 0, False, np.int32(1)),
        ('test_read_8', -1, False, np.int32(5)),
    ],
)
def test_read_data(sample_array, buffer_name, index, convert, expected):
    """Verifies the functionality of the SharedMemoryArray class read_data() method.

    Notes:
        Uses separate buffer names to prevent name collisions when tests are spread over multiple cores during
        pytest-xdist runtime.

    Tested configurations:
        - 0 Reading data at index 0
        - 1 Reading data at index -1 (last element)
        - 2 Reading data using a closed-ended slice (0, 3)
        - 3 Reading data using an open-ended slice (1,)
        - 4 Reading data using negative indices for both start and stop (-3, -1)
        - 5 Reading data using a slice (0, 1), expecting the return to be a scalar and not a list.
    """
    sma = SharedMemoryArray.create_array(buffer_name, sample_array)
    result = sma.read_data(index=index, convert_output=convert)
    if isinstance(result, np.ndarray):
        np.testing.assert_array_equal(result, expected)
    else:
        assert result == expected


@pytest.mark.parametrize(
    "buffer_name, index, data",
    [
        ('test_write_1', 0, 10),
        ('test_write_2', -1, 50),
        ('test_write_3', (0, 3), [10, 20, 30]),
        ('test_write_4', (1,), [20, 30, 40, 50]),
        ('test_write_5', (-3, -1), [30, 40]),
    ],
)
def test_write_data(sample_array, buffer_name, index, data):
    """Verifies the functionality of the SharedMemoryArray class write_data() method.

    Notes:
        Uses separate buffer names to prevent name collisions when tests are spread over multiple cores during
        pytest-xdist runtime.

    Tested configurations:
        - 0: Writing a single value to index 0
        - 1: Writing a single value to index -1 (last element)
        - 2: Writing multiple values using a closed-ended slice (0, 3)
        - 3: Writing multiple values using an open-ended slice (1,)
        - 4: Writing multiple values using negative indices for both start and stop (-3, -1)
    """
    sma = SharedMemoryArray.create_array(buffer_name, sample_array)
    sma.write_data(index, data)
    result = sma.read_data(index)
    if isinstance(data, list):
        np.testing.assert_array_equal(result, data)
    else:
        assert result == data


def test_disconnect_connect(sample_array):
    """Verifies the functionality of the SharedMemoryArray class disconnect() and connect() methods.

    Tested configurations:
        - 0: Disconnecting from a connected SharedMemoryArray
        - 1: Reconnecting to a disconnected SharedMemoryArray
        - 2: Verifying data integrity after reconnection
    """
    sma = SharedMemoryArray.create_array("test_disconnect", sample_array)
    sma.disconnect()
    assert not sma.is_connected
    sma.connect()
    assert sma.is_connected
    np.testing.assert_array_equal(sma.read_data((0, 5)), sample_array)


def test_create_array_error():
    """Verifies error handling in the SharedMemoryArray class create_array() method.

    Tested configurations:
        - 0: Attempting to create an array with an invalid prototype (list instead of numpy array)
        - 1: Attempting to create an array with a multi-dimensional numpy array
        - 2: Attempting to create an array with a name that already exists
    """
    # Test with invalid prototype type
    message = (
        f"Invalid 'prototype' argument type encountered when creating SharedMemoryArray object 'test_error'. "
        f"Expected a flat (one-dimensional) numpy ndarray but instead encountered {type([1, 2, 3]).__name__}."
    )
    with pytest.raises(TypeError, match=error_format(message)):
        # noinspection PyTypeChecker
        SharedMemoryArray.create_array(name="test_error", prototype=[1, 2, 3])

    # Test with multidimensional array
    multi_dim_array = np.array([[1, 2], [3, 4]])
    message = (
        f"Invalid 'prototype' array shape encountered when creating SharedMemoryArray object 'test_error_2'. "
        f"Expected a flat (one-dimensional) numpy ndarray but instead encountered prototype with shape "
        f"{multi_dim_array.shape} and dimensions number {multi_dim_array.ndim}."
    )
    with pytest.raises(ValueError, match=error_format(message)):
        SharedMemoryArray.create_array(name="test_error_2", prototype=multi_dim_array)

    # Test with existing name
    SharedMemoryArray.create_array(name="existing_array", prototype=np.array([1, 2, 3]))
    message = (
        f"Unable to create SharedMemoryArray object using name 'existing_array', as object with this name already "
        f"exists. This is likely due to calling create_array() method from a child process. "
        f"Use connect() method to connect to the SharedMemoryArray from a child process."
    )
    with pytest.raises(FileExistsError, match=error_format(message)):
        SharedMemoryArray.create_array(name="existing_array", prototype=np.array([4, 5, 6]))


def test_read_data_error(sample_array):
    """Verifies error handling in the SharedMemoryArray class read_data() method.

    Tested configurations:
        - 0: Attempting to read with an index greater than array length
        - 1: Attempting to read with a negative index that translates to a position before the array start
        - 2: Attempting to read with a stop index greater than array length
        - 3: Attempting to read with a start index greater than stop index
        - 4: Attempting to read from a disconnected array
        - 5: Attempting to read with an invalid index type
    """
    sma = SharedMemoryArray.create_array("test_read_error", sample_array)

    # Test index out of bounds (positive)
    message = (
        f"Unable to retrieve the data from test_read_error SharedMemoryArray class instance using start index "
        f"5. The index is outside the valid start index range (0:4)."
    )
    with pytest.raises(IndexError, match=error_format(message)):
        sma.read_data(5)

    # Test index out of bounds (negative)
    message = (
        f"Unable to retrieve the data from test_read_error SharedMemoryArray class instance using start index "
        f"-1. The index is outside the valid start index range (0:4)."
    )
    with pytest.raises(IndexError, match=error_format(message)):
        sma.read_data(-6)

    # Test stop index out of bounds
    message = (
        f"Unable to retrieve the data from test_read_error SharedMemoryArray class instance using stop index "
        f"6. The index is outside the valid stop index range (1:5)."
    )
    with pytest.raises(IndexError, match=error_format(message)):
        sma.read_data((0, 6))

    # Test start index greater than stop index
    message = (
        f"Invalid pair of slice indices encountered when manipulating data of the test_read_error "
        f"SharedMemoryArray class instance. After converting the indices to positive numbers, the start "
        f"index (3) is greater than the end index (2), which is not allowed."
    )
    with pytest.raises(ValueError, match=error_format(message)):
        sma.read_data((3, 2))

    # Test reading from disconnected array
    sma.disconnect()
    message = (
        f"Unable to access the data stored in the test_read_error SharedMemoryArray instance, as the class is not "
        f"connected to the shared memory buffer. Use connect() method prior to calling other class methods."
    )
    with pytest.raises(RuntimeError, match=error_format(message)):
        sma.read_data(0)

    # Test invalid index type
    sma.connect()
    message = (
        f"Unable to read data from test_read_error SharedMemoryArray class instance. Expected an integer index or "
        f"a tuple of two integers, but encountered 'invalid' of type {type('invalid').__name__} instead."
    )
    with pytest.raises(ValueError, match=error_format(message)):
        sma.read_data('invalid')


@pytest.mark.parametrize(
    "index, data, error_type, error_message",
    [
        (5, 10, IndexError, "The index is outside the valid start index range"),
        (-6, 10, IndexError, "The index is outside the valid start index range"),
        ((0, 6), [1, 2, 3, 4, 5, 6], IndexError, "The index is outside the valid stop index range"),
        ((3, 2), [1, 2], ValueError, "the start index .* is greater than the end index"),
        (0, "invalid_data", ValueError, "Unable write data"),
    ],
)
def test_write_data_error(sample_array, index, data, error_type, error_message):
    """Verifies error handling in the SharedMemoryArray class write_data() method.

    Tested configurations:
        - 0: Attempting to write with an index greater than array length
        - 1: Attempting to write with a negative index that translates to a position before the array start
        - 2: Attempting to write with a stop index greater than array length
        - 3: Attempting to write with a start index greater than stop index
        - 4: Attempting to write data of an invalid type
    """
    sma = SharedMemoryArray.create_array("test_write_error", sample_array)
    with pytest.raises(error_type, match=error_message):
        sma.write_data(index, data)


def read_write_worker(name):
    """This worker is used to verify that SharedMemoryArray class can be used from multiple processes as intended.

    To do so, it has to be defined outside the main test scope (to deal with how multiprocessing distributes the data
    across workers).

    Specifically, it is used as part of the cross_process_read_write() test task.
    """
    sma = SharedMemoryArray(name, (5,), np.dtype(np.int32), None)
    sma.connect()
    sma.write_data(2, 42)
    assert sma.read_data(2) == 42
    sma.disconnect()


def concurrent_worker(name, index):
    """This worker is used to verify that SharedMemoryArray is process-safe (when used with default locking flags).

    To do so, it has to be defined outside the main test scope (to deal with how multiprocessing distributes the data
    across workers).

    Specifically, it is used as part of the cross_process_concurrent_access() test task.
    """
    sma = SharedMemoryArray(name, (5,), np.dtype(np.int32), None)
    sma.connect()
    for _ in range(100):
        value = sma.read_data(index)
        sma.write_data(index, value + 1)
    sma.disconnect()


@pytest.mark.loadgroup("cross_process")
def test_cross_process_read_write():
    """Verifies the ability of the SharedMemoryArray class to share data across processes.

    Tested configurations:
        - 0: Writing data from a child process
        - 1: Reading the written data from the parent process
    """
    sma = SharedMemoryArray.create_array("test_cross_process", np.array([1, 2, 3, 4, 5], dtype=np.int32))
    try:
        p = Process(target=read_write_worker, args=(sma.name,))
        p.start()
        p.join()
        assert sma.read_data(2) == 42
    finally:
        sma.disconnect()
        # Clean up the shared memory
        import multiprocessing.shared_memory
        try:
            multiprocessing.shared_memory.SharedMemory(name=sma.name).unlink()
        except FileNotFoundError:
            pass  # The shared memory may already be cleaned up


@pytest.mark.loadgroup("cross_process")
def test_cross_process_concurrent_access():
    """Verifies the ability of the SharedMemoryArray class to handle concurrent access from multiple processes.

    Tested configurations:
        - 0: Multiple processes (5) incrementing values in the shared array concurrently
        - 1: Verifying the final value of each array element after concurrent incrementing
    """

    sma = SharedMemoryArray.create_array("test_concurrent", np.zeros(5, dtype=np.int32))
    processes = [Process(target=concurrent_worker, args=(sma.name, i)) for i in range(5)]
    for p in processes:
        p.start()
    for p in processes:
        p.join()

    assert np.all(sma.read_data((0, 5)) == 100)
