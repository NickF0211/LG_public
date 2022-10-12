def multisort(xs, specs):
    for key, reverse in reversed(specs):
        xs.sort(key=key, reverse=reverse)
    return xs



def print_trace(model, ACTION, state_action, include_temp = False, should_print=True, ignore_class = None):
    all_objects = []
    for action in ACTION:
        if include_temp:
            all_objects += action.snap_shot
        else:
            all_objects += action.collect_list

    filtered_objects = filter(lambda obj: model.get_py_value(obj.presence) and hasattr(obj, "time"), all_objects)
    sorted_objects = multisort(list(filtered_objects), [(lambda obj: model.get_py_value(obj.time), False),
                     (lambda obj: type(obj) in state_action, True)])
    old_res = ""
    vol  = 0
    entry = set()
    for obj in sorted_objects:
        if ignore_class is not None and type(obj) in ignore_class:
            continue
        res = obj.get_record(model, debug= False)
        entry.add(res)
        if res != old_res:
            if should_print:
                print(res)
            vol += 1
        old_res = res
    return len(entry)
