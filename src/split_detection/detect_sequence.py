from src.split_detection.detection_helper_functions import eventually_connected_in_only_one_direction, overlapping



def detect_sequence(log):
    return len(create_sequence_partitions(log)) > 1

def create_sequence_partitions(log):
    eventually_follows_relations = log.get_eventually_follows_relations_by_label()
    overlapping_relations = log.get_overlapping_relations_by_label()
    activities = log.get_activities_by_label()

    partitions = []
    while activities:
        new_partition = [activities.pop()]
        changed = True
        while changed:
            changed = False
            saved_activities = []
            for a1 in activities:
                in_partition = False
                for a2 in new_partition:
                    if (overlapping(a1, a2, overlapping_relations)
                            or not eventually_connected_in_only_one_direction(a1, a2, eventually_follows_relations)):
                        in_partition = True
                if in_partition:
                    if not a1.activity_exists_by_label(new_partition):
                        new_partition.append(a1)
                        changed = True
                else:
                    saved_activities.append(a1)
            activities = saved_activities
        partitions.append(new_partition)

    return partitions