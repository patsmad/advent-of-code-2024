import argparse
from get_input import get_input
import re
from typing import Dict, List

def day_num() -> int:
    return int(re.search(r'.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()

# Slow, but there is a way whereby if a value is too large with operations left over you can eliminate
# all operations that share that prefix of operations ... not going to do it though, runs in <10 seconds and I
# can't be bothered.
def augment(line: List[int], num_ops: int) -> List[int]:
    for i in range(len(line)):
        line[i] += 1
        if line[i] != num_ops:
            return line
        line[i] = 0

operations = [
    lambda s, v: s + v,
    lambda s, v: s * v,
    lambda s, v: int(str(s) + str(v))
]

def test_operator(target: int, values: List[int], operator: List[int]):
    s = values[0]
    for o, v in zip(operator, values[1:]):
        s = operations[o](s, v)
    return s == target

def test_line(target: int, values: List[int], num_ops: int) -> bool:
    operator = [0 for _ in range(len(values) - 1)]
    for _ in range(num_ops**(len(values) - 1)):
        if test_operator(target, values, operator):
            return True
        operator = augment(operator, num_ops)
    return False


def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day)
    else:
        raw_input: str = """
        190: 10 19
        3267: 81 40 27
        83: 17 5
        156: 15 6
        7290: 6 8 6 15
        161011: 16 10 13
        192: 17 8 14
        21037: 9 7 18 13
        292: 11 6 16 20
        """.strip()
    input = []
    for line in raw_input.strip().split('\n'):
        key, values = line.strip().split(':')
        input.append((int(key.strip()), list(map(int, values.strip().split()))))

    # part 1
    s = 0
    for target, values in input:
        if test_line(target, values, 2):
            s += target
    print(s)

    # part 2
    s = 0
    for target, values in input:
        if test_line(target, values, 3):
            s += target
    print(s)

if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
