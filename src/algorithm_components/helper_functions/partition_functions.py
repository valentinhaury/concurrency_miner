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

def add_partitions_with_no_start_or_end_to_arbitrary(partitions, start_activities, end_activities):
    changed = True
    while changed:
        changed = False
        if len(partitions) <= 1:
            continue
        i = 0
        for partition in partitions:
            has_start = False
            has_end = False
            for activity in partition:
                if activity.activity_exists_by_label(start_activities):
                    has_start = True
                if activity.activity_exists_by_label(end_activities):
                    has_end = True
            if not has_start and not has_end:
                if i == 0:
                    connect_partitions(partitions[0][0], partitions[1][0], partitions)
                if i > 0:
                    connect_partitions(partitions[i][0], partitions[0][0], partitions)
                changed = True
            i += 1
    return partitions
