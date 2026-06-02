from data_structures.activity import Activity
from data_structures.directly_follows_relation import DirectlyFollowsRelation
from data_structures.log import Log
from data_structures.trace import Trace

a = Activity("a")
b = Activity("b")
c = Activity("c")
d = Activity("d")
e = Activity("e")
f = Activity("f")
g = Activity("g")
h = Activity("h")

def get_log(specifier):
    match specifier:
        case "exclusive":       return log_exclusive()   # exclusive Log
        case "sequence":        return log_sequence()   # sequence log
        case "loop":            return log_loop()   # loop log
        case "interleafing":    return log_interleafing()   # interleafing log
        case "concurrent":      return log_concurrent()   # concurrent log
        case "parallel":        return log_parallel()   # parallel log
        case "c_parallel":      return log_c_parallel()   # certain parallel log
    return None


def log_exclusive():
    trace_a = Trace([a], [a], [a])
    trace_b = Trace([b], [b], [b])
    return Log([trace_a, trace_b])

def log_sequence():
    trace_a = Trace([a, b], [a], [b], [DirectlyFollowsRelation(a, b)])
    return Log([trace_a])

def log_loop():
    trace_a = Trace([a, b], [a],[a],[DirectlyFollowsRelation(a, b), DirectlyFollowsRelation(b, a)])
    return Log([trace_a])

def log_interleafing():
    trace_a = Trace([a, b, c], [a],[c],[DirectlyFollowsRelation(a, b), DirectlyFollowsRelation(b, c)])
    trace_b = Trace([a, b, c], [b], [a], [DirectlyFollowsRelation(b, c), DirectlyFollowsRelation(c, a)])
    return Log([trace_a, trace_b])

def log_concurrent():
    trace_a = Trace([a, b, c], [a],[c],[DirectlyFollowsRelation(a, b), DirectlyFollowsRelation(b, c)])
    trace_b = Trace([a, b, c], [b], [a], [DirectlyFollowsRelation(b, c), DirectlyFollowsRelation(c, a)])
    trace_c = Trace([a, b, c], [b], [c], [DirectlyFollowsRelation(b, a), DirectlyFollowsRelation(a, c)])
    return Log([trace_a, trace_b, trace_c])

def log_parallel():
    trace_a = Trace([a, b, c], [a], [c], [DirectlyFollowsRelation(a, b), DirectlyFollowsRelation(b, c)])
    trace_b = Trace([a, b, c], [b], [a], [DirectlyFollowsRelation(b, c), DirectlyFollowsRelation(c, a)])
    trace_c = Trace([a, b, c], [b], [c], [DirectlyFollowsRelation(b, a), DirectlyFollowsRelation(a, c)])
    trace_d = Trace([a, b, c], [a, b], [c], [DirectlyFollowsRelation(a, c), DirectlyFollowsRelation(b, c)])
    trace_e = Trace([a, b, c], [b], [a, c], [DirectlyFollowsRelation(b, c), DirectlyFollowsRelation(b, a)])
    trace_f = Trace([a, b, c], [a, b], [a, c], [DirectlyFollowsRelation(b, c)])
    return Log([trace_a, trace_b, trace_c, trace_d, trace_e, trace_f])

def log_c_parallel():
    trace_f = Trace([a, b, c], [a, b], [a, c], [DirectlyFollowsRelation(b, c)])
    return Log([trace_f])