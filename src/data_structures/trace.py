from itertools import combinations

from src.data_structures.directly_follows_relation import DirectlyFollowsRelation
from src.data_structures.overlapping_relation import OverlappingRelation
from src.data_structures.eventually_follows_relation import EventuallyFollowsRelation

class Trace:
    def __init__(self, activities=None, directly_follows_relations=None):
        if directly_follows_relations is None:
            directly_follows_relations = []
        if activities is None:
            activities = []
        self.activities = activities
        self.directly_follows_relations = directly_follows_relations

    def append_activity(self, activity):
        self.activities.append(activity)
    def append_directly_follows_relation(self, relation):
        self.directly_follows_relations.append(relation)

    def is_empty_trace(self):
        if self.activities:
            return False
        return True

    def has_disjunct_activities_to(self, other):
        duplicate = [a for a in self.activities if a.label_occurs_at_least(other.get_activities(), 1)]
        if duplicate:
            return False
        return True


    def get_activities(self):
        return self.activities
    def get_directly_follows_relations(self):
        return self.directly_follows_relations

    def get_overlapping_relations(self):
        eventually_follows_relations = self.get_eventually_follows_relations()

        return [
            OverlappingRelation(a1, a2)
            for a1, a2 in combinations(self.activities, 2)
            if not EventuallyFollowsRelation(a1, a2).exists_by_label(eventually_follows_relations)
               and not EventuallyFollowsRelation(a2, a1).exists_by_label(eventually_follows_relations)
        ]

    def get_eventually_follows_relations(self):
        return True

    def __str__(self):
        trace_string = "(A{"
        if self.activities:
            for activity in self.activities:
                trace_string += str(activity) + ", "
            trace_string = trace_string[:-2]
        trace_string += "}, R{"
        if self.directly_follows_relations:
            for relation in self.directly_follows_relations:
                trace_string += str(relation) + ", "
            trace_string = trace_string[:-2]
        trace_string += "})"
        return trace_string