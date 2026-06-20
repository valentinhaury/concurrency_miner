from itertools import product

from src.data_structures.relation import Relation
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

    def append_activity(self, activity):
        self.activities.append(activity)

    def append_directly_follows_relation(self, relation):
        self.directly_follows_relations.append(relation)

    def is_empty_trace(self):
        if self.activities:
            return False
        return True

    def has_disjunct_activities_to(self, other):
        duplicate = [a for a in self.activities if a.activity_exists_by_label(other.get_activities())]
        if duplicate:
            return False
        return True

    def get_activities(self):
        return self.activities

    def get_start_activities(self):
        start_activities = []
        if self.activities:
            for a1 in self.activities:
                checked = True
                for a2 in self.activities:
                    if DirectlyFollowsRelation(a2, a1).relation_exists_by_id(self.directly_follows_relations):
                        checked = False
                if checked and  not a1.activity_exists_by_label(start_activities):
                    start_activities.append(a1)
        return start_activities

    def get_end_activities(self):
        end_activities = []
        if self.activities:
            for a1 in self.activities:
                checked = True
                for a2 in self.activities:
                    if DirectlyFollowsRelation(a1, a2).relation_exists_by_id(self.directly_follows_relations):
                        checked = False
                if checked and not a1.activity_exists_by_label(end_activities):
                    end_activities.append(a1)
        return end_activities

    def get_directly_follows_relations(self):
        return self.directly_follows_relations

    def get_directly_follows_relations_by_label(self):
        dfg_by_label = []
        if self.directly_follows_relations:
            for relation in self.directly_follows_relations:
                if not relation.relation_exists_by_label(dfg_by_label):
                    dfg_by_label.append(relation)
        return dfg_by_label

    def get_overlapping_relations_by_label(self):
        eventually_follows_relations = self.get_eventually_follows_relations_by_label()
        return [
            OverlappingRelation(a1, a2)
            for a1, a2 in product(self.activities, repeat = 2)
            if not EventuallyFollowsRelation(a1, a2).relation_exists_by_label(eventually_follows_relations)
               and not EventuallyFollowsRelation(a2, a1).relation_exists_by_label(eventually_follows_relations)
        ]

    def get_eventually_follows_relations_by_label(self):
        eventually_follows_relations = []
        for relation in self.directly_follows_relations:
           eventually_follows_relations.append(EventuallyFollowsRelation(relation.get_first_activity(), relation.get_second_activity()))

        added_relations = ["true"]
        while added_relations:
            added_relations = [
                EventuallyFollowsRelation(a1, a2)
                for a1, a2 in product(self.activities, repeat=2)
                for a3 in self.activities
                if not Relation(a1, a2).relation_exists_by_label(eventually_follows_relations)
                   and Relation(a1, a3).relation_exists_by_label(eventually_follows_relations)
                   and Relation(a3, a2).relation_exists_by_label(eventually_follows_relations)
            ]

            if added_relations:
                for relation in added_relations:
                    if not relation.relation_exists_by_label(eventually_follows_relations):
                        eventually_follows_relations.append(relation)
        return eventually_follows_relations



