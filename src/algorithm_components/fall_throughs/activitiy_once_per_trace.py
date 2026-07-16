import copy


def detect_activity_once_per_trace(event_log):
    log = copy.deepcopy(event_log)
    if get_activities_once_per_trace(log):
        return True
    else:
        return False

def get_activities_once_per_trace(event_log):
    log = copy.deepcopy(event_log)
    activities = []
    candidates = log.get_activities_by_label()
    for candidate in candidates:
        once_per_trace = True
        for trace in log.get_traces():
            count = 0
            for activity in trace.get_activities():
                if activity.get_label() == candidate.get_label():
                    count += 1
            if count != 1:
                once_per_trace = False
                break
        if once_per_trace:
            activities.append(candidate)
    return activities