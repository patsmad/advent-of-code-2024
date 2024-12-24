import argparse
from get_input import get_input
import re

def day_num() -> int:
    return int(re.search(r'.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()

class Graph:
    def __init__(self, connex):
        self.computers = set()
        self.connex = {}
        for c1, c2 in connex:
            self.computers |= {c1, c2}
            if c1 not in self.connex:
                self.connex[c1] = []
            if c2 not in self.connex:
                self.connex[c2] = []
            self.connex[c1].append(c2)
            self.connex[c2].append(c1)

    def get_next_level(self, c_set, c_bank):
        next_level = set()
        for computer in c_bank:
            if all([c in self.connex[computer] for c in c_set]):
                next_level |= {computer}
        return next_level


def get_max(g):
    max_graph = {}
    possible_max = max([len(a) for a in g.connex.values()])
    for i, c1 in enumerate(g.computers):
        connex_c = g.get_next_level({c1}, g.computers - {c1})
        queue = set([(c1, c2) for c2 in connex_c])
        while len(queue) > 0:
            c_set = set(queue.pop())
            if c1 not in max_graph or len(max_graph[c1]) < len(c_set):
                max_graph[c1] = c_set
                if len(c_set) == possible_max:
                    return max_graph
            for new_c in g.get_next_level(c_set, connex_c - c_set):
                queue |= {tuple(c_set | {new_c})}
    return max_graph


def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day)
    else:
        raw_input: str = """
        kh-tc
        qp-kh
        de-cg
        ka-co
        yn-aq
        qp-ub
        cg-tb
        vc-aq
        tb-ka
        wh-tc
        yn-cg
        kh-ub
        ta-co
        de-co
        tc-td
        tb-wq
        wh-td
        ta-ka
        td-qp
        aq-cg
        wq-ub
        ub-vc
        de-ta
        wq-aq
        wq-vc
        wh-yn
        ka-de
        kh-ta
        co-tc
        wh-qp
        tb-vc
        td-yn
        """.strip()
    connex = [tuple(a.strip().split('-')) for a in raw_input.strip().split('\n')]

    # part 1
    g = Graph(connex)
    triples = set()
    for c1 in g.computers:
        if 't' == c1[0]:
            connex_c = g.get_next_level({c1}, g.computers - {c1})
            for c2 in connex_c:
                for c3 in g.get_next_level({c1, c2}, connex_c - {c2}):
                    triples |= {tuple(sorted([c1, c2, c3]))}
    print(len(triples))

    # part 2
    g = Graph(connex)
    max_graph = get_max(g)
    print(','.join(sorted(max_graph[sorted(max_graph, key=lambda x: -len(max_graph[x]))[0]])))



if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
