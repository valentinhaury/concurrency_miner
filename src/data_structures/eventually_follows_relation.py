from src.data_structures.relation import Relation

class EventuallyFollowsRelation(Relation):
    def __init__(self, first_activity, second_activity):
        super().__init__(first_activity, second_activity)

    def __str__(self):
        return "(" + str(self.first_activity) + ">>" + str(self.second_activity) + ")"