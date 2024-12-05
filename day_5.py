import argparse
from get_input import get_input
import re
from typing import Dict, List

def day_num() -> int:
    return int(re.search(r'.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()

def check_order(order: List, invalid_rules: Dict) -> bool:
    invalid = set()
    for page in order:
        if page in invalid:
            return False
        invalid |= invalid_rules.get(page, set())
    return True

def get_idx(page: int, new_order: List, invalid_rules: Dict) -> int:
    for i, new_page in enumerate(new_order):
        if page in invalid_rules.get(new_page, set()):
            return i
    return len(new_order)

def reorder(order: List, invalid_rules: Dict) -> List:
    new_order = []
    for page in order:
        # Find index of first placed page that would cause the list to be invalid
        idx = get_idx(page, new_order, invalid_rules)
        # insert into the spot right before that page
        new_order = new_order[:idx] + [page] + new_order[idx:]
    return new_order

def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day)
    else:
        raw_input: str = """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
        """.strip()

    raw_rules, raw_orders = raw_input.strip().split('\n\n')
    rules = [tuple(map(int, a.strip().split('|'))) for a in raw_rules.strip().split('\n')]
    orders = [list(map(int, a.strip().split(','))) for a in raw_orders.strip().split('\n')]

    invalid_rules = {}
    for rule in rules:
        if rule[1] not in invalid_rules:
            invalid_rules[rule[1]] = set()
        invalid_rules[rule[1]] |= {rule[0]}

    # part 1
    s = 0
    for order in orders:
        if check_order(order, invalid_rules):
            s += order[len(order) // 2]
    print(s)

    # part 2
    s = 0
    for order in orders:
        if not check_order(order, invalid_rules):
            new_order = reorder(order, invalid_rules)
            s += new_order[len(new_order) // 2]
    print(s)

if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
