from typing import List, TypeVar

T = TypeVar("T")

def find(needle: T, haystack: List[T]) -> int:
    for i in range(len(haystack)):
        if needle == haystack[i]:
            return i
    raise ValueError(str(needle) + " is not in haystack")

find("hello", ["hello", "hi", "hey"])

find(3, [3,2,1])

find("hello", [3,2,1])