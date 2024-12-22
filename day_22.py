import argparse
from get_input import get_input
import re

def day_num() -> int:
    return int(re.search(r'.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()

def mix(num, other_num):
    return num ^ other_num

def prune(num):
    return num % 16777216

def evolve(num: int) -> int:
    num = prune(mix(num, num * 64))
    num = prune(mix(num, num // 32))
    return prune(mix(num, num * 2048))

def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day)
    else:
        raw_input: str = """
        1
        2
        3
        2024
        """.strip()
    nums = [int(a.strip()) for a in raw_input.strip().split('\n')]

    # part 1
    s = 0
    for num in nums:
        for _ in range(2000):
            num = evolve(num)
        s += num
    print(s)

    # part 2
    prices = {}
    for i, num in enumerate(nums):
        last_four = []
        curr_price = num % 10
        for _ in range(2000):
            num = evolve(num)
            new_price = num % 10
            delta = new_price - curr_price
            last_four.append(delta)
            if len(last_four) == 4:
                key = ''.join(map(str, last_four))
                if key not in prices:
                    prices[key] = {}
                if i not in prices[key]:
                    prices[key][i] = new_price
                last_four.pop(0)
            curr_price = new_price
    max_amount = 0
    for price in prices:
        amount = sum(prices[price].values())
        if amount > max_amount:
            max_amount = amount
    print(max_amount)

if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
