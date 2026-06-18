class Relation:
    def __init__(self, first_activity, second_activity):
        self.first_activity = first_activity
        self.second_activity = second_activity

    def __str__(self):
        return "(" + str(self.first_activity) + "R" + str(self.second_activity) + ")"

    def exists_by_label(self, relations):
        for relation in relations:
            same_first = self.first_activity.get_label == relation.get_first_activity().get_label
            same_second = self.second_activity.get_label == relation.get_second_activity().get_label
            if same_first and same_second:
                return True
        return False

    def get_first_activity(self):
        return self.first_activity

    def get_second_activity(self):
        return self.second_activity