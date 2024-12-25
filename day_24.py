import argparse
from get_input import get_input
import re

def day_num() -> int:
    return int(re.search(r'.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()

class Gate:
    def __init__(self, name, g1, g2, op):
        self.name = name
        self.g1 = g1
        self.g2 = g2
        self.op = op
        self.ans = None

    def get_ans(self):
        if self.op == 'AND':
            ans = self.g1.get_ans() & self.g2.get_ans()
        elif self.op == 'OR':
            ans = self.g1.get_ans() | self.g2.get_ans()
        else:
            ans = self.g1.get_ans() ^ self.g2.get_ans()
        return ans

    def __str__(self):
        return f'{self.g1.name} {self.op} {self.g2.name} ->  {self.name}'

class NoOp:
    def __init__(self, name, value):
        self.name = name
        self.ans = value
        self.g1 = None
        self.g2 = None
        self.op = None

    def get_ans(self):
        return self.ans

    def __str__(self):
        return self.name

def get_gates(start_conds, gate_descs, swaps):
    gates = {}
    for start_cond in start_conds:
        gate, val = start_cond.split(': ')
        gates[gate] = NoOp(gate, int(val))
    descs = {}
    for gate_desc in gate_descs:
        g1, op, g2, _, gout = gate_desc.split()
        descs[gout] = (g1, g2, op)
    for a, b in swaps:
        tmp = descs[a]
        descs[a] = descs[b]
        descs[b] = tmp
    while len(descs) + len(start_conds) > len(gates):
        for gout, desc in descs.items():
            if desc[0] in gates and desc[1] in gates:
                gates[gout] = Gate(gout, gates[desc[0]], gates[desc[1]], desc[2])
    return gates

def get_prefix_binary(gates, prefix):
    p_gates = [a for a in gates.keys() if a[0] == prefix]
    b = [0] * len(p_gates)
    for p_gate in p_gates:
        b[int(p_gate.replace(prefix, ''))] = gates[p_gate].get_ans()
    return b

def get_swap(gates):
    xb = get_prefix_binary(gates, 'x')
    yb = get_prefix_binary(gates, 'y')
    zb = get_prefix_binary(gates, 'z')
    swaps = []
    carry = 0
    swapped = False
    a = []
    for i, (xi, yi, zi) in enumerate(zip(xb, yb, zb)):
        a.append((xi + yi + carry) % 2)
        if (not swapped and zi != (xi + yi + carry) % 2) or (swapped and zi == (xi + yi + carry) % 2):
            swaps.append(i)
            swapped = not swapped
        carry = (xi + yi + carry) // 2
    a.append(carry)
    t = []
    for i in range(len(zb)):
        if zb[i] == 1:
            t.append(i)
    return t

def get_affecting_gates(gates, name):
    queue = [name]
    g = []
    while len(queue) > 0:
        curr_name = queue.pop(0)
        if curr_name not in g:
            if curr_name not in g:
                g.append(curr_name)
            curr_gate = gates[curr_name]
            if curr_gate.g1 is not None:
                queue.append(curr_gate.g1.name)
                queue.append(curr_gate.g2.name)
    return g

def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day)
        swaps = [('z08', 'thm'), ('wss', 'wrm'), ('z29', 'gbs'), ('z22', 'hwq')]
    else:
        raw_input: str = """
        x00: 1
        x01: 0
        x02: 1
        x03: 1
        x04: 0
        y00: 1
        y01: 1
        y02: 1
        y03: 1
        y04: 1
        
        ntg XOR fgs -> mjb
        y02 OR x01 -> tnw
        kwq OR kpj -> z05
        x00 OR x03 -> fst
        tgd XOR rvg -> z01
        vdt OR tnw -> bfw
        bfw AND frj -> z10
        ffh OR nrd -> bqk
        y00 AND y03 -> djm
        y03 OR y00 -> psh
        bqk OR frj -> z08
        tnw OR fst -> frj
        gnj AND tgd -> z11
        bfw XOR mjb -> z00
        x03 OR x00 -> vdt
        gnj AND wpb -> z02
        x04 AND y00 -> kjc
        djm OR pbm -> qhw
        nrd AND vdt -> hwm
        kjc AND fst -> rvg
        y04 OR y02 -> fgs
        y01 AND x02 -> pbm
        ntg OR kjc -> kwq
        psh XOR fgs -> tgd
        qhw XOR tgd -> z09
        pbm OR djm -> kpj
        x03 XOR y03 -> ffh
        x00 XOR y04 -> ntg
        bfw OR bqk -> z06
        nrd XOR fgs -> wpb
        frj XOR qhw -> z04
        bqk OR frj -> z07
        y03 OR x01 -> nrd
        hwm AND bqk -> z03
        tgd XOR rvg -> z12
        tnw OR pbm -> gnj
        """.strip()
        swaps = []
    lines = [a.strip() for a in raw_input.strip().split('\n')]
    idx = [len(a) for a in lines].index(0)
    start_conds = lines[:idx]
    gate_descs = lines[idx + 1:]

    gates = get_gates(start_conds, gate_descs, [])

    # part 1
    z_gates = [a for a in gates.keys() if a[0] == 'z']
    z = 0
    zb = [0] * len(z_gates)
    for z_gate in z_gates:
        z += gates[z_gate].get_ans() * 2**(int(z_gate.replace('z', '')))
        zb[int(z_gate.replace('z', ''))] = gates[z_gate].get_ans()
    print(z)

    gates = get_gates(start_conds, gate_descs, swaps)

    # part 2
    # Manual: See if the next level has the right structure
    # Should be a XOR <- XOR and OR <- AND and AND basically

    for i in range(45):
        gates[f'x{str(i).zfill(2)}'].ans = 0
        gates[f'y{str(i).zfill(2)}'].ans = 0

    for i in range(45):
        t = []
        t.append(get_swap(gates))
        gates[f'x{str(i).zfill(2)}'].ans = 1
        t.append(get_swap(gates))
        gates[f'y{str(i).zfill(2)}'].ans = 1
        t.append(get_swap(gates))
        gates[f'x{str(i).zfill(2)}'].ans = 0
        t.append(get_swap(gates))
        gates[f'y{str(i).zfill(2)}'].ans = 0
        if t != [[], [i], [i + 1], [i]]:
            for k in range(i - 1, i + 2):
                print(k)
                g1 = get_affecting_gates(gates, f'z{str(k).zfill(2)}')
                g2 = get_affecting_gates(gates, f'z{str(k - 1).zfill(2)}')
                for g in g1:
                    if g not in g2:
                        print(gates[g])
                print()
            print(i, t)
    print(','.join(sorted([b for a in swaps for b in a])))


if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
