from src.data_structures.activity import Activity
from src.data_structures.directly_follows_relation import DirectlyFollowsRelation
from src.data_structures.log import Log
from src.data_structures.trace import Trace

def a():
    return Activity("a")
def b():
    return Activity("b")
def c():
    return Activity("c")
def d():
    return Activity("d")
def e():
    return Activity("e")
def f():
    return Activity("f")
def g():
    return Activity("g")
def h():
    return Activity("h")

def arbitrary_trace_a_sequence():
    a1 = a()
    b1 = b()
    c1 = c()
    return Trace([a1, b1, c1], [a1],[c1],[DirectlyFollowsRelation(a1, b1), DirectlyFollowsRelation(b1, c1)])
def arbitrary_trace_sequence_a():
    a1 = a()
    b1 = b()
    c1 = c()
    return Trace([a1, b1, c1], [b1], [a1], [DirectlyFollowsRelation(b1, c1), DirectlyFollowsRelation(c1, a1)])
def interleafing_trace_a_sequence():
    a1 = a()
    b1 = b()
    c1 = c()
    return Trace([a1, b1, c1], [b1], [c1], [DirectlyFollowsRelation(b1, a1), DirectlyFollowsRelation(a1, c1)])
def certain_parallel_trace_a_sequence():
    a1 = a()
    b1 = b()
    c1 = c()
    return Trace([a1, b1, c1], [a1, b1], [a1, c1], [DirectlyFollowsRelation(b1, c1)])


def get_log(specifier):
    match specifier:
        case "exclusive":       return log_exclusive()   # exclusive Log
        case "sequence":        return log_sequence()   # sequence log
        case "loop":            return log_loop()   # loop log
        case "interleafing":    return log_interleafing()   # interleafing log
        case "concurrent":      return log_concurrent()   # concurrent log
        case "parallel":        return log_parallel()   # parallel log
        case "certain_parallel":      return log_c_parallel()   # certain parallel log
    return None


def log_exclusive():
    a1 = a()
    b1 = b()
    trace_a = Trace([a1], [a1], [a1])
    trace_b = Trace([b1], [b1], [b1])
    return Log([trace_a, trace_b])

def log_sequence():
    a1 = a()
    b1 = b()
    trace_a = Trace([a1, b1], [a1], [b1], [DirectlyFollowsRelation(a1, b1)])
    return Log([trace_a])

def log_loop():
    a1 = a()
    a2 = a()
    b1 = b()
    trace_a = Trace([a1, a2, b1], [a1],[a2],[DirectlyFollowsRelation(a1, b1), DirectlyFollowsRelation(b1, a2)])
    return Log([trace_a])

def log_interleafing():
    trace_a = arbitrary_trace_a_sequence()
    trace_b = arbitrary_trace_sequence_a()
    return Log([trace_a, trace_b])

def log_concurrent():
    trace_a = arbitrary_trace_a_sequence()
    trace_b = arbitrary_trace_sequence_a()
    trace_c = interleafing_trace_a_sequence()
    return Log([trace_a, trace_b, trace_c])

def log_parallel():
    trace_a = arbitrary_trace_a_sequence()
    trace_b = arbitrary_trace_sequence_a()
    trace_c = interleafing_trace_a_sequence()
    a1 = a()
    b1 = b()
    c1 = c()
    trace_d = Trace([a1, b1, c1], [a1, b1], [c1], [DirectlyFollowsRelation(a1, c1), DirectlyFollowsRelation(b1, c1)])
    a2 = a()
    b2 = b()
    c2 = c()
    trace_e = Trace([a2, b2, c2], [b2], [a2, c2], [DirectlyFollowsRelation(b2, c2), DirectlyFollowsRelation(b2, a2)])
    trace_f = certain_parallel_trace_a_sequence()
    return Log([trace_a, trace_b, trace_c, trace_d, trace_e, trace_f])

def log_c_parallel():
    trace_f = certain_parallel_trace_a_sequence()
    return Log([trace_f])