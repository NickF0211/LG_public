from type_constructor import create_type, create_action, create_pair_action
from random import randint
type_dict = dict()
eid = create_type("uid", type_dict, lower_bound=0)
tid = create_type("tid", type_dict, lower_bound=0)
amount = create_type("amount", type_dict, lower_bound=0)
time = create_type("time", type_dict, lower_bound=0)

Trans = create_action("Transfer", [("sender", "uid"), ("receiver", "uid"),("id", "tid"),("amount", "amount"), ("time", "time")],type_dict)
Depo = create_action("Deposite", [("user", "uid"), ("amount", "amount"),("id", "tid"),("time", "time")],type_dict)
Withdraw = create_action("Withdraw", [("user", "uid"), ("amount", "amount"),("id", "tid"),("time", "time")],type_dict)
TimeStamp = create_action("TimeStamp", [("time", "time")],type_dict)


ACTION = [TimeStamp, Trans, Depo, Withdraw]
state_action = [TimeStamp]

thresh = randint(1, 1000000)