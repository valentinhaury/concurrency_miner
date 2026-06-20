from data_structures import eventually_follows_relation
from data_structures.log import Log


def detect_arbitrary_order(log):
    return False

def create_arbitrary_order_partitions(log):
    eventually_follows_relations = log.get_eventually_follows_relations_by_label()
    overlapping_relation =log.get_overlapping_relations_by_label()
    partitions = []
    activities = log.get_activities_by_label()

    while activities:
        new_partition = [activities.pop()]
        partitions.append(new_partition)

        changed = True
        while changed:
            changed = False

            if not activities:
                break