from itertools import product

from src.data_structures.log import Log
from src.data_structures.trace import Trace
from src.data_structures.eventually_follows_relation import EventuallyFollowsRelation
from src.data_structures.overlapping_relation import OverlappingRelation
from src.data_structures.directly_follows_relation import DirectlyFollowsRelation

def connect_partitions(activity_a, activity_b, partitions):
    partition_a = []
    partition_b = []
    for p1 in partitions:
        if activity_a.activity_exists_by_label(p1) and not activity_b.activity_exists_by_label(p1):
            for p2 in partitions:
                if activity_b.activity_exists_by_label(p2):
                    partition_a = p1
                    partition_b = p2
    if not partition_a == partition_b:
        partitions.remove(partition_a)
        partitions.remove(partition_b)
        new_partition = []
        new_partition.extend(partition_a)
        new_partition.extend(partition_b)
        partitions.append(new_partition)
    return partitions

def are_in_loop(a1, a2, log):
    start = log.get_start_activities_by_label()
    end = log.get_end_activities_by_label()
    if not a1.activity_exists_by_label(start) and not a1.activity_exists_by_label(end):
        return True
    if not a2.activity_exists_by_label(start) and not a2.activity_exists_by_label(end):
        return True
    return False

def fully_direct_connected(a1, a2, directly_follows_relations):
    if (DirectlyFollowsRelation(a1, a2).relation_exists_by_label(directly_follows_relations)
     and DirectlyFollowsRelation(a2, a1).relation_exists_by_label(directly_follows_relations)
     ):
        return True
    return False

def direct_connected_id(a1, a2, directly_follows_relations):
    if (DirectlyFollowsRelation(a1, a2).relation_exists_by_id(directly_follows_relations)
     or DirectlyFollowsRelation(a2, a1).relation_exists_by_id(directly_follows_relations)
     ):
        return True
    return False


def fully_eventually_connected_partitions(partition_1, partition_2, eventually_follows_relations):
    p1_follows_p2 = False
    p2_follows_p1 = False
    for a, b in product(partition_1, partition_2):
        if EventuallyFollowsRelation(a, b).relation_exists_by_label(eventually_follows_relations):
            p2_follows_p1 = True
        if EventuallyFollowsRelation(b, a).relation_exists_by_label(eventually_follows_relations):
            p1_follows_p2 = True
    return p1_follows_p2 and p2_follows_p1


def eventually_connected_in_only_one_direction(a1, a2, eventually_follows_relations):
    right = False
    left = False
    if EventuallyFollowsRelation(a1, a2).relation_exists_by_label(eventually_follows_relations):
        right = True
    if EventuallyFollowsRelation(a2, a1).relation_exists_by_label(eventually_follows_relations):
        left = True
    return right != left

def eventually_connected(a1, a2, eventually_follows_relations):
    if (EventuallyFollowsRelation(a1, a2).relation_exists_by_label(eventually_follows_relations)
            or EventuallyFollowsRelation(a2, a1).relation_exists_by_label(eventually_follows_relations)):
        return True
    return False

def overlapping(a1, a2, overlapping_relations):
    if (OverlappingRelation(a1, a2).relation_exists_by_label(overlapping_relations)
        or OverlappingRelation(a2, a1).relation_exists_by_label(overlapping_relations)):
        return True
    return False

def create_sublogs_sequential(log, partitions):
    sublogs = []
    for partition in partitions:
        sub_log = []
        for trace in log.get_traces():
            new_trace = Trace()
            for activity in trace.activities:
                if activity.activity_exists_by_label(partition):
                    new_trace.add_activity(activity)
            for relation in trace.get_directly_follows_relations():
                if relation.get_first_activity().activity_exists_by_label(new_trace.get_activities()) and relation.get_second_activity().activity_exists_by_label(new_trace.get_activities()):
                    new_trace.add_directly_follows_relation(relation)
            sub_log.append(new_trace)
        sublogs.append(Log(sub_log))

    return sublogs

def create_sublogs_concurrent(log, partitions):
    sublogs = []
    for partition in partitions:
        sub_log = []
        for trace in log.get_traces():
            new_trace = Trace()
            eventually_follows_relation_id = trace.get_eventually_follows_relations_by_id()
            for activity in trace.activities:
                if activity.activity_exists_by_label(partition):
                    new_trace.add_activity(activity)
            for relation in trace.get_directly_follows_relations():
                if relation.get_first_activity().activity_exists_by_label(new_trace.get_activities()) and relation.get_second_activity().activity_exists_by_label(new_trace.get_activities()):
                    new_trace.add_directly_follows_relation(relation)
            for a1 in new_trace.get_activities():
                for a2 in new_trace.get_activities():
                    if EventuallyFollowsRelation(a1, a2).relation_exists_by_id(eventually_follows_relation_id):
                        for a3 in new_trace.get_activities():
                            if  not (EventuallyFollowsRelation(a1, a3).relation_exists_by_id(eventually_follows_relation_id)
                                    and EventuallyFollowsRelation(a3, a2).relation_exists_by_id(eventually_follows_relation_id))\
                                and not DirectlyFollowsRelation(a1, a2).relation_exists_by_id(new_trace.get_directly_follows_relations()):
                                new_trace.add_directly_follows_relation(DirectlyFollowsRelation(a1, a2))
            sub_log.append(new_trace)
        sublogs.append(Log(sub_log))

    return sublogs