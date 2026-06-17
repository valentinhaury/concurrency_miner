import uuid

class Activity:
    def __init__(self, activity_label):
        self.label = activity_label
        self.id = uuid.uuid4()

    def __str__(self):
        return self.label

    def __eq__(self, other):
        if not isinstance(other, Activity):
            return NotImplemented
        return self.label == other.label

    def __hash__(self):
        return hash(self.label)

    def has_same_id_as(self, other):
        return self.id == other.id

    def label_occurs_at_least(self, activities, count):
        occurrences = sum(
            1 for activity in activities
            if activity.has_same_label_as(self)
        )
        return occurrences >= count