import argparse
from get_input import get_input
import re
from typing import List

def day_num() -> int:
    return int(re.search(r'.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()

class Game:
    def __init__(self, x1, x2, y1, y2, tx, ty) -> None:
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.tx = tx
        self.ty = ty

    def get_p1(self):
        return (self.ty * self.x2 - self.tx * self.y2) / (self.y1 * self.x2 - self.y2 * self.x1)

    def get_presses(self):
        p1 = self.get_p1()
        return p1, (self.tx - p1 * self.x1) / self.x2

    def __str__(self):
        return f'x1={self.x1}, x2={self.x2}, y1={self.y1}, y2={self.y2}, tx={self.tx}, ty={self.ty}'

def process_input(raw_input: str) -> List[Game]:
    out = []
    lines = raw_input.strip().split('\n')
    for i in range(0, len(lines), 4):
        x1, y1 = map(lambda x: int(x.split('+')[-1]), lines[i].strip().split(': ')[-1].split(', '))
        x2, y2 = map(lambda x: int(x.split('+')[-1]), lines[i + 1].strip().split(': ')[-1].split(', '))
        tx, ty = map(lambda x: int(x.split('=')[-1]), lines[i + 2].strip().split(': ')[-1].split(', '))
        out.append(Game(x1, x2, y1, y2, tx, ty))
    return out

def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day)
    else:
        raw_input: str = """
        Button A: X+94, Y+34
        Button B: X+22, Y+67
        Prize: X=8400, Y=5400
        
        Button A: X+26, Y+66
        Button B: X+67, Y+21
        Prize: X=12748, Y=12176
        
        Button A: X+17, Y+86
        Button B: X+84, Y+37
        Prize: X=7870, Y=6450
        
        Button A: X+69, Y+23
        Button B: X+27, Y+71
        Prize: X=18641, Y=10279
        """.strip()
    games = process_input(raw_input)

    # part 1
    tokens = 0
    for game in games:
        p1, p2 = game.get_presses()
        if p1 % 1 == 0 and p2 % 1 == 0:
            tokens += p1 * 3 + p2
    print(tokens)

    # part 2
    for game in games:
        game.tx += 10000000000000
        game.ty += 10000000000000
    tokens = 0
    for game in games:
        p1, p2 = game.get_presses()
        if p1 % 1 == 0 and p2 % 1 == 0:
            tokens += p1 * 3 + p2
    print(tokens)

if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
