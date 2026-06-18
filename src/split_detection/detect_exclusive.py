from src.data_structures.log import Log
from src.data_structures.trace import Trace


def detect_exclusive(log):
    if len(log.get_traces()) < 2:
        return False
    else:
        all_traces = log.get_traces()
        trace_partition = [all_traces[0]]
        changed_partition = ["true"]
        while changed_partition:
            changed_partition = {
                t2
                for t1 in trace_partition
                for t2 in all_traces
                if t2 not in trace_partition
                and not t1.has_disjunct_activities_to(t2)
            }
            trace_partition.extend(changed_partition)
        if len(all_traces) == len(trace_partition):
            return False
        else:
            return True