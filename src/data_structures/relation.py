class Relation:
    def __init__(self, first_activity, second_activity):
        self.first_activity = first_activity
        self.second_activity = second_activity

    def __str__(self):
        return "(" + str(self.first_activity) + "R" + str(self.second_activity) + ")"

    def __eq__(self, other):
        return self.first_activity == other.first_activity and self.second_activity == other.second_activity

    def __hash__(self):
        return hash((self.first_activity, self.second_activity))

    def get_first_activity(self):
        return self.first_activity

    def get_second_activity(self):
        return self.second_activity