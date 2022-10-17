import sys
sys.path.append('../Analyzer')
from logic_operator import *
import time
from analyzer import check_property_refining

'''
TODO: The domain file need to be linked
'''


from graph_domain import *

#now we write rules here, we want to being able to construct a tree with a single root



def is_node_available(node, time, add_node = None):
    if add_node and isinstance(add_node, AddNode):
        return NOT(exist(RemoveNode, lambda rn: AND(EQ(rn.node, add_node.node), rn.time <= time, rn > add_node)))
    else:
        return since(AddNode, lambda an: EQ(an.node, node), RemoveNode, lambda rn:
                     EQ(rn.node, node),time, input_subs={"node":node})

def same_edge(edge, f, t):
    return AND(EQ(edge.f, f), EQ(edge.t, t))

def is_edge_available(f, t, time):
    return since(AddEdge, lambda ae: same_edge(ae, f, t), RemoveEdge, lambda re:
    same_edge(re, f, t), time, input_subs={"f":f, "t":t})

def has_parent(node, time):
    return once(AddEdge, lambda ae: AND( EQ(ae.t, node),
                                        is_edge_available(ae.f, ae.t, time)), time, input_subs={"t":node})

def has_child(node, time):
    return once(AddEdge, lambda ae: AND(EQ(ae.f, node),
                                        is_edge_available(ae.f, ae.t, time)), time, input_subs={"f":node})

# a node is a root if it doesn't have any parent
def is_root(node, time):
    return AND(is_node_available(node, time),
               has_parent(node, time))



def get_num_child(node, time, trigger_action):
    return Count(AddEdge, lambda ae: AND(EQ(ae.f, node),
                                                          is_edge_available(ae.f, ae.t, time)), trigger_act=trigger_action)

def get_num_parent(node, time, tigger_action):
    return Count(AddEdge, lambda ae: AND(EQ(ae.t, node),
                                                          is_edge_available(ae.f, ae.t, time)), trigger_act=tigger_action)

# get_num_child = make_predicate(_get_num_child, 2)
# get_num_parent = make_predicate(_get_num_parent, 2)

complete_rules = []

#a node can be added if it was not already there
complete_rules.append(forall(AddNode, lambda an:
    NOT(is_node_available(an.node, an.time-1))))

#a node can be removed if it was already there
complete_rules.append(forall(RemoveNode, lambda rn:
    is_node_available(rn.node, rn.time-1)))

#a node can be removed if all of its edges have been removed
complete_rules.append(forall(RemoveNode, lambda rn:
    AND(NOT(has_child(rn.node, rn.time)),
                                                        NOT(has_parent(rn.node, rn.time)))))



#an edge can be added if the edge was not already there, and both f and t are available
complete_rules.append(forall(AddEdge, lambda ae: AND(is_node_available(ae.f, ae.time),
                                                     is_node_available(ae.t, ae.time),
                                                     NOT(is_edge_available(ae.f, ae.t, ae.time-1)))))

#no self edge is allowed
complete_rules.append(forall(AddEdge, lambda ae: NEQ(ae.f, ae.t)))

#each node can only have at most 1 parent
complete_rules.append(forall(AddEdge, lambda ae:AND(NOT(has_parent(ae.t, ae.time-1)),
                                                        NOT(exist(AddEdge, lambda ae1: AND(EQ(ae1.time, ae.time),
                                                                                           EQ(ae1.t, ae.t),
                                                                                           NEQ(ae1.f, ae.f)))))))

#an edge can be removed if the edge is available
complete_rules.append(forall(RemoveEdge, lambda re: is_edge_available(re.f, re.t, re.time-1)))



#tree
tree_req = forall(AddEdge, lambda ae: get_num_parent(ae.f, ae.time, ae) <= Int(2))
binary_tree_req = forall(AddEdge, lambda ae: get_num_child(ae.f, ae.time, ae) <= Int(2))
connected_rule = forall(AddNode, lambda an: get_num_parent(an.node, an.time, an) > Int(0))


complete_rules.append(tree_req )
complete_rules.append(binary_tree_req)
complete_rules.append(connected_rule)

rule_1 = exist(Var, lambda var: Count(AddNode, lambda addnode: is_node_available(addnode.node, var.v)) > Int(2))
rule_2 = exist(Var, lambda var: Count(AddNode, lambda addnode: is_node_available(addnode.node, var.v)) > Int(4))
rule_3 = exist(Var, lambda var: Count(AddNode, lambda addnode: is_node_available(addnode.node, var.v)) > Int(5))
rule_4 = exist(Var, lambda var: Count(AddNode, lambda addnode: is_node_available(addnode.node, var.v)) > Int(8))
rule_5 = exist(Var, lambda var: Count(AddNode, lambda addnode: is_node_available(addnode.node, var.v)) > Int(10))
rule_6 = exist(Var, lambda var: Count(AddNode, lambda addnode: is_node_available(addnode.node, var.v)) > Int(12))
rule_7 = exist([Var, Var], lambda var1, var2:
                AND(Count(AddNode, lambda addnode: is_node_available(addnode.node, var1.v) ) > Int(4),
                   Count(AddNode, lambda addnode1: is_node_available(addnode1.node, var2.v)) < Int(2),
                    var1.v < var2.v)
                )
rule_8 = exist([Var, Var], lambda var1, var2:
                AND(Count(AddNode, lambda addnode: is_node_available(addnode.node, var1.v) ) > Int(5),
                   Count(AddNode, lambda addnode1: is_node_available(addnode1.node, var2.v)) < Int(3),
                    var1.v < var2.v)
                )
rule_9 = exist([Var, Var], lambda var1, var2:
                AND(Count(AddNode, lambda addnode: is_node_available(addnode.node, var1.v) ) > Int(6),
                   Count(AddNode, lambda addnode1: is_node_available(addnode1.node, var2.v)) < Int(4),
                    var1.v < var2.v)
                )
rule_10 = exist([AddEdge, AddEdge, AddEdge, AddEdge], lambda ae1, ae2, ae3, ae4:
                               AND(EQ(ae1.t, ae2.f),
                                   EQ(ae2.t, ae3.f),
                                   EQ(ae3.t, ae4.f)))

rule_11 = exist([Var, Var, Var, TimeStamp], lambda v1, v2, v3, t: AND( NEQ(v3.v, v1.v),
                                                                                is_node_available(v1.v, t.time),
                                                                                is_node_available(v2.v, t.time),
                                                                                is_node_available(v3.v, t.time),
                                                                                is_edge_available(v3.v, v2.v, t.time),
                                                                                is_edge_available(v1.v, v2.v, t.time)))



if __name__ == '__main__':
    args = sys.argv[1:]
    target_rule = globals()["rule_{}".format(args[0])]

    args = args[1:]

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


    start = time.time()
    '''
    TODO: Specify parameters, the following parameters need to 
    be changed based on parsed input  
    '''
    is_minimized = False
    complete_rules = add_background_theories(ACTION, state_action, complete_rules, bcr)
    check_property_refining(target_rule, set(), complete_rules, ACTION, state_action, True, min_solution=True,
                            final_min_solution=True, restart=restart, boundary_case=bcr, universal_blocking=ub)
    print(time.time() - start)
