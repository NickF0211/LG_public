import sys
sys.path.append('../Analyzer')
from logic_operator import *
from bank_domain import *
import time
from analyzer import check_property_refining
from type_constructor import union


# rules go here
def _balance(user, time, action):
    deposit_sum = Sum(Depo, lambda deposit: deposit.amount, lambda deposit: AND(EQ(deposit.user, user),
                                                                                deposit.time < time),
                      trigger_act=action, input_subs={"user":user})
    # withdraw_sum = Sum(Withdraw, lambda withdraw: withdraw.amount, lambda withdraw: AND(EQ(withdraw.user, user),
    #                                                                                 withdraw.time < time))

    transfer_in_sum = Sum(Trans, lambda trans: trans.amount,
                          lambda trans: AND(trans.time < time,
                                            EQ(trans.receiver, user)), trigger_act=action, input_subs={"receiver":user})
    trans_out_sum = Sum(Trans, lambda trans: trans.amount,
                        lambda trans: AND(trans.time < time,
                                          EQ(trans.sender, user)), trigger_act=action, input_subs={"sender":user})

    return deposit_sum + transfer_in_sum - trans_out_sum


balance = make_bin_predicate(_balance)

# balance = _balance
complete_rules = []
TS = union(Trans, Depo, Withdraw)

# every transication has a unqie tid
complete_rules.append(NOT(exist([Trans, Trans], lambda ts1, ts2: AND(NEQ(ts1, ts2), EQ(ts1.id, ts2.id)))))
complete_rules.append(NOT(exist([Withdraw, Withdraw], lambda ts1, ts2: AND(NEQ(ts1, ts2), EQ(ts1.id, ts2.id)))))
complete_rules.append(NOT(exist([Depo, Depo], lambda ts1, ts2: AND(NEQ(ts1, ts2), EQ(ts1.id, ts2.id)))))

# every deposite can have at most 500 dollars
complete_rules.append(forall(Depo, lambda depo: depo.amount <= 500))
# every user can deposite at most once every day
complete_rules.append(forall([Depo, Depo], lambda depo1, depo2: Implication(AND(depo1.id > depo2.id,
                                                                                EQ(depo1.user, depo2.user)),
                                                                            NEQ(depo1.time, depo2.time))))

# if a user withdraw, then it must have sufficent balance
complete_rules.append(forall(Withdraw, lambda wd: balance(wd.user, wd.time, wd) >= wd.amount))

# if a user transfer out, then it must have sufficent balance
complete_rules.append(forall(Trans, lambda tr: balance(tr.sender, tr.time, tr) >= tr.amount))
complete_rules.append(forall(Trans, lambda tr: NEQ(tr.sender, tr.receiver)))

# a user can receive at most 2 transfer a day
complete_rules.append(NOT(exist([Trans, Trans, Trans], lambda trans1, trans2, trans3:
AND([trans1.id > trans2.id,
     trans2.id > trans3.id,
     EQ(trans1.receiver, trans2.receiver),
     EQ(trans2.receiver, trans3.receiver),
     EQ(trans1.time, trans2.time),
     EQ(trans2.time, trans3.time)]
    )
                                )))

# a user can send at most 1 transfer
complete_rules.append(NOT(exist([Trans, Trans], lambda trans1, trans2:
AND([trans1.id > trans2.id,
     EQ(trans1.sender, trans2.sender),
     EQ(trans1.time, trans2.time)])
                                )))

rule_1 = exist(Withdraw, lambda wd: AND(EQ(wd.amount, Int(1273)), wd.time <= 2))
rule_2 = exist(Withdraw, lambda wd: AND(EQ(wd.amount, Int(1800)), wd.time <= 2))
rule_3 = exist(Withdraw, lambda wd: AND(EQ(wd.amount, Int(2001)), wd.time <= 2))
rule_4 = exist(Withdraw, lambda wd: AND(EQ(wd.amount, Int(2001)), wd.time <= 3))
rule_5 = exist(Withdraw, lambda wd: AND(EQ(wd.amount, Int(4000)), wd.time <= 3))
rule_6 = exist(Withdraw, lambda wd: AND(EQ(wd.amount, Int(6000)), wd.time <= 3))
rule_7 = exist(Withdraw, lambda wd: AND(EQ(wd.amount, Int(6500)), wd.time <= 3))
rule_8 = exist(Withdraw, lambda wd: AND(EQ(wd.amount, Int(6501)), wd.time <= 3))
rule_9 = exist(Withdraw, lambda wd: AND(EQ(wd.amount, Int(7000)), wd.time <= 4))
rule_10 = exist(Withdraw, lambda wd: AND(EQ(wd.amount, Int(12000)), wd.time <= 4))
rule_11 = exist(Withdraw, lambda wd: AND(EQ(wd.amount, Int(200000)), wd.time <= 4))

if __name__ == '__main__':
    args = sys.argv[1:]
    target_rule = globals()["rule_{}".format(args[0])]

    args = args[1:]
    mymin = True
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

    rules = set()
    start = time.time()
    complete_rules = add_background_theories(ACTION, state_action, complete_rules, bcr)
    check_property_refining(target_rule, set(complete_rules), complete_rules, ACTION, state_action, True, min_solution=True,
                            final_min_solution=True, restart=restart, boundary_case=bcr, universal_blocking=ub)
    print(time.time() - start)
