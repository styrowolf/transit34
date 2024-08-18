from itertools import islice


def query_transform(query: str) -> str:
    query_transformed = query.replace("i", "İ").replace("ı", "I").upper()
    return f"%{'%'.join(query_transformed.split())}%"


def is_depar_route(route_pattern_code: str):
    return route_pattern_code.split("_")[2] != "D0"


def batch(iterable, n=1):
    length = len(iterable)
    for ndx in range(0, length, n):
        yield iterable[ndx : min(ndx + n, length)]


def window(seq, n=2):
    "Returns a sliding window (of width n) over data from the iterable"
    "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result
