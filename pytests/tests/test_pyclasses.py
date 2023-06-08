import sys
from unittest import mock

import pytest
from pyo3_pytests import pyclasses


def test_empty_class_init(benchmark):
    benchmark(pyclasses.EmptyClass)


class EmptyClassPy:
    pass


def test_empty_class_init_py(benchmark):
    benchmark(EmptyClassPy)


def test_iter():
    i = pyclasses.PyClassIter()
    assert next(i) == 1
    assert next(i) == 2
    assert next(i) == 3
    assert next(i) == 4
    assert next(i) == 5

    with pytest.raises(StopIteration) as excinfo:
        next(i)
    assert excinfo.value.value == "Ended"


class AssertingSubClass(pyclasses.AssertingBaseClass):
    pass


def test_new_classmethod():
    # The `AssertingBaseClass` constructor errors if it is not passed the relevant subclass.
    _ = AssertingSubClass(expected_type=AssertingSubClass)
    with pytest.raises(ValueError):
        _ = AssertingSubClass(expected_type=str)


def test_del():
    d = pyclasses.PyClassDel()
    del d


@pytest.mark.skipif(sys.version_info < (3, 8), reason="requires python3.8 or higher")
def test_del_error():
    with mock.patch("sys.unraisablehook") as unraisablehook:
        d = pyclasses.PyClassDelError()
        del d
        assert unraisablehook.called
