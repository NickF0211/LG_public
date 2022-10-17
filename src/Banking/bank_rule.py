import sys
sys.path.append('../Analyzer')
from logic_operator import *
from bank_domain import *
import time
from analyzer import check_property_refining, prove_by_induction
from type_constructor import union

Balance_delay = 12


# rules go here


def _deposit_sum(user, time, action):
    deposit_sum = Sum(Depo, lambda deposit: deposit.amount, lambda deposit: AND(EQ(deposit.user, user),
                                                                                deposit.time < time),
                      trigger_act=action, input_subs={"user":user})
    return deposit_sum


#deposit_sum = make_bin_predicate(_deposit_sum)
deposit_sum = _deposit_sum

def _withdraw_sum(user, time, action):
    withdraw_sum = Sum(Withdraw, lambda withdraw: withdraw.amount, lambda withdraw: AND(EQ(withdraw.user, user),
                                                                                        withdraw.time < time),
                       trigger_act=action, input_subs={"user":user})

    return withdraw_sum


#withdraw_sum = make_bin_predicate(_withdraw_sum)
withdraw_sum = _withdraw_sum


def _transfer_in_sum(user, time, action):
    transfer_in_sum = Sum(Trans, lambda trans: trans.amount,
                          lambda trans: AND(trans.time < time,
                                            EQ(trans.receiver, user)), trigger_act=action, input_subs={"receiver":user})
    return transfer_in_sum


#transfer_in_sum = make_bin_predicate(_transfer_in_sum)
transfer_in_sum = _transfer_in_sum


def _transfer_out_sum(user, time, action):
    trans_out_sum = Sum(Trans, lambda trans: trans.amount,
                        lambda trans: AND(trans.time < time,
                                          EQ(trans.sender, user)), trigger_act=action, input_subs={"sender":user})
    return trans_out_sum

#transfer_out_sum = make_bin_predicate(_transfer_out_sum)
transfer_out_sum = _transfer_out_sum


def _balance(user, time, action, delay=Balance_delay):
    d_sum = deposit_sum(user,time - delay,action)
    t_in_sum = transfer_in_sum(user,time - delay,action)
    t_out_sum = transfer_out_sum(user,time,action)
    return d_sum + t_in_sum - t_out_sum


balance = make_bin_predicate(_balance)


def _daily_transfer_out_sum(user, time, action):
    trans_out_sum = Sum(Trans, lambda trans: trans.amount,
                        lambda trans: AND(trans.time >= time - Int(24),
                                          trans.time < time,
                                          EQ(trans.sender, user)), trigger_act=action, input_subs={"sender":user})
    return trans_out_sum

daily_transfer_out_sum = make_bin_predicate(_daily_transfer_out_sum)



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
                                                                            depo1.time > depo2.time + Int(24))))

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
     trans1.time < trans3.time + Int(24),
     trans2.time < trans3.time + Int(24), ]
    )
                                )))

# a user can send at most 1 transfer at every hour
complete_rules.append(NOT(exist([Trans, Trans], lambda trans1, trans2:
AND([trans1.id > trans2.id,
     EQ(trans1.sender, trans2.sender),
     trans1.time <= trans2.time])
                                )))

# if a user transfer out an amount that is greater than 3000, then there is at least one day
# in the last week the user has transfer out more than 3000
transfer_protection = forall(Trans, lambda trans: Implication(trans.amount > 1500,
                                                              once(Trans, lambda trans1: AND(EQ(trans.sender, trans1.sender),
                                                                  _daily_transfer_out_sum(trans1.sender, trans1.time, trans1) > 1500,
                                                                                             trans1.time < trans.time -24,
                                                                                             trans1.time >= trans.time - Int(144)) ,
                                                                   trans.time
                                                              )))

rule_1 = exist(Trans, lambda wd: AND(EQ(wd.amount, Int(325)), wd.time <= 24))
rule_2 = exist(Trans, lambda wd: AND(EQ(wd.amount, Int(1000)), wd.time <= 36))
rule_3 = exist(Trans, lambda wd: AND(EQ(wd.amount, Int(3000)), wd.time <= 41))
rule_4 = exist(Trans, lambda wd: AND(EQ(wd.amount, Int(4000)), wd.time <= 48))
rule_5 = exist(Trans, lambda wd: AND(EQ(wd.amount, Int(4001)), wd.time <= 48))
rule_6 = exist(Trans, lambda wd: AND(EQ(wd.amount, Int(4001)), wd.time <= 50))
rule_7 = exist(Trans, lambda wd: AND(EQ(wd.amount, Int(6500)), wd.time <= 52))
rule_8 = exist(Trans, lambda wd: AND(EQ(wd.amount, Int(6501)), wd.time <= 60))
rule_9 = AND(transfer_protection, exist(Trans, lambda wd: wd.amount > 1001))
rule_10 = AND(transfer_protection, exist(Trans, lambda wd: wd.amount > 1501))
rule_11 = AND(transfer_protection, exist(Trans, lambda wd: wd.amount > 2000))
rule_12 = AND(transfer_protection, exist(Trans, lambda wd: wd.amount > 2500))

if __name__ == '__main__':

    args = sys.argv[1:]
    target_rule = globals()["rule_{}".format(args[0])]

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

    rules = set()
    start = time.time()
    complete_rules = add_background_theories(ACTION, state_action, complete_rules, bcr)
    check_property_refining(target_rule, set(complete_rules), complete_rules, ACTION, state_action, True, min_solution=True,
                            final_min_solution=True, restart=restart, boundary_case=bcr, universal_blocking=ub)
    print(time.time() - start)
