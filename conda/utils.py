


def iter_pairs(lst):
    assert isinstance(lst, list)
    for i, elem in enumerate(lst):
        try:
            next = lst[i + 1]
        except IndexError:
            next = None
        yield elem, next
