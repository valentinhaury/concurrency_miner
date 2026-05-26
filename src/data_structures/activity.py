class Activity:
    def __init__(self, activity_label):
        self.label = activity_label

    def __str__(self):
        return self.label

    def is_same(self, other):
        return self.label == other.label