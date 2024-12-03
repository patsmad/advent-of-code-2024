import argparse
from get_input import get_input
import re

def day_num() -> int:
    return int(re.search(r'.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()

def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day)
    else:
        raw_input: str = """
        xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
        """.strip()
    input = raw_input.strip()

    # part 1
    values = re.findall(r'mul\([0-9]{1,3},[0-9]{1,3}\)', input)
    sum = 0
    for value in values:
        a, b = map(int, re.findall(r'mul\(([0-9]{1,3}),([0-9]{1,3})\)', value)[0])
        sum += a * b
    print(sum)

    # part 2
    values = re.findall(r'do\(\)|don\'t\(\)|mul\([0-9]{1,3},[0-9]{1,3}\)', input)
    sum = 0
    on = True
    for value in values:
        if value == 'do()':
            on = True
        elif value == 'don\'t()':
            on = False
        else:
            a, b = map(int, re.findall(r'mul\(([0-9]{1,3}),([0-9]{1,3})\)', value)[0])
            if on:
                sum += a * b
    print(sum)

if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
