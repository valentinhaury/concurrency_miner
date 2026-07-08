import copy
from itertools import combinations

from src.split_detection.helper_functions import are_in_loop, fully_direct_connected, overlapping, \
    create_sublogs_concurrent, connect_partitions, not_fully_direct_connected_relation, \
    are_in_loop_partitions  # , minimum_self_distance_relation


def detect_interleafing(log):
    return len(create_interleafing_partitions(log)) > 1

def get_interleafing_sublogs(log):
    partitions = create_interleafing_partitions(log)
    return create_sublogs_concurrent(log, partitions)

def create_interleafing_partitions(event_log):
    log = copy.deepcopy(event_log)
    directly_follows_relations = log.get_directly_follows_relations_by_label()
    overlapping_relations = log.get_overlapping_relations_by_label()
    activities = log.get_activities_by_label()
    partitions = []

    while activities:
        new_partition = [activities.pop()]
        partitions.append(new_partition)

    # merge overlapping partitions
    for relation in overlapping_relations:
        connect_partitions(relation.get_first_activity(), relation.get_second_activity(), partitions)

    # merge not fully direct connected partitions
    for relation in not_fully_direct_connected_relation(log.get_activities_by_label(), directly_follows_relations):
        connect_partitions(relation.get_first_activity(), relation.get_second_activity(), partitions)

    # merge partitions with minimum self distance relationship
    changed = True
    while changed:
        changed = False
        for p1, p2 in combinations(partitions, 2):
            if are_in_loop_partitions(p1, p2, log):
                connect_partitions(p1[0], p2[0], partitions)
                changed = True
                break

    return partitions
    #for relation in minimum_self_distance_relation(log):
    #    connect_partitions(relation.get_first_activity(), relation.get_second_activity(), partitions)

    # connect partitions with no start or no end activity to an arbitrary partition



    while activities:                                           #WHILE LOOP to create new partitions
        new_partition = [activities.pop()]
        partitions.append(new_partition)
        changed = True
        while changed:                                          #WHILE LOOP to update the new_partition by adding activities until nothing changes
            changed = False

            for a1 in new_partition:                            #for all activities in the new_partition check:
                activities_save = []
                length_activities = len(activities)
                for i in range(length_activities):          #for all activities that are in no partition check to see if they should be added
                    a2 = activities.pop()
                    if overlapping(a1, a2, overlapping_relations):
                        if not a2.activity_exists_by_label(new_partition):
                            new_partition.append(a2)
                    elif not fully_direct_connected(a1, a2, directly_follows_relations):
                        if not a2.activity_exists_by_label(new_partition):
                            new_partition.append(a2)
                    elif are_in_loop(a1, a2, log):
                        if not a2.activity_exists_by_label(new_partition):
                            new_partition.append(a2)
                    else:
                        activities_save.append(a2)
                if not length_activities == len(activities_save):
                    changed = True
                activities = activities_save

    return partitions