from src.data_structures.overlapping_relation import OverlappingRelation
from src.split_detection.detection_helper_functions import are_in_loop, fully_direct_connected, overlapping


def detect_interleafing(log):
    return len(create_interleafing_partitions(log)) > 1

def create_interleafing_partitions(log):
    directly_follows_relations = log.get_directly_follows_relations_by_label()
    overlapping_relations = log.get_overlapping_relations_by_label()
    activities = log.get_activities_by_label()
    partitions = []

    while activities:                                           #WHILE LOOP to create new partitions
        new_partition = [activities.pop()]
        partitions.append(new_partition)

        changed = True
        while changed:                                          #WHILE LOOP to update partitions by adding activities until nothing changes
            changed = False
            if not activities:
                break
                                                                #TODO Maybe i just need to run the following for the new_partition and not for all partitions in partitions
            for partition in partitions:                        #check all existing partitions
                if not activities:
                    break
                for a1 in partition:                            #for all activities in the current partition check:
                    activities_save = []
                    length_activities = len(activities)
                    for i in range(length_activities):          #for all activities that are in no partition check to see if they should be added
                        a2 = activities.pop()
                        if overlapping(a1, a2, overlapping_relations):
                            if not a2.activity_exists_by_label(partition):
                                partition.append(a2)
                        elif not fully_direct_connected(a1, a2, directly_follows_relations):
                            if not a2.activity_exists_by_label(partition):
                                partition.append(a2)
                        elif are_in_loop(a1, a2, log):
                            if not a2.activity_exists_by_label(partition):
                                partition.append(a2)
                        else:
                            activities_save.append(a2)
                    if not length_activities == len(activities_save):
                        changed = True
                    activities = activities_save

    return partitions