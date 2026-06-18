class Log:
    def __init__(self, traces):
        self.traces = traces

    def __str__(self):
        string = "("
        for trace in self.traces:
            string += str(trace) + ",    "
        string = string[:-5] + ")"
        return string

    def add_trace(self, trace):
        self.traces.append(trace)

    def get_traces(self):
        return self.traces

    def get_eventually_follows_relations_by_label(self):
        eventually_follows_relations = []
        for trace in self.traces:
            trace_relations = trace.get_eventually_follows_relations_by_label()
            for relation in trace_relations:
                if not relation.exists_by_label(eventually_follows_relations):
                    eventually_follows_relations.append(relation)

        return eventually_follows_relations

    def get_overlapping_relations_by_label(self):
        overlapping_relations = []
        for trace in self.traces:
            trace_relations = trace.get_overlapping_relations_by_label()
            for relation in trace_relations:
                if not relation.exists_by_label(overlapping_relations):
                    overlapping_relations.append(relation)

        return overlapping_relations

    def get_activities_by_label(self):
        activities = []
        for trace in self.traces:
            trace_activities = trace.get_activities()
            for activity in trace_activities:
                if not activity.exists_by_label(activities):
                    activities.append(activity)

        return activities
