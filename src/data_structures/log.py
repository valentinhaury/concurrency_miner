from src.data_structures.activity import Activity

class Log:
    def __init__(self, traces=None):
        if traces is None:
            traces = []
        self.traces = traces

    def __str__(self):
        if not self.traces:
            return "(empty-log)"
        string = "("
        for trace in self.traces:
            string += str(trace) + ",    "
        string = string[:-5] + ")"
        return string

    def add_trace(self, trace):
        self.traces.append(trace)

    def get_traces(self):
        return self.traces

    def get_directly_follows_relations_by_label(self):
        directly_follows_relations = []
        for trace in self.traces:
            unique_trace_directly_follows_relations = [
                r
                for r in trace.get_directly_follows_relations_by_label()
                if r not in directly_follows_relations
            ]
            directly_follows_relations.extend(unique_trace_directly_follows_relations)
        return directly_follows_relations

    def get_eventually_follows_relations_by_label(self):
        eventually_follows_relations = []
        for trace in self.traces:
            trace_relations = trace.get_eventually_follows_relations_by_label()
            for relation in trace_relations:
                if not relation.relation_exists_by_label(eventually_follows_relations):
                    eventually_follows_relations.append(relation)

        return eventually_follows_relations

    def get_overlapping_relations_by_label(self):
        overlapping_relations = []
        for trace in self.traces:
            trace_relations = trace.get_overlapping_relations_by_label()
            for relation in trace_relations:
                if not relation.relation_exists_by_label(overlapping_relations):
                    overlapping_relations.append(relation)

        return overlapping_relations

    def get_activities_by_label(self):
        activities = []
        for trace in self.traces:
            trace_activities = trace.get_activities()
            for activity in trace_activities:
                if not activity.activity_exists_by_label(activities):
                    activities.append(Activity(activity.get_label()))

        return activities

    def get_start_activities_by_label(self):
        start_activities = []
        for trace in self.traces:
            trace_start_activities = trace.get_start_activities()
            for activity in trace_start_activities:
                if not activity.activity_exists_by_label(start_activities):
                    start_activities.append(Activity(activity.get_label()))
        return start_activities

    def get_end_activities_by_label(self):
        end_activities = []
        for trace in self.traces:
            trace_end_activities = trace.get_end_activities()
            for activity in trace_end_activities:
                if not activity.activity_exists_by_label(end_activities):
                    end_activities.append(Activity(activity.get_label()))
        return end_activities