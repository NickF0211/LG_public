from type_constructor import create_type, create_action, create_pair_action
type_dict = dict()

player = create_type("player", type_dict, lower_bound=1)
time = create_type("time", type_dict, lower_bound=0)

Play = create_action("Play", [("a", "player"), ("b", "player"), ("time", "time")],type_dict)
Friend = create_action("Friend", [("a", "player"), ("b", "player"), ("time", "time")],type_dict)
TimeStamp = create_action("TimeStamp", [("time", "time")],type_dict)


ACTION = [TimeStamp, Play, Friend]
state_action = [TimeStamp]
