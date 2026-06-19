from data_structures.directly_follows_relation import DirectlyFollowsRelation
from src.split_detection.detect_interleafing import detect_interleafing
from src.data_structures.activity import Activity
from src.data_structures.log import Log
from src.data_structures.trace import Trace
from src.log_creation.log_creator import get_log
from src.split_detection.detect_exclusive import detect_exclusive
from src.split_detection.detect_sequence import detect_sequence
str_input = 'interleafing'
test_log = get_log(str_input)
print("-----------------------------------------------------------------------------------------------------------")
print("In Function prints: ")
result = detect_interleafing(test_log)
print("-----------------------------------------------------------------------------------------------------------")
if result:
    print("---------------------------------------Found cut in " + str_input + "-log---------------------------------------")
if not result:
    print("--------------------------------------Found no cut in " + str_input + "-log-------------------------------------")
print("-----------------------------------------------------------------------------------------------------------")
print("Additional prints: ")
a1 = Activity("a1")
b1 = Activity("b1")
c1 = Activity("c1")
t1 = Trace([a1, b1, c1], [DirectlyFollowsRelation(b1, a1), DirectlyFollowsRelation(a1, c1)])
t2 = Trace([a1, b1, c1], [DirectlyFollowsRelation(a1, b1), DirectlyFollowsRelation(b1, c1)])
t3 = Trace([a1, b1, c1], [DirectlyFollowsRelation(b1, c1), DirectlyFollowsRelation(c1, a1)])

print("-----------------------------------------------------------------------------------------------------------")

