from split_detection.detect_arbitrary_order import get_arbitrary_order_sublogs, create_arbitrary_order_partitions
from split_detection.minimum_self_distance_relation import trace_self_distance_list, get_minimum_self_distance_relations
from src.data_structures.activity import Activity
from src.data_structures.trace import Trace
from src.data_structures.log import Log
from src.concurrency_miner import concurrency_miner
from src.log_creation.log_creator import get_log

#TODO look into tau/silent-activities/optional-activities when there are empty trace
#   if there is an empty trace in Log1 return x(tau, f(Log1')) where Log1' is Log1 without empty traces
#   and also look into where empty traces can and should be created

#TODO Fallthroughs, infrequent etc.

#TODO Tree to traces - parser -> Given a tree returns a Log with all possible Traces -> Good to create Testcases

str_input = 'sequence_loop' # exclusive sequence arbitrary interleafing concurrent parallel loop sequence_loop
test_log = get_log(str_input)

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