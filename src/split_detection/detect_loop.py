def detect_loop(log):
    return False

def create_loop_partitions(log):
    activities = log.get_activities_by_label()
    start_activities = log.get_start_activities_by_label()
    end_activities = log.get_end_activities_by_label()
    eventually_follows_relations = log.get_evenually_follows_relations_by_label()

    partitions = []
    partition_1 = []

    saved_activities = []
    for activity in activities:
        if activity.activity_exists_by_label(start_activities) or activity.activity_exists_by_label(end_activities):
            partition_1.append(activity)
        else:
            saved_activities.append(activity)
    activities = saved_activities







    return False