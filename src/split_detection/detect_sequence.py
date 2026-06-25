from data_structures.eventually_follows_relation import EventuallyFollowsRelation
from src.data_structures.activity import Activity
from src.data_structures.log import Log
from src.data_structures.relation import Relation
from src.data_structures.trace import Trace
from src.data_structures.trace import Trace
from src.split_detection.detection_helper_functions import eventually_connected_in_only_one_direction, overlapping

def detect_sequence(log):
    return len(create_sequence_partitions(log)) > 1

def get_sequence_sublogs(log):
    partitions = create_sequence_partitions(log)
    sublogs = []
    for partition in partitions:
        sub_log = []
        for trace in log.get_traces():
            new_trace = Trace()
            for activity in trace.activities:
                if activity.activity_exists_by_label(partition):
                    new_trace.add_activity(activity)
            for relation in trace.get_directly_follows_relations():
                if relation.get_first_activity().activity_exists_by_label(new_trace.get_activities()) and relation.get_second_activity().activity_exists_by_label(new_trace.get_activities()):
                    new_trace.add_directly_follows_relation(relation)
            sub_log.append(new_trace)
        sublogs.append(Log(sub_log))

    return _sort_sublogs(sublogs, log.get_eventually_follows_relations_by_label())

def _sort_sublogs(sublogs, eventually_follows_relations):

    n = len(sublogs)
    for i in range(n-1):
      swapped = False
      for j in range(n-i-1):
        if _follows(sublogs[j],sublogs[j+1], eventually_follows_relations):
          sublogs[j], sublogs[j+1] = sublogs[j+1], sublogs[j]
          swapped = True
      if not swapped:
        break

    return sublogs

def _follows(log_a, log_b, eventually_follows_relations):
    for a1 in log_a.get_activities_by_label():
        for a2 in log_b.get_activities_by_label():
            if EventuallyFollowsRelation(a2, a1).relation_exists_by_label(eventually_follows_relations):
                return True
            elif EventuallyFollowsRelation(a1, a2).relation_exists_by_label(eventually_follows_relations):
                return False
    return False



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