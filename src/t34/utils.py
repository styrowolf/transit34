from itertools import islice
import functools

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

def sort_vehicle_door_codes(vehicles: list[str]) -> list[str]:
    return sorted(vehicles, key=functools.cmp_to_key(compare_vehicle_door_codes))

def compare_vehicle_door_codes(a: str, b: str):
    def get_first_numeric_index(s: str):
        for i, c in enumerate(s):
            if c.isnumeric():
                return i
        return len(s)

    a_index = get_first_numeric_index(a)
    b_index = get_first_numeric_index(b)
    a_number = int(a[a_index:])
    b_number = int(b[b_index:])
    a_str = a[:a_index]
    b_str = b[:b_index]

    def compare_strs():
        if a_str < b_str:
            return -1
        if a_str > b_str:
            return 1
        return 0
    
    str_cmp = compare_strs()
    if str_cmp != 0:
        return str_cmp
    else:
        return a_number - b_number