from src.concurrency_miner import concurrency_miner
from src.data_structures.relation import Relation
from src.data_structures.trace import Trace
from src.split_detection.detect_arbitrary_order import get_arbitrary_order_sublogs
from src.split_detection.detect_parallel import get_parallel_sublogs
from src.split_detection.detect_concurrent import create_concurrent_partitions, detect_concurrent, \
    get_concurrent_sublogs
from src.data_structures.directly_follows_relation import DirectlyFollowsRelation
from src.split_detection.detect_arbitrary_order import detect_arbitrary_order, create_arbitrary_order_partitions
from src.split_detection.detect_interleafing import detect_interleafing, get_interleafing_sublogs
from src.data_structures.activity import Activity
from src.data_structures.log import Log
from src.data_structures.trace import Trace
from src.log_creation.log_creator import get_log
from src.split_detection.detect_exclusive import detect_exclusive, get_exclusive_choice_sublogs
from src.split_detection.detect_sequence import detect_sequence, create_sequence_partitions, get_sequence_sublogs
from src.split_detection.detect_loop import detect_loop, create_loop_partitions, get_loop_sublogs

#TODO for concurrent/interleafing cut : All partitions that have no start and no end activity should be merged with another partition
# The reason is that every partition should be able to start and end the trace if they are concurrent/interleafing
# maybe its already implemented in the are_in_loop
# look into minimum self distance relationship

#Saturday
#TODO Multi-Instance Operator - maybe just check in the beginning and then remember them and replace them at the end with MI(a)
#TODO Connect all the Mining elements
#Sunday
#TODO Tree to traces - parser -> Given a tree returns a Log with all possible Traces -> Good to create Testcases


str_input = 'sequence_loop'
test_log = get_log(str_input)
#test_log = Log([])

if detect_sequence(test_log):
    print("s detected")
else:
    print("s not detected")

print("-----------------------------------------------------------------------------------------------------------")
process_tree = concurrency_miner(test_log)
print(str(process_tree))
print("-----------------------------------------------------------------------------------------------------------")
print("log: " + str(test_log))
print("activities: ")
print(str(test_log.get_activities_by_label()))
print("-----------------------------------------------------------------------------------------------------------")
if False:
    for log in get_loop_sublogs(test_log):
        print("log: " + str(log))
    print("-----------------------------------------------------------------------------------------------------------")

    print(str(create_loop_partitions(test_log)))
    print("-----------------------------------------------------------------------------------------------------------")
    print("In Function prints: ")
    result = detect_loop(test_log)
    print("-----------------------------------------------------------------------------------------------------------")
    if result:
        print("---------------------------------------Found cut in " + str_input + "-log---------------------------------------")
    if not result:
        print("--------------------------------------Found no cut in " + str_input + "-log-------------------------------------")
    print("-----------------------------------------------------------------------------------------------------------")


