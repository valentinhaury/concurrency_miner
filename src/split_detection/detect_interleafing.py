from src.data_structures.directly_follows_relation import DirectlyFollowsRelation
from src.data_structures.eventually_follows_relation import EventuallyFollowsRelation
from src.data_structures.log import Log
from src.data_structures.trace import Trace
from src.data_structures.overlapping_relation import OverlappingRelation
from src.split_detection.detection_helper_functions import are_in_loop, fully_direct_connected, overlapping

def detect_interleafing(log):
    return len(create_interleafing_partitions(log)) > 1

def get_interleafing_sublogs(log):
    partitions = create_interleafing_partitions(log)
    sublogs = []
    for partition in partitions:
        sub_log = []
        for trace in log.get_traces():
            new_trace = Trace()
            eventually_follows_relation_id = trace.get_eventually_follows_relations_by_id()
            for activity in trace.activities:
                if activity.activity_exists_by_label(partition):
                    new_trace.add_activity(activity)
            for relation in trace.get_directly_follows_relations():
                if relation.get_first_activity().activity_exists_by_label(new_trace.get_activities()) and relation.get_second_activity().activity_exists_by_label(new_trace.get_activities()):
                    new_trace.add_directly_follows_relation(relation)
            for a1 in new_trace.get_activities():
                for a2 in new_trace.get_activities():
                    if EventuallyFollowsRelation(a1, a2).relation_exists_by_id(eventually_follows_relation_id)\
                        and not OverlappingRelation(a1, a2).relation_exists_by_id(trace.get_overlapping_relations_by_id()):
                        for a3 in new_trace.get_activities():
                            if  not (EventuallyFollowsRelation(a1, a3).relation_exists_by_id(eventually_follows_relation_id)
                                    and EventuallyFollowsRelation(a3, a2).relation_exists_by_id(eventually_follows_relation_id))\
                                and not EventuallyFollowsRelation(a1, a2).relation_exists_by_id(new_trace.get_eventually_follows_relations_by_id()):
                                new_trace.add_directly_follows_relation(DirectlyFollowsRelation(a1, a2))
            sub_log.append(new_trace)
        sublogs.append(Log(sub_log))

    return sublogs


def create_interleafing_partitions(log):
    directly_follows_relations = log.get_directly_follows_relations_by_label()
    overlapping_relations = log.get_overlapping_relations_by_label()
    activities = log.get_activities_by_label()
    partitions = []

    while activities:                                           #WHILE LOOP to create new partitions
        new_partition = [activities.pop()]
        partitions.append(new_partition)
        changed = True
        while changed:                                          #WHILE LOOP to update the new_partition by adding activities until nothing changes
            changed = False

            for a1 in new_partition:                            #for all activities in the new_partition check:
                activities_save = []
                length_activities = len(activities)
                for i in range(length_activities):          #for all activities that are in no partition check to see if they should be added
                    a2 = activities.pop()
                    if overlapping(a1, a2, overlapping_relations):
                        if not a2.activity_exists_by_label(new_partition):
                            new_partition.append(a2)
                    elif not fully_direct_connected(a1, a2, directly_follows_relations):
                        if not a2.activity_exists_by_label(new_partition):
                            new_partition.append(a2)
                    elif are_in_loop(a1, a2, log):
                        if not a2.activity_exists_by_label(new_partition):
                            new_partition.append(a2)
                    else:
                        activities_save.append(a2)
                if not length_activities == len(activities_save):
                    changed = True
                activities = activities_save

    return partitions