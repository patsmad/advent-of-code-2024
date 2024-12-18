import argparse
from get_input import get_input
import re

def day_num() -> int:
    return int(re.search(r'.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()

class Computer:
    def __init__(self, A, B, C, program):
        self.A = A
        self.B = B
        self.C = C
        self.program = program
        self.idx = 0

    def combo_op(self, op):
        return {
            0: 0,
            1: 1,
            2: 2,
            3: 3,
            4: self.A,
            5: self.B,
            6: self.C
        }[op]

    def adv(self, op):
        self.A = self.A // 2**self.combo_op(op)
        self.idx += 2

    def bxl(self, op):
        self.B ^= op
        self.idx += 2

    def bst(self, op):
        self.B = self.combo_op(op) % 8
        self.idx += 2

    def jnz(self, op):
        if self.A != 0:
            self.idx = op
        else:
            self.idx += 2

    def bxc(self, op):
        self.B ^= self.C
        self.idx += 2

    def out(self, op):
        output = self.combo_op(op) % 8
        self.idx += 2
        return output

    def bdv(self, op):
        self.B = self.A // 2**self.combo_op(op)
        self.idx += 2

    def cdv(self, op):
        self.C = self.A // 2 ** self.combo_op(op)
        self.idx += 2

    def run_command(self, instruction, op):
        return {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv
        }[instruction](op)

    def run_program(self):
        overall_output = []
        while 0 <= self.idx < len(self.program):
            output = self.run_command(self.program[self.idx], self.program[self.idx + 1])
            if output is not None:
                overall_output.append(output)
        return overall_output

def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day)
    else:
        raw_input: str = """
        Register A: 729
        Register B: 0
        Register C: 0
        
        Program: 0,1,5,4,3,0
        """.strip()

        raw_input: str = """
        Register A: 2024
        Register B: 0
        Register C: 0
        
        Program: 0,3,5,4,3,0
        """.strip()

    input = raw_input.strip().split('\n')
    idx = [len(a.strip()) for a in input].index(0)
    registers = [int(a.split(': ')[-1].strip()) for a in input[:idx]]
    program = list(map(int, input[idx + 1].split(': ')[-1].strip().split(',')))

    # part 1
    c = Computer(*registers, program)
    print(','.join(map(str, c.run_program())))

    # part 2
    A = 0
    num = 1
    while num <= len(program):
        A *= 8
        registers[0] = A
        output = Computer(*registers, program).run_program()
        while output != program[-num:]:
            A += 1
            registers[0] = A
            output = Computer(*registers, program).run_program()
        num += 1
    print(A)

if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
