import sys
sys.path.append('../Analyzer')
from logic_operator import *
from magic_domain import *
from analyzer import check_property_refining
import time
'''
This problem is inspired by the magic sequence problem introduced in: DPLL(Agg): an efficient SMT module for aggregates.
We want to synthesize a function f: [0 ... N - 1] -> [0... N] such that f(x) = #{y | f(y) = x}

The problem is encoded with a default f(x) = 0
'''


def number_of_y(x):
    return Sum(Magic, lambda _ : Int(1), lambda m1: EQ(m1.y, x))


if __name__ == '__main__':
    args = sys.argv[1:]
    N = int(args[0]) * 50


    args = args[1:]
    mymin = False
    restart = False
    bcr = False
    ub = False
    arg_len = len(args)
    if arg_len >= 1:
        restart = args[0].lower().startswith('t')
    if arg_len >= 2:
        bcr = args[1].lower().startswith('t')
    if arg_len >= 3:
        ub = args[2].lower().startswith('t')

    complete_rules = []
    add_background_theories(ACTION, state_action, complete_rules)

    # Magic property
    complete_rules.append(forall(Magic, lambda m: Implication(m.x > 0, EQ(m.y, number_of_y(m.x)))))

    # function definition
    complete_rules.append(forall([Magic, Magic], lambda m1, m2: Implication(EQ(m1.x, m2.x), EQ(m1, m2))))

    # value bound on the x and y
    complete_rules.append(forall(Magic, lambda m: AND(m.x < N, m.y <= N)))

    # if f(x) > 0, then f(f(x)) > 0
    complete_rules.append(
        forall(Magic, lambda m: Implication(m.y > 0, exist(Magic, lambda m1: AND(EQ(m1.x, m.y), m1.y > 0)))))

    # f(0) > 0
    target_rule = exist(Magic, lambda m: AND(EQ(m.x, Int(0)),
                                             EQ(Int(N) - m.y, Sum(Magic, lambda _: Int(1), lambda m: m.y > 0))))

    rules = set()
    start = time.time()
    check_property_refining(target_rule, rules, complete_rules, ACTION, state_action, True, min_solution=False,
                            final_min_solution=True, restart=restart, boundary_case=bcr, universal_blocking=ub)
    print(time.time() - start)
