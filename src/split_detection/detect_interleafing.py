from src.data_structures.directly_follows_relation import DirectlyFollowsRelation
from src.data_structures.overlapping_relation import OverlappingRelation


def detect_interleafing(log):
    return len(create_interleafing_partitions(log)) > 1

def fully_connected(a1, a2, directly_follows_relations):
    if (not DirectlyFollowsRelation(a1, a2).relation_exists_by_label(directly_follows_relations)
     or not DirectlyFollowsRelation(a2, a1).relation_exists_by_label(directly_follows_relations)
     ):
        return False
    return True

def are_in_loop(a1, a2, log):
    start = log.get_start_activities_by_label()
    end = log.get_end_activities_by_label()
    if not a1.activity_exists_by_label(start) and not a1.activity_exists_by_label(end):
        return True
    if not a2.activity_exists_by_label(start) and not a2.activity_exists_by_label(end):
        return True
    return False

def create_interleafing_partitions(log):
    directly_follows_relations = log.get_directly_follows_relations_by_label()
    overlapping_relations = log.get_overlapping_relations_by_label()
    activities = log.get_activities_by_label()
    partitions = []

    while activities:
        new_partition = [activities.pop()]
        partitions.append(new_partition)

        changed = True
        while changed:
            changed = False
            if not activities:
                break
            for partition in partitions:
                if not activities:
                    break
                for a1 in partition:
                    activities_save = []
                    length_activities = len(activities)
                    for i in range(length_activities):
                        a2 = activities.pop()
                        if OverlappingRelation(a1, a2).relation_exists_by_label(overlapping_relations) or OverlappingRelation(a2, a1).relation_exists_by_label(overlapping_relations):
                            if a2 not in partition:
                                partition.append(a2)
                        elif not fully_connected(a1, a2, directly_follows_relations):
                            if a2 not in partition:
                                partition.append(a2)
                        elif are_in_loop(a1, a2, log):
                            if a2 not in partition:
                                partition.append(a2)
                        else:
                            activities_save.append(a2)
                    if not length_activities == len(activities_save):
                        changed = True
                    activities = activities_save

    return partitions