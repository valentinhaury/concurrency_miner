import copy
from idlelib.configdialog import changes
from itertools import combinations, product

from src.data_structures.overlapping_relation import OverlappingRelation
from src.data_structures.trace import Trace
from src.split_detection.helper_functions import overlapping, create_sublogs_concurrent, connect_partitions


def detect_parallel(log):
    return len(create_parallel_partitions(log)) > 1

def get_parallel_sublogs(log):
    partitions = create_parallel_partitions(log)
    return create_sublogs_concurrent(log, partitions)

def create_parallel_partitions(event_log):
    log = copy.deepcopy(event_log)
    activities = log.get_activities_by_label()
    traces = log.get_traces()
    partitions = []

    # initialize partitions
    while activities:
        new_partition = [activities.pop()]
        partitions.append(new_partition)

    # add all partitions if not every activity is overlapping every activity
    changed = True
    while changed:
        changed = False
        for p1, p2 in combinations(partitions, 2):
            for a, b in product(p1, p2):
                for trace in traces:
                    if not (OverlappingRelation(a, b).relation_exists_by_label(trace.get_overlapping_relations_by_label())
                        or OverlappingRelation(b, a).relation_exists_by_label(trace.get_overlapping_relations_by_label())):
                        changed = True
                        break
                if changed: break
            if changed:
                connect_partitions(p1[0], p2[0], partitions)
                break


    return partitions

    # old code not used anymore
    while activities:  # WHILE LOOP to create new partitions
        new_partition = [activities.pop()]
        changed = True
        while changed:  # WHILE LOOP to update the new_partition by adding activities until nothing changes
            changed = False
            activities_save = []
            length_activities = len(activities)
            for i in range(length_activities):  # for all activities that are in no partition check to see if they should be added
                a2 = activities.pop()
                in_partition = False
                for a1 in new_partition:  # for all activities in the new_partition check if they are overlapping in every trace:
                    for trace in traces:
                        if not overlapping(a1, a2, trace.get_overlapping_relations_by_label()):
                            in_partition = True
                if in_partition:
                    if not a2.activity_exists_by_label(new_partition):
                        new_partition.append(a2)
                else:
                    activities_save.append(a2)
            if not length_activities == len(activities_save):
                changed = True
            activities = activities_save
        partitions.append(new_partition)
    return partitions