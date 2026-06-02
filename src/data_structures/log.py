class Log:
    def __init__(self, traces):
        self.log = traces

    def __str__(self):
        string = "("
        for trace in self.log:
            string += str(trace) + ", "
        string = string[:-2] + ")"
        return string

    def add_trace(self, trace):
        self.log.append(trace)

    def get_traces(self):
        return self.log
