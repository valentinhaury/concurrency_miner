from data_structures.activity import Activity

def handle_empty_traces(log):
    for trace in log.get_traces():
        if trace.is_empty_trace():
            trace.add_activity(Activity("tau"))
