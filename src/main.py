from src.split_detection.detect_concurrent import create_concurrent_partitions, detect_concurrent
from src.data_structures.directly_follows_relation import DirectlyFollowsRelation
from src.split_detection.detect_arbitrary_order import detect_arbitrary_order, create_arbitrary_order_partitions
from src.split_detection.detect_interleafing import detect_interleafing
from src.data_structures.activity import Activity
from src.data_structures.log import Log
from src.data_structures.trace import Trace
from src.log_creation.log_creator import get_log
from src.split_detection.detect_exclusive import detect_exclusive
from src.split_detection.detect_sequence import detect_sequence, create_sequence_partitions

str_input = 'sequence'
test_log = get_log(str_input)
#test_log = Log([])
print("activities")
print(str(test_log.get_activities_by_label()))
print("-----------------------------------------------------------------------------------------------------------")
print(str(create_concurrent_partitions(test_log)))
print("-----------------------------------------------------------------------------------------------------------")
print("In Function prints: ")
result = detect_concurrent(test_log)
print("-----------------------------------------------------------------------------------------------------------")
if result:
    print("---------------------------------------Found cut in " + str_input + "-log---------------------------------------")
if not result:
    print("--------------------------------------Found no cut in " + str_input + "-log-------------------------------------")
print("-----------------------------------------------------------------------------------------------------------")


