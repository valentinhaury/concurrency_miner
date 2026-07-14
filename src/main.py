from data_structures.directly_follows_relation import DirectlyFollowsRelation
from split_detection.detect_arbitrary_order import get_arbitrary_order_sublogs, create_arbitrary_order_partitions
from split_detection.detect_sequence import get_sequence_sublogs
from split_detection.minimum_self_distance_relation import trace_self_distance_list, get_minimum_self_distance_relations
from src.data_structures.activity import Activity
from src.data_structures.trace import Trace
from src.data_structures.log import Log
from src.concurrency_miner import concurrency_miner
from src.log_creation.log_creator import get_log

#TODO Fallthroughs, infrequent etc.


#TODO Add good test cases (bigger constructs with all operators mixed)
#TODO Tree to traces - parser -> Given a tree returns a Log with all possible Traces -> Good to create Testcases

str_input = 'sequence_loop' # exclusive sequence arbitrary interleafing concurrent parallel loop sequence_loop
#test_log = get_log(str_input)
a1 = Activity("a")
a2 = Activity("a")
b1 = Activity("b")
b2 = Activity("b")
c1 = Activity("c")
t1 = Trace([a1, b1, c1], [DirectlyFollowsRelation(a1, c1), DirectlyFollowsRelation(c1, b1)])
t2 = Trace([a2, b2], [DirectlyFollowsRelation(a2, b2)])
test_log = Log([t1, t2])


print("-----------------------------------------------------------------------------------------------------------")

i = 1
for log in get_sequence_sublogs(test_log):
    print("Log " + str(i))
    i +=1
    for trace in log.get_traces():
        print(str(trace))

print("-----------------------------------------------------------------------------------------------------------")
if False:
    print(str(create_arbitrary_order_partitions(test_log)))
    print("-----------------------------------------------------------------------------------------------------------")
print("-----------------------------------------------------------------------------------------------------------")
print("Discovered Tree")
process_tree = concurrency_miner(test_log)
print(str(process_tree))
print("-----------------------------------------------------------------------------------------------------------")
print("Input Log")
print(str(test_log))
print("-----------------------------------------------------------------------------------------------------------")