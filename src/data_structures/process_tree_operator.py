from enum import Enum

class Operator(Enum):
    Exclusive = "\u00D7"
    Sequence = "\u2192"
    Loop = "\u27f3"
    Arbitrary = "\u2194"
    Interleafing = "\u2227"
    Concurrent = "||"
    Parallel ="//"
#op.value für das Symbol