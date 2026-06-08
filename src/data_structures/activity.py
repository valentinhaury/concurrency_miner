import uuid

class Activity:
    def __init__(self, activity_label):
        self.label = activity_label
        self.id = uuid.uuid4()

    def __str__(self):
        return self.label

    def __eq__(self, other):
        return self.label == other.label

    def __hash__(self):
        return hash(self.label)

    def has_same_id(self, other):
        return self.id == other.id