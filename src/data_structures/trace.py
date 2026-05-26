class Trace:
    def __init__(self, activities=None, relations=None):
        if relations is None:
            relations = []
        if activities is None:
            activities = []
        self.activities = activities
        self.relations = relations

    def append(self, item):
        self.activities.append(item)