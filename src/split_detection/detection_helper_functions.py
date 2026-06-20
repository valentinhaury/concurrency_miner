from src.data_structures.directly_follows_relation import DirectlyFollowsRelation

def are_in_loop(a1, a2, log):
    start = log.get_start_activities_by_label()
    end = log.get_end_activities_by_label()
    if not a1.activity_exists_by_label(start) and not a1.activity_exists_by_label(end):
        return True
    if not a2.activity_exists_by_label(start) and not a2.activity_exists_by_label(end):
        return True
    return False

def fully_connected(a1, a2, directly_follows_relations):
    if (not DirectlyFollowsRelation(a1, a2).relation_exists_by_label(directly_follows_relations)
     or not DirectlyFollowsRelation(a2, a1).relation_exists_by_label(directly_follows_relations)
     ):
        return False
    return True