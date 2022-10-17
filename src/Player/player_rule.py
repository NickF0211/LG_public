"""
A player can play with at most X players at the same time.
If a player A plays with B, then he has two play with at most $Turn_Around$ players before playing with B again
A player becomes friend with another player if they have played at least 3 times

Is it possible to have a player befriend with everyone he has ever played with X days
"""
import sys
sys.path.append('../Analyzer')
from logic_operator import *
from player_domain import *
from analyzer import check_property_refining
import time




if __name__ == '__main__':

    args = sys.argv[1:]

    FRIEND_THRESHOLD = int(args[0])
    Group_Size = int(args[1])
    Turn_Around_Players = int(args[2])

    args = args[3:]
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





    # A palyer is friend with player B at time t if A and B has played more than FRIEND_THRESHOLD number of times since t,
    # and they have, and the most recent play was within the last 3 days
    def _friend(a, b, time, trigger_action):
        return AND(Count(Play, lambda p: AND(EQ(p.a, a),
                                         EQ(p.b, b),
                                         p.time < time), trigger_act=trigger_action, input_subs={"a": a,
                                                                                                 "b": b}) >= Int(
            FRIEND_THRESHOLD),

                   exist(Play, lambda play: AND(EQ(play.a, a),
                                                            EQ(play.b, b),
                                                            play.time < time,
                                                            play.time >= (time - Int(Turn_Around_Players + 1))), input_subs={"a": a,
                                                                                                "b": b}))


    friend = make_predicate(_friend, 3)

    complete_rules = []

    # No self play
    complete_rules.append(forall(Play, lambda play: NEQ(play.a, play.b)))

    # at any point, A player should not play with more than Group_Size of players at one time
    complete_rules.append(forall(Play, lambda p: Count(Play, lambda p1: AND(EQ(p.a, p1.a), EQ(p.time, p1.time)),
                                                       trigger_act=p, input_subs={"a": p.a, "time": p.time}) <= Int(
        Group_Size)))


    # if A plays with B, then it must play with at least Turn_Around_Players players before play with B again
    complete_rules.append(forall([Play, Play], lambda p1, p2:
    Implication(AND(EQ(p1.a, p2.a), EQ(p1.b, p2.b), p1 < p2),
                Count(Play, lambda p3: AND(EQ(p3.a, p1.a),
                                           NEQ(p3.b, p2.b),
                                           p3 > p1,
                                           p3 < p2
                                           ), trigger_act=p2, input_subs={"a": p1.a}) >= Int(Turn_Around_Players)
                )
                                 ))

    complete_rules.append(forall(Friend, lambda f: friend(f.a, f.b, f.time, f)
                                 ))

    # property, exists a user who has at least one friend who befriended everyone he ever played with
    target_rule = exist(Friend, lambda f: forall(Play, lambda play: Implication(EQ(f.a, play.a),
                                                                           exist(Friend,
                                                                                 lambda f1: AND(EQ(play.a, f1.a),
                                                                                                EQ(play.b, f1.b),
                                                                                                EQ(f.time, f1.time)),
                                                                                 input_subs={"a": play.a, "b": play.b, "time":f.time})
                                                                           )), input_subs=({"a": Int(1), "b": Int(2)}))

    complete_rules = add_background_theories(ACTION, state_action, complete_rules, bcr)

    rules = set()
    start = time.time()
    check_property_refining(target_rule, rules, complete_rules, ACTION, state_action, True, min_solution=True,
                             restart=restart, boundary_case=bcr, universal_blocking=ub)
    print(time.time() - start)