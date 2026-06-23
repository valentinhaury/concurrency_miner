from src.split_detection.detection_helper_functions import fully_direct_connected, overlapping


def detect_concurrent(log):
    return len(create_concurrent_partitions(log)) > 1

def create_concurrent_partitions(log):
    directly_follows_relations = log.get_directly_follows_relations_by_label()
    overlapping_relations = log.get_overlapping_relations_by_label()
    activities = log.get_activities_by_label()
    partitions = []

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
                for a1 in new_partition:  # for all activities in the new_partition check:
                    if not overlapping(a1, a2, overlapping_relations):
                        in_partition = True
                    if not fully_direct_connected(a1, a2, directly_follows_relations):
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