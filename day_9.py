import argparse
from get_input import get_input
import re

def day_num() -> int:
    return int(re.search(r'.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()


def get_check_sum_input(input):
    check_sum_input = []
    idx = 0
    while idx < len(input):
        check_sum_input.append((idx // 2, input[idx]))
        check_sum_input.append((-1, input[idx + 1]))
        idx += 2
    return check_sum_input

def part_1_fill(check_sum_input):
    filled_input = [check_sum_input[0]]
    idx = 1
    rev_idx = len(check_sum_input) - 2
    while rev_idx > idx:
        if check_sum_input[idx][1] < check_sum_input[rev_idx][1]:
            filled_input.append((check_sum_input[rev_idx][0], check_sum_input[idx][1]))
            check_sum_input[rev_idx] = (check_sum_input[rev_idx][0], check_sum_input[rev_idx][1] - check_sum_input[idx][1])
            filled_input.append(check_sum_input[idx + 1])
            idx += 2
        elif check_sum_input[idx][1] > check_sum_input[rev_idx][1]:
            filled_input.append(check_sum_input[rev_idx])
            check_sum_input[idx] = (check_sum_input[idx][0], check_sum_input[idx][1] - check_sum_input[rev_idx][1])
            rev_idx -= 2
        else:
            filled_input.append(check_sum_input[rev_idx])
            filled_input.append(check_sum_input[idx + 1])
            idx += 2
            rev_idx -= 2
    return filled_input


def part_2_fill(check_sum_input):
    filled_input = [check_sum_input[0]]
    idx = 1
    moved_idx = {0}
    while idx < len(check_sum_input) - 1:
        gap_size = check_sum_input[idx][1]
        rev_idx = len(check_sum_input) - 2
        while rev_idx >= 0 and gap_size > 0:
            if check_sum_input[rev_idx][0] not in moved_idx and check_sum_input[rev_idx][1] <= gap_size:
                gap_size -= check_sum_input[rev_idx][1]
                filled_input.append(check_sum_input[rev_idx])
                moved_idx |= {check_sum_input[rev_idx][0]}
            rev_idx -= 2
        if gap_size > 0:
            filled_input.append((-1, gap_size))
        if check_sum_input[idx + 1][0] not in moved_idx:
            filled_input.append(check_sum_input[idx + 1])
            moved_idx |= {check_sum_input[idx + 1][0]}
        else:
            filled_input.append((-1, check_sum_input[idx + 1][1]))
        idx += 2
    return filled_input


def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day)
    else:
        raw_input: str = """
        2333133121414131402
        """.strip()

    # part 1
    input = list(map(int, raw_input.strip())) + [0]
    check_sum_input = get_check_sum_input(input)
    filled_input = part_1_fill(check_sum_input)
    check_sum = 0
    idx = 0
    for i in filled_input:
        for j in range(i[1]):
            check_sum += idx * i[0]
            idx += 1
    print(check_sum)

    # part 2
    check_sum_input = get_check_sum_input(input)
    filled_input = part_2_fill(check_sum_input)
    check_sum = 0
    idx = 0
    for i in filled_input:
        for j in range(i[1]):
            if i[0] > 0:
                check_sum += idx * i[0]
            idx += 1
    print(check_sum)


if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
