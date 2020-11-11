def find(needle, haystack):
    for i in range(len(haystack)):
        if needle == haystack[i]:
            return i
    raise ValueError(str(needle) + " is not in haystack")