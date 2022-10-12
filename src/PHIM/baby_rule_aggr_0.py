import sys
sys.path.append('../Analyzer/')

from logic_operator import *
from baby_domain_0 import *
from analyzer import check_property_refining, prove_by_induction
import time

########################################################################
# Shortcuts
########################################################################

EQ = Equals
NEQ = NotEquals

########################################################################
# Declarative model
########################################################################

def get_action_name(action_id):
    if action_id == 1:
        return "access"
    elif action_id == 2:
        return "disclose"

action_iteration_bound = 1000

#pid starts with pid 0
root_pid = forall(Collect, lambda collect1 : Implication(GT(collect1.pid, Int(0)),
                                                             exist(Collect, lambda collect2: AND(EQ(collect2.pid, Int(0)), collect2 < collect1))))

# patient id unique and increasing
incrementing_pid = forall(Collect, lambda collect1 : Implication(GT(collect1.pid, Int(0)),
                                                             OR(exist(Collect, lambda collect2: And(
                                                                 (EQ(collect1.pid, Plus(collect2.pid, Int(1)))),
                                                             collect2 < collect1)))))

#pids are collected in order
increasing_pid = forall(Collect, lambda collect1 : forall(Collect, lambda collect2: Implication(collect1 > collect2,
                                                                                                 GT(collect1.pid, collect2.pid))))

# A data can be collected only once
no_double_collect = forall(Collect, lambda c1: forall(Collect, lambda c2: Implication(NOT(c1.build_eq_constraint(c2)),
                                                                                      NEQ(c1.pid, c2.pid))))

#update after collection but before deletion
update_after_collection = forall(Request_Update, lambda update: once(Collect, lambda collect: AND(
                                                                                           EQ(collect.pid, update.pid),
                                                                                           EQ(collect.subject, update.subject),
                                                                                                   NOT(exist(Erase, lambda erase: AND(
                                                                                                             erase <= update,
                                                                                                             erase >= collect,
                                                                                                             EQ(erase.pid, collect.pid))
                                                                                                             ))), update.time))

#a pid can be accessed only if it has been collected
access_after_collection = forall(Access, lambda access: exist(Collect, lambda collect: AND(collect < access,
                                                                                           EQ(collect.pid, access.pid))))

#the value of access is the most update to date
access_up_to_date_u =  forall(Access, lambda access: forall(Update, lambda update: Implication(AND(update < access,
                                                                                           EQ(update.pid, access.pid),
                                                                                      NEQ(update.pvalue, access.pvalue)),
                                                                                              exist(Update, lambda update1:
                                                                                                    AND(update1 < access,
                                                                                                        update1 > update,
                                                                                                        EQ(update1.pid,
                                                                                                               access.pid),
                                                                                                        EQ(update1.pvalue,
                                                                                                               access.pvalue))))))

access_up_to_date_c =  forall(Access, lambda access: forall(Collect, lambda update: Implication(AND(update < access,
                                                                                           EQ(update.pid, access.pid),
                                                                                      NEQ(update.pvalue, access.pvalue)),
                                                                                              exist(Update, lambda update1:
                                                                                                    AND(update1 < access,
                                                                                                        update1 > update,
                                                                                                        EQ(update1.pid,
                                                                                                               access.pid),
                                                                                                        EQ(update1.pvalue,
                                                                                                               access.pvalue))))))
access_up_to_date = AND(access_up_to_date_c, access_up_to_date_u)

access_not_deleted = forall([Access, Erase], lambda ac, er: Implication(EQ(ac.pid, er.pid),
                                                                        ac < er))

request_to_update_fullfilled = forall(Request_Update, lambda ur: exist(Update, lambda update:
                                                                       AND(EQ(ur.pid, update.pid),
                                                                           EQ(ur.subject, update.subject),
                                                                           EQ(ur.pvalue, update.pvalue),
                                                                           LT(update.time, ur.time + Int(30)),
                                                                           update > ur)))

no_random_update = forall(Update, lambda update: exist(Request_Update, lambda ur:
                                                                       AND(EQ(ur.pid, update.pid),
                                                                           EQ(ur.subject, update.subject),
                                                                           EQ(ur.pvalue, update.pvalue),
                                                                           ur < update)))

no_two_collect_with_time = NOT(exist([Collect, Collect], lambda c1, c2: AND(NEQ(c1.pid, c2.pid), EQ(c1.subject, c2.subject),
                                                                            c1 > c2,
                                                                            LT(Minus(c1.time, c2.time), Int(5)))))


erase_own_data = forall(Erase,lambda erase : exist(Collect, lambda collect: AND(collect < erase, EQ(collect.pid, erase.pid),
                                                                                 EQ(collect.subject, erase.subject))))

def _balance(subject, time, trigger_action):
    isb = dict()
    isb["subject"] = subject
    col_sum = Sum(Collect, lambda _: Int(4), lambda col: AND(EQ(col.subject, subject), col < time), trigger_act=trigger_action, input_subs = isb)
    update_sum = Sum(Update, lambda _: Int(3), lambda col: AND(EQ(col.subject, subject), col < time), trigger_act=trigger_action, input_subs = isb)
    erase_sum = Sum(Erase, lambda erase: erase.time + Int(5), lambda col: AND(EQ(col.subject, subject), col < time), trigger_act=trigger_action, input_subs= isb)
    return col_sum + update_sum - erase_sum

balance = make_bin_predicate(_balance)

erase_with_balence = forall(Erase, lambda erase : balance(erase.subject, erase.time, erase) >= (erase.time + Int(5)))

One_data_per_person = forall(Collect, lambda c1: forall(Collect, lambda c2:
                                                        Implication(NEQ(c1.pid, c2.pid),
                                                                    NEQ(c1.subject, c2.subject))))


access_consented = forall(Access, lambda access: once(Authorize, lambda au:
AND(EQ(access.pid, au.pid), EQ(access.a1, au.a1), EQ(au.permission, Int(1))),access.time))


access_right_purpose = forall(Access, lambda access: once(Collect, lambda collect: AND(EQ(access.pid, collect.pid),
                                                                                       once(Assign_Expertise,
                                                                                            lambda ae: AND(EQ(ae.a1, access.a1),
                                                                                                           exist(Has_Expertise, lambda he:
                                                                                                                 AND(EQ(he.time, Int(0)),
                                                                                                                     EQ(he.purpose, collect.purpose),
                                                                                                                     EQ(ae.expertise, he.expertise)
                                                                                                                     )
                                                                                                                 )) ,access.time)), access.time))

complete_rules = [access_consented, access_right_purpose,  no_two_collect_with_time, increasing_pid, One_data_per_person, incrementing_pid, root_pid, update_after_collection, access_up_to_date,
             request_to_update_fullfilled, no_random_update, access_after_collection, no_double_collect, erase_own_data, erase_with_balence,
                  access_not_deleted]

########################################################################
## Rules
########################################################################

# test rule
rule_0 = exist(Update, lambda collect : EQ(collect.pid, Int(90)))

# violation against permission to update
rule_1 = exist(Request_Update, lambda ru: exist(Collect, lambda collect:
													exist(TimeStamp, lambda ts:
														  AND(GT(ts.time, ru.time + Int(30)),
															EQ(collect.subject, ru.subject),
															EQ(collect.pid, ru.pid),
															collect < ru,
																NOT(exist(Update, lambda update:
																		  AND(EQ(update.pid, ru.pid),
																			  EQ(update.subject, ru.subject),
																			  EQ(update.pvalue, ru.pvalue),
																			  update >= ru,
																			  update <= ts)
																		  ))
															  ))))

# unordered pids
rule_2 = exist(Collect, lambda collect: AND(EQ(collect.pid, Int(5)),
                                               exist(Collect, lambda collect1: AND(collect1 < collect,
                                                                                   GE(collect1.pid, collect.pid)))))
# invalid_access
rule_3 =  exist(Update, lambda update: forall(Collect, lambda  collect: Implication(collect < update, NEQ(collect.pid, update.pid))))

# out of order pids
rule_4 = exist([Collect, Collect], lambda collect1, collect2: AND(collect2 > collect1, LT(collect2.pid, collect1.pid)))

# access a given big pid
rule_5 = eventually(Access, lambda cl: GT(cl.pid, Int(50)))

# access after data deleted
rule_6 = eventually(Access,  lambda access : once(Collect, lambda collect:
	                                         AND (EQ(collect.pid, access.pid),
	                                              exist(Erase, lambda erase:
														AND (erase < access,
														erase >= collect,
														EQ(erase.pid, collect.pid))
														)),
											access.time))
if max_pid is None:
    rule_7 = eventually(Erase, lambda erase: EQ(erase.pid, Int(10)))
else:
    rule_7 = eventually(Erase, lambda erase: EQ(erase.pid, Int(min(10, max_pid))))

def generate_function(index, max_pid):
    if max_pid is None:
        return eventually(Erase, lambda erase: EQ(erase.pid, Int(index)))
    else:
        return eventually(Erase, lambda erase: EQ(erase.pid, Int(min(index, max_pid))))

starting = 5
fuzz_counter = 18
for k in range(8, fuzz_counter):
    globals()["rule_" + str(k)] = generate_function(starting, max_pid)
    starting += 1

cur_rule = fuzz_counter
for k in range(7, fuzz_counter):
    for j in range(k+1, fuzz_counter):
        globals()["rule_"+str(cur_rule)] = AND(globals()["rule_"+str(k)], globals()["rule_"+str(j)])
        cur_rule += 1

# data minimisation

########################################################################
## Main
########################################################################
# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    args = sys.argv[1:]
    mymin = False
    restart = False
    bcr = False
    ub = False
    arg_len = len(args)
    if arg_len >= 1:
        mymin = args[0].lower().startswith('t')
    if arg_len >= 2:
        restart = args[1].lower().startswith('t')
    if arg_len >= 3:
        bcr = args[2].lower().startswith('t')
    if arg_len >= 4:
        ub = args[3].lower().startswith('t')

    rules = set()
    start = time.time()
    print(mymin)
    add_background_theories(ACTION, state_action, complete_rules)
    check_property_refining(rule_8, rules, complete_rules, ACTION, state_action, True, vol_bound = 10, min_solution=mymin, final_min_solution=True, restart=restart, boundary_case = bcr, universal_blocking=ub)
    print(time.time() - start)
