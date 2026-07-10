import copy
from itertools import product, combinations

from src.data_structures.relation import Relation
from src.data_structures.log import Log
from src.data_structures.trace import Trace
from src.data_structures import directly_follows_relation
from src.data_structures.directly_follows_relation import DirectlyFollowsRelation
from src.split_detection.helper_functions import eventually_connected, direct_connected_id, overlapping, \
    connect_partitions


def detect_loop(log):
    return len(create_loop_partitions(log)) > 1

def get_loop_sublogs(log):
    partitions = create_loop_partitions(log)
    sublogs = []
    for partition in partitions:
        new_sublog = Log([])
        for trace in log.get_traces():
            trace_directly_follows_relation = trace.get_directly_follows_relations()
            trace_overlapping_relation = trace.get_overlapping_relations_by_id()

            activities = trace.get_activities()
            partition_activities = []
            for activity in activities:
                if activity.activity_exists_by_label(partition):
                    partition_activities.append(activity)

            while partition_activities:
                new_trace = Trace()
                changed = True
                while changed:
                    changed = False
                    saved_activities = []
                    for i in range(len(partition_activities)):
                        a1 = partition_activities.pop()
                        added = False
                        if not new_trace.get_activities():
                            new_trace.add_activity(a1)
                            added = True
                        else:
                            for a2 in new_trace.get_activities():
                                if direct_connected_id(a1, a2, trace_directly_follows_relation) or overlapping(a1, a2, trace_overlapping_relation):
                                    new_trace.add_activity(a1)
                                    changed = True
                                    added = True
                                    break
                        if not added:
                            saved_activities.append(a1)
                    partition_activities = saved_activities
                new_trace_activities = new_trace.get_activities()
                for relation in trace_directly_follows_relation:
                    if relation.get_first_activity() in new_trace_activities and relation.get_second_activity() in new_trace_activities:
                        new_trace.add_directly_follows_relation(relation)
                new_sublog.add_trace(new_trace)
        sublogs.append(new_sublog)

    return sublogs

def create_loop_partitions(event_log):
    log = copy.deepcopy(event_log)
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

# create all other partitions from the non-start and non-end activities
    while activities:
        new_partition = [activities.pop()]
        partitions.append(new_partition)

# merge partitions 2-n if they are connected
    changed = True
    while changed:
        changed = False
        for p1, p2 in combinations(partitions, 2):
            for a, b in product(p1, p2):
                if DirectlyFollowsRelation(a, b).relation_exists_by_label(directly_follows_relations) \
                    or DirectlyFollowsRelation(b, a).relation_exists_by_label(directly_follows_relations):
                    changed = True
                    break
            if changed:
                connect_partitions(p1[0], p2[0], partitions)
                break

# merge partitions to p1 if they can be directly reached from a start-activity that is no end-activity
#   or if an end-activity that is no start-activity can be directly reached from there
    start_and_not_end_activities = []
    end_and_not_start_activities = []
    for activity in start_activities:
        if not activity.activity_exists_by_label(end_activities):
            start_and_not_end_activities.append(activity)
    for activity in end_activities:
        if not activity.activity_exists_by_label(start_activities):
            end_and_not_start_activities.append(activity)

    saved_partitions = []
    while partitions:
        partition = partitions.pop()
        merge = False
        for activity in partition:
            for start_activity in start_and_not_end_activities:
                if DirectlyFollowsRelation(start_activity, activity).relation_exists_by_label(directly_follows_relations):
                    merge = True
                    break
            if merge: break
            for end_activity in end_and_not_start_activities:
                if DirectlyFollowsRelation(activity, end_activity).relation_exists_by_label(directly_follows_relations):
                    merge = True
                    break
            if merge: break
        if merge:
            partition_1.extend(partition)
        else:
            saved_partitions.append(partition)
    partitions = saved_partitions

# merge partitions to p1 if from a partition one but not all start-activities can be reached
#   or if a partition can be reached from one but not all end-activities
    saved_partitions = []
    while partitions:
        partition = partitions.pop()
        reaches_start_count = 0
        reached_by_end_count = 0
        for start in start_activities:
            for activity in partition:
                if DirectlyFollowsRelation(activity, start).relation_exists_by_label(directly_follows_relations):
                    reaches_start_count += 1
                    break
        for end in end_activities:
            for activity in partition:
                if DirectlyFollowsRelation(end, activity).relation_exists_by_label(directly_follows_relations):
                    reached_by_end_count += 1
                    break
        if 0 < reaches_start_count < len(start_activities):
            partition_1.extend(partition)
        elif 0 < reached_by_end_count < len(end_activities):
            partition_1.extend(partition)
        else:
            saved_partitions.append(partition)#
    partitions = saved_partitions

    partitions.insert(0, partition_1)
    return partitions




#old code
#merge activities to p1 if they can be directly reached from a start-activity that is no end-activity
#   or if and end-activity that is no start-activity can be directly reached from there
    saved_activities = []
    for activity in activities:
        merge = False
        for start_activity in start_activities:
            if not start_activity.activity_exists_by_label(end_activities):
                if DirectlyFollowsRelation(start_activity, activity).relation_exists_by_label(directly_follows_relations):
                    merge = True
        for end_activity in end_activities:
            if not end_activity.activity_exists_by_label(start_activities):
                if DirectlyFollowsRelation(activity, end_activity).relation_exists_by_label(directly_follows_relations):
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
