from src.data_structures.activity import Activity
from src.data_structures.eventually_follows_relation import EventuallyFollowsRelation
from src.data_structures.overlapping_relation import OverlappingRelation
from src.data_structures.relation import Relation

def only_one_eventually_follows_relations_exist(activity, activities, eventually_follows_relations):
    right = False
    left = False
    for a in activities:
        if EventuallyFollowsRelation(a, activity).relation_exists_by_label(eventually_follows_relations):
            right = True
        if EventuallyFollowsRelation(activity, a).relation_exists_by_label(eventually_follows_relations):
            left = True
    return right != left

def overlapping_relation_exists(activity, activities, overlapping_relations):
    for a in activities:
        if OverlappingRelation(a, activity).relation_exists_by_label(overlapping_relations):
            return True
    return False

def detect_sequence(log):
    eventually_follows_relations = log.get_eventually_follows_relations_by_label()
    overlapping_relations = log.get_overlapping_relations_by_label()
    activities = log.get_activities_by_label()
    if not activities:
        return False
    partition = [activities[0]]
    new_partition = ["true"]
    while new_partition:
        new_partition = []
        for a in activities:
            if (a not in partition
                    and (not only_one_eventually_follows_relations_exist(a,partition,eventually_follows_relations)
                    or overlapping_relation_exists(a,partition,overlapping_relations)
                    )
            ):
                new_partition.append(a)
        if new_partition:
            partition.extend(new_partition)

    return len(partition) != len(activities)