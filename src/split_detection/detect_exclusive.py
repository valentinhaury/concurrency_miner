from src.data_structures.log import Log
from src.data_structures.trace import Trace


def detect_exclusive(log):
    return len(create_exclusive_choice_partitions(log)) > 1

def create_exclusive_choice_partitions(log):
    traces = log.get_traces()
    if len(traces) == 0:
        return []
    if len(traces) == 1:
        return [[traces.pop()]]

    trace_partitions = []

    while traces:
        trace_partition = [traces.pop()]
        saved_traces = []
        while traces:
            t2 = traces.pop()
            disjunct = True
            for t1 in trace_partition:
                if not t1.has_disjunct_activities_to(t2):
                    disjunct = False
            if not disjunct:
                trace_partition.append(t2)
            else:
                saved_traces.append(t2)
        traces = saved_traces
        trace_partitions.append(trace_partition)

    return trace_partitions




