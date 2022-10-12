from type_constructor import create_type, create_action, create_pair_action
from random import randint
type_dict = dict()

N = 10000
nat = create_type("nat", type_dict, lower_bound=0, upper_bound=N)
time = create_type("time", type_dict, lower_bound=0)

Magic = create_action("Magic", [("x", "nat"), ("y", "nat"), ("time", "time")],type_dict)
TimeStamp = create_action("TimeStamp", [("time", "time")],type_dict)


ACTION = [TimeStamp, Magic]
state_action = [TimeStamp]
