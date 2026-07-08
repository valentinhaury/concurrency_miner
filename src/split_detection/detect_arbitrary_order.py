import copy
from itertools import combinations

from src.data_structures.trace import Trace
from src.split_detection.helper_functions import create_sublogs_sequential, \
    connect_partitions, fully_eventually_connected_partitions
from src.data_structures.eventually_follows_relation import EventuallyFollowsRelation
from src.split_detection.helper_functions import overlapping
from src.data_structures import eventually_follows_relation
from src.data_structures.log import Log
from src.data_structures.overlapping_relation import OverlappingRelation


def detect_arbitrary_order(log):
    return len(create_arbitrary_order_partitions(log)) > 1

def get_arbitrary_order_sublogs(log):
    partitions = create_arbitrary_order_partitions(log)
    return create_sublogs_sequential(log, partitions)

def create_arbitrary_order_partitions(event_log):
    log = copy.deepcopy(event_log)
    log_eventually_follows_relations = log.get_eventually_follows_relations_by_label()
    log_overlapping_relations =log.get_overlapping_relations_by_label()
    partitions = []
    activities = log.get_activities_by_label()

    while activities:
        new_partition = [activities.pop()]
        partitions.append(new_partition)

    # connect partitions if activities are overlapping in log
    for relation in log_overlapping_relations:
        connect_partitions(relation.get_first_activity(), relation.get_second_activity(), partitions)

    # connect partitions if activities are not fully eventually connected in log
    changed = True
    while changed:
        changed = False
        for p1, p2 in combinations(partitions, 2):
            if not fully_eventually_connected_partitions(p1, p2, log_eventually_follows_relations):
                connect_partitions(p1[0], p2[0], partitions)
                changed = True
                break

    # connect partitions if they are fully eventually connected in one trace
    for trace in log.get_traces():
        trace_eventually_follows_relations = trace.get_eventually_follows_relations_by_label()
        changed = True
        while changed:
            changed = False
            for p1, p2 in combinations(partitions, 2):
                if fully_eventually_connected_partitions(p1, p2, trace_eventually_follows_relations):
                    connect_partitions(p1[0], p2[0], partitions)
                    changed = True
                    break

    return partitions

#old code / first solution not working on partitions - new solution above is better to describe (both should be equivalent)

    while activities:                                           #WHILE LOOP to create new partitions
        new_partition = [activities.pop()]
        changed = True
        while changed:                                          #WHILE LOOP to add all activities that belong to the new partition
            changed = False

            if not activities:
                break

            activities_save = []
            length_activities = len(activities)
            for i in range(length_activities):
                a2 = activities.pop()
                activity_added_to_partition = False

                for a1 in new_partition:
                    if overlapping(a1, a2, log_overlapping_relations):
                        activity_added_to_partition = True
                        if not a2.activity_exists_by_label(new_partition):
                            new_partition.append(a2)                            #Adding to partition if overlapping anywhere
                    if not fully_eventually_connected(a1, a2, log_eventually_follows_relations):
                        activity_added_to_partition = True
                        if not a2.activity_exists_by_label(new_partition):
                            new_partition.append(a2)                            #Adding to partition if not fully connected over all traces

                #TODO maybe outsource this check (next 12 lines) to helper functions
                fully_connected_in_one_trace = False
                for trace in log.get_traces():
                    left = 0
                    right = 0
                    trace_eventually_follows_relations = trace.get_eventually_follows_relations_by_label()
                    for a1 in new_partition:
                        if EventuallyFollowsRelation(a2, a1).relation_exists_by_label(trace_eventually_follows_relations):
                            left += 1
                        if EventuallyFollowsRelation(a1, a2).relation_exists_by_label(trace_eventually_follows_relations):
                            right += 1
                    if left > 0 and right > 0:
                        fully_connected_in_one_trace = True
                if fully_connected_in_one_trace:
                    activity_added_to_partition = True

                    if not a2.activity_exists_by_label(new_partition):
                        new_partition.append(a2)                                    #Adding to partition if fully connected in one trace
                if not activity_added_to_partition:
                    activities_save.append(a2)

            if not length_activities == len(activities_save):
                changed = True
            activities = activities_save

        partitions.append(new_partition)


    return partitions

