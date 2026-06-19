from data_structures.directly_follows_relation import DirectlyFollowsRelation
from data_structures.overlapping_relation import OverlappingRelation


def detect_interleafing(log):
    directly_follows_relations = log.get_directly_follows_relations_by_label()
    activities = log.get_activities_by_label()

    return False

def are_in_loop(a1, a2):
    return True

def create_interleafing_partitions(log):
    directly_follows_relations = log.get_directly_follows_relations_by_label()
    overlapping_relations = log.get_overlapping_relations_by_label()
    activities = log.get_activities_by_label()

    partitions = []
    if not activities:
        return []

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
                    if OverlappingRelation(a1, a2).exists_by_label(overlapping_relations):
                        partition.append(a2)
                    elif (not DirectlyFollowsRelation(a1, a2).exists_by_label(directly_follows_relations)
                        or not DirectlyFollowsRelation(a2, a1).exists_by_label(directly_follows_relations)
                        and a2 not in partition):
                        partition.append(a2)
                    elif are_in_loop(a1, a2):
                        partition.append(a2)
                    else:
                        activities_save.append(a2)
                if not length_activities == len(activities_save):
                    changed = True
                activities = activities_save


    return partitions