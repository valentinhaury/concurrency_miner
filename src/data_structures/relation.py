class Relation:
    def __init__(self, first_activity, second_activity):
        self.first_activity = first_activity
        self.second_activity = second_activity

    def __str__(self):
        return "(" + str(self.first_activity) + "R" + str(self.second_activity) + ")"

    def relation_occurs_in(self, relations):
        for relation in relations:
            same_first = self.first_activity.has_same_label_as(relation.first_activity)
            same_second = self.second_activity.has_same_label_as(relation.second_activity)
            if same_first and same_second:
                return True
        return False

    def get_first_activity(self):
        return self.first_activity

    def get_second_activity(self):
        return self.second_activity