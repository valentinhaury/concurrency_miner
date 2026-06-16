from src.data_structures.log import Log
from src.data_structures.trace import Trace


def detect_exclusive(log):
    if log.number_of_traces() < 2:
        return False
    else:
        all_traces = log.get_traces()
        partition = [all_traces[0]]
        changed = True
        while changed:
            changed = False
            not_disjoint = []
            for trace in partition:
                for trace2 in all_traces:
                    if not set(trace.get_activities()).isdisjoint(set(trace2.get_activities())) and trace2 not in not_disjoint and trace2 not in partition:
                        not_disjoint.append(trace2)
                        changed = True
            if not_disjoint:
                for trace in not_disjoint:
                    partition.append(trace)
        if len(all_traces) == len(partition):
            return False
        else:
            return True