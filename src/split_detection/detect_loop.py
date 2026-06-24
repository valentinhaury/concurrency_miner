from src.data_structures import directly_follows_relation
from src.data_structures.directly_follows_relation import DirectlyFollowsRelation
from src.split_detection.detection_helper_functions import eventually_connected


def detect_loop(log):
    return len(create_loop_partitions(log)) > 1

def create_loop_partitions(log):
    activities = log.get_activities_by_label()
    start_activities = log.get_start_activities_by_label()
    end_activities = log.get_end_activities_by_label()
    eventually_follows_relations = log.get_eventually_follows_relations_by_label()
    directly_follows_relations = log.get_directly_follows_relations_by_label()

    partitions = []
    partition_1 = []
#create partition 1 where all start and end activities are
    saved_activities = []
    for activity in activities:
        if activity.activity_exists_by_label(start_activities) or activity.activity_exists_by_label(end_activities):
            partition_1.append(activity)
        else:
            saved_activities.append(activity)
    activities = saved_activities


#merge activities to p1 if they can be directly reached from a start-activity that is no end-activity
#   or if and end-activity that is no start-activity can be directly reached from there
    saved_activities = []
    for activity in activities:
        merge = False
        for start_activity in start_activities:
            if not start_activity.activity_exists_by_label(end_activities):
                if DirectlyFollowsRelation(start_activity, activity):
                    merge = True
        for end_activity in end_activities:
            if not end_activity.activity_exists_by_label(start_activities):
                if DirectlyFollowsRelation(activity, end_activity):
                    merge = True
        if merge:
            partition_1.append(activity)
        else:
            saved_activities.append(activity)
    activities = saved_activities

#merge activities to p1 if from an activity one but not all start-activities can be reached
#   or if an activity can be reached from one but not all end-activities
    saved_activities = []
    for activity in activities:
        reaches_start_count = 0
        reached_by_end_count = 0
        for start_activity in start_activities:
            if DirectlyFollowsRelation(activity, start_activity).relation_exists_by_label(directly_follows_relations):
                reaches_start_count += 1
        for end_activity in end_activities:
            if DirectlyFollowsRelation(end_activity, activity).relation_exists_by_label(directly_follows_relations):
                reached_by_end_count += 1
        if (not (reaches_start_count == 0 or reaches_start_count == len(start_activities))
            or not (reached_by_end_count == 0 or reached_by_end_count == len(end_activities))):
            partition_1.append(activity)
        else:
            saved_activities.append(activity)
    activities = saved_activities

# merge partitions if they are connected
    while activities:
        new_partition = [activities.pop()]
        if not activities:
            partitions.append(new_partition)
            break
        saved_activities = []
        changed = True
        while changed:
            changed = False
            for a1 in activities:
                in_partition = False
                for a2 in new_partition:
                    if eventually_connected(a1, a2, eventually_follows_relations):
                        changed = True
                        in_partition = True
                if in_partition:
                    if not a1.activity_exists_by_label(new_partition):
                        new_partition.append(a1)
                else:
                    saved_activities.append(a1)
            activities = saved_activities

    partitions.insert(0, partition_1)
    return partitions
