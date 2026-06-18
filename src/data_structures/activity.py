import uuid

class Activity:
    def __init__(self, activity_label):
        self.label = activity_label
        self.id = uuid.uuid4()

    def __repr__(self):
        return f"<Activity \"{self.label}\" with id {self.id}>"

    def __str__(self):
        return self.label

    def get_id(self):
        return self.id

    def get_label(self):
        return self.label

    def exists_by_label(self, activities):
        count = 0
        occurrences = sum(
            1 for activity in activities
            if activity.get_label() == self.label
        )
        return occurrences > count