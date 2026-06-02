from enum import Enum

class Operator(Enum):
    Exclusive = "\u00D7"
    Sequence = "\u2192"
    Loop = "\u27f3"
    Interleafing = "\u2194"
    Concurrent = "\u2227"
    Parallel = "||"
    CertainParallel ="c||"
#op.value für das Symbol