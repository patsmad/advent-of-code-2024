from typing import List


def augment_array(array: List[int], max_num: int) -> List[int]:
    out = array.copy()
    for i in range(len(out)):
        out[i] += 1
        if out[i] != max_num + 1:
            return out
        out[i] = 0
    return [0 for _ in range(len(array))] + [1]

def permutations(size: int, max_num: int) -> List[List[int]]:
    arrays = [[0 for _ in range(size)]]
    for _ in range((max_num + 1)**size - 1):
        arrays.append(augment_array(arrays[-1], max_num))
    return arrays
