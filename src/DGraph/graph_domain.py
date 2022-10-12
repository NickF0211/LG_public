from type_constructor import create_type, create_action, create_pair_action
from random import randint
type_dict = dict()

'''
TODO: define your data type here
'''
_int = create_type("int", type_dict)
t = create_type("time", type_dict, lower_bound=0)
var = create_type("var", type_dict)

#other data types....
node_id = create_type("node", type_dict)


'''
TODO: define your data actions here: INPUT
'''
Var = create_action("Var", [("v", "var")],type_dict)
TimeStamp = create_action("TimeStamp", [("time", "time")],type_dict)
AddNode = create_action("AddNode", [("node", "node"), ("time", "time")], type_dict)
AddEdge = create_action("AddEdge", [("f", "node"), ("t", "node"), ("time", "time")], type_dict)
RemoveNode = create_action("removeNode", [("node", "node"), ("time", "time")], type_dict)
RemoveEdge = create_action("removeEdge", [("f", "node"), ("t", "node"), ("time", "time")], type_dict)

'''
TODO: record the complete list of data actions: INPUT
'''
ACTION = [TimeStamp, Var, AddNode, AddEdge, RemoveNode, RemoveEdge]

'''
TODO: Hidden or AUX data actions: INPUT
'''
state_action = [TimeStamp]

