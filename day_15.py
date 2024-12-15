import argparse
from get_input import get_input
import re

def day_num() -> int:
    return int(re.search(r'.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()

class Grid:
    def __init__(self, input):
        self.input = input
        self.reset_grid()

    command_to_direction = {
        '>': (0, 1),
        'v': (1, 0),
        '<': (0, -1),
        '^': (-1, 0)
    }

    def reset_grid(self):
        split_idx = [len(a) for a in self.input].index(0)
        self.grid = [[c for c in line] for line in self.input[:split_idx]]
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == '@':
                    self.robot = (i, j)
        self.commands = ''.join(self.input[split_idx + 1:])

    def reject_move(self, potential_move):
        new_pos = (self.robot[0] + potential_move[0], self.robot[1] + potential_move[1])
        while self.grid[new_pos[0]][new_pos[1]] == 'O':
            new_pos = (new_pos[0] + potential_move[0], new_pos[1] + potential_move[1])
        if self.grid[new_pos[0]][new_pos[1]] == '.':
            self.grid[new_pos[0]][new_pos[1]] = 'O'
        return self.grid[new_pos[0]][new_pos[1]] == '#'

    def run_command(self, idx):
        potential_move = self.command_to_direction[self.commands[idx]]
        if not self.reject_move(potential_move):
            self.grid[self.robot[0]][self.robot[1]] = '.'
            self.robot = (self.robot[0] + potential_move[0], self.robot[1] + potential_move[1])
            self.grid[self.robot[0]][self.robot[1]] = '@'

    def run_commands(self):
        for idx in range(len(self.commands)):
            self.run_command(idx)

    def get_gps(self):
        gps = 0
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 'O':
                    gps += 100 * i + j
        return gps

    def __str__(self):
        return '\n'.join([''.join(line) for line in self.grid])

class DoubleGrid:
    def __init__(self, input):
        self.input = input
        self.reset_grid()

    command_to_direction = {
        '>': (0, 1),
        'v': (1, 0),
        '<': (0, -1),
        '^': (-1, 0)
    }
    doublify = {
        '#': ['#', '#'],
        '.': ['.', '.'],
        '@': ['@', '.'],
        'O': ['[', ']']
    }

    def reset_grid(self):
        split_idx = [len(a) for a in self.input].index(0)
        self.grid = [[dc for c in line for dc in self.doublify[c]] for line in self.input[:split_idx]]
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == '@':
                    self.robot = (i, j)
        self.commands = ''.join(self.input[split_idx + 1:])

    def get_affected_box_positions(self, current_positions):
        affected_box_positions = set()
        for position in current_positions:
            if self.grid[position[0]][position[1]] == ']':
                affected_box_positions |= {(position[0], position[1] - 1), (position[0], position[1])}
            if self.grid[position[0]][position[1]] == '[':
                affected_box_positions |= {(position[0], position[1] + 1), (position[0], position[1])}
            if self.grid[position[0]][position[1]] == '#':
                affected_box_positions |= {(position[0], position[1])}
        return affected_box_positions

    def move_boxes_vert(self, potential_move):
        new_pos = (self.robot[0] + potential_move[0], self.robot[1] + potential_move[1])
        new_affected_box_positions = self.get_affected_box_positions({new_pos})
        affected_box_positions = set()
        while len(new_affected_box_positions) > 0:
            if any([self.grid[position[0]][position[1]] == '#' for position in new_affected_box_positions]):
                affected_box_positions = set()
                break
            else:
                affected_box_positions |= new_affected_box_positions
                potential_box_positions = {(position[0] + potential_move[0], position[1] + potential_move[1]) for position in new_affected_box_positions}
                new_affected_box_positions = self.get_affected_box_positions(potential_box_positions)
        moving_dict = {position: self.grid[position[0]][position[1]] for position in affected_box_positions}
        for position, c in moving_dict.items():
            self.grid[position[0]][position[1]] = '.'
        for position, c in moving_dict.items():
            self.grid[position[0] + potential_move[0]][position[1] + potential_move[1]] = c

    def move_boxes_horiz(self, potential_move):
        new_pos = (self.robot[0] + potential_move[0], self.robot[1] + potential_move[1])
        affected_box_positions = set()
        while self.grid[new_pos[0]][new_pos[1]] in ['[', ']']:
            affected_box_positions |= {(new_pos[0], new_pos[1])}
            new_pos = (new_pos[0] + potential_move[0], new_pos[1] + potential_move[1])
        if self.grid[new_pos[0]][new_pos[1]] == '.':
            moving_dict = {position: self.grid[position[0]][position[1]] for position in affected_box_positions}
            for position, c in moving_dict.items():
                self.grid[position[0]][position[1]] = '.'
            for position, c in moving_dict.items():
                self.grid[position[0] + potential_move[0]][position[1] + potential_move[1]] = c

    def run_command(self, idx):
        potential_move = self.command_to_direction[self.commands[idx]]
        if potential_move[0] != 0:
            self.move_boxes_vert(potential_move)
        else:
            self.move_boxes_horiz(potential_move)
        if self.grid[self.robot[0] + potential_move[0]][self.robot[1] + potential_move[1]] == '.':
            self.grid[self.robot[0]][self.robot[1]] = '.'
            self.robot = (self.robot[0] + potential_move[0], self.robot[1] + potential_move[1])
            self.grid[self.robot[0]][self.robot[1]] = '@'

    def run_commands(self):
        for idx in range(len(self.commands)):
            self.run_command(idx)

    def get_gps(self):
        gps = 0
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == '[':
                    gps += 100 * i + j
        return gps

    def __str__(self):
        return '\n'.join([''.join(line) for line in self.grid])


def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day)
    else:
        raw_input: str = """
        ##########
        #..O..O.O#
        #......O.#
        #.OO..O.O#
        #..O@..O.#
        #O#..O...#
        #O..O..O.#
        #.OO.O.OO#
        #....O...#
        ##########

        <vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
        vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
        ><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
        <<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
        ^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
        ^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
        >^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
        <><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
        ^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
        v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
        """.strip()

    input = [a.strip() for a in raw_input.strip().split('\n')]

    # part 1
    grid = Grid(input)
    grid.run_commands()
    print(grid.get_gps())

    # part 2
    double_grid = DoubleGrid(input)
    double_grid.run_commands()
    print(double_grid.get_gps())


if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
