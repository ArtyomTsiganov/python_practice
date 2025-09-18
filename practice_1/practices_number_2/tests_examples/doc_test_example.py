# command to run: python -m doctest doc_test_example.py

def kth_stat(iterable, k):
    """Return the k-th smallest element of iterable.

    >>> kth_stat([3, 1, 2], 0)
    1
    >>> kth_stat([3, 1, 2], 1)
    2
    >>> kth_stat([4, 1, 2], 2)
    3
    >>> kth_stat([3, 1, 2], 3)
    Traceback (most recent call last):
        ...
    IndexError: list index out of range
    """
    a = list(iterable)
    a.sort()
    return a[k]