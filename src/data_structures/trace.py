from src.data_structures.eventually_follows_relation import EventuallyFollowsRelation


class Trace:
    def __init__(self, activities=None, direct_relations=None):
        if direct_relations is None:
            direct_relations = []
        if activities is None:
            activities = []
        self.activities = activities
        self.direct_relations = direct_relations

    def __str__(self):
        trace_string = "[{"
        for activity in self.activities:
            trace_string += str(activity) + "; "
        trace_string += "}, {"
        for relation in self.direct_relations:
            trace_string += str(relation) + "; "
        trace_string += "}]"
        return trace_string

    def append_activity(self, activity):
        self.activities.append(activity)
    def append_relation(self, relation):
        self.direct_relations.append(relation)

    def contains_activity(self, activity):
        return activity in self.activities
    def contains_relation(self, relation):
        return relation in self.direct_relations

    def get_activities(self):
        return self.activities
    def get_relations(self):
        return self.direct_relations

    def get_eventually_relations(self):
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