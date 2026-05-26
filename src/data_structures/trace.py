class Trace:
    def __init__(self, activities=None, relations=None):
        if relations is None:
            relations = []
        if activities is None:
            activities = []
        self.activities = activities
        self.relations = relations

    def append_activity(self, activity):
        self.activities.append(activity)

    def append_relation(self, relation):
        self.relations.append(relation)

    def contains_activity(self, activity):
        return activity in self.activities

    def contains_relation(self, relation):
        return relation in self.relations