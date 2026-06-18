from itertools import combinations

from src.data_structures.directly_follows_relation import DirectlyFollowsRelation
from src.data_structures.overlapping_relation import OverlappingRelation
from src.data_structures.eventually_follows_relation import EventuallyFollowsRelation

class Trace:
    def __init__(self, activities=None,direct_relations=None):
        if direct_relations is None:
            direct_relations = []
        if activities is None:
            activities = []
        self.activities = activities
        self.direct_relations = direct_relations

    def append_activity(self, activity):
        self.activities.append(activity)
    def append_directly_follows_relation(self, relation):
        self.direct_relations.append(relation)

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
        return self.direct_relations

    def get_overlapping_relations(self):
        eventually_follows = set(self.get_eventually_follows_relations())

        return [
            OverlappingRelation(a1, a2)
            for a1, a2 in combinations(self.activities, 2)
            if EventuallyFollowsRelation(a1, a2) not in eventually_follows
               and EventuallyFollowsRelation(a2, a1) not in eventually_follows
        ]

    def get_eventually_follows_relations(self):
        closure = set()

        for r in self.direct_relations:
            closure.add((r.get_first_activity(), r.get_second_activity()))

        changed = True
        while changed:
            changed = False
            new_edges = set()

            for a, b in closure:
                for c, d in closure:
                    if b == c:
                        edge = (a, d)
                        if edge not in closure:
                            new_edges.add(edge)
                            changed = True

            closure.update(new_edges)

        return [
            EventuallyFollowsRelation(a, b)
            for a, b in closure
        ]

    def __str__(self):
        trace_string = "(A{"
        if self.activities:
            for activity in self.activities:
                trace_string += str(activity) + ", "
            trace_string = trace_string[:-2]
        trace_string += "}, R{"
        if self.direct_relations:
            for relation in self.direct_relations:
                trace_string += str(relation) + ", "
            trace_string = trace_string[:-2]
        trace_string += "})"
        return trace_string