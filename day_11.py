import argparse
from get_input import get_input
import re
from typing import Dict, List

def day_num() -> int:
    return int(re.search(r'.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()

def apply_rule(num: int) -> List[int]:
    if num == 0:
        return [1]
    if len(str(num)) % 2 == 0:
        value = str(num)
        s1, s2 = value[:len(value) // 2], value[len(value) // 2:]
        return [int(s1), int(s2)]
    else:
        return [num * 2024]

def apply_rules_to_vec(vec: List[int]) -> List[int]:
    return [new_num for num in vec for new_num in apply_rule(num)]

def apply_rules_to_dict(num_dict: Dict[int, int]) -> Dict[int, int]:
    new_dict = {}
    for num in num_dict:
        count = num_dict[num]
        new_nums = apply_rule(num)
        for new_num in new_nums:
            if new_num not in new_dict:
                new_dict[new_num] = 0
            new_dict[new_num] += count
    return new_dict

def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day)
    else:
        raw_input: str = """
        125 17
        """.strip()
    vec = list(map(int, raw_input.strip().split(' ')))
    count = {}
    for num in vec:
        if num not in count:
            count[num] = 0
        count[num] += 1

    # part 1
    for _ in range(25):
        count = apply_rules_to_dict(count)
    print(sum(count.values()))

    # part 2
    for i in range(50):
        count = apply_rules_to_dict(count)
    print(sum(count.values()))

if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
