from src.data_structures.eventually_follows_relation import EventuallyFollowsRelation
from src.data_structures.overlapping_relation import OverlappingRelation
from src.data_structures.directly_follows_relation import DirectlyFollowsRelation

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

def fully_eventually_connected(a1, a2, eventually_follows_relations):
    if (EventuallyFollowsRelation(a1, a2).relation_exists_by_label(eventually_follows_relations)
        and EventuallyFollowsRelation(a2, a1).relation_exists_by_label(eventually_follows_relations)):
        return True
    return False

def overlapping(a1, a2, overlapping_relations):
    if (OverlappingRelation(a1, a2).relation_exists_by_label(overlapping_relations)
        or OverlappingRelation(a2, a1).relation_exists_by_label(overlapping_relations)):
        return True
    return False