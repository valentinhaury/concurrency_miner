from src.data_structures.activity import Activity
from src.data_structures.trace import Trace
from src.data_structures.log import Log
from src.concurrency_miner import concurrency_miner
from src.log_creation.log_creator import get_log

#TODO for concurrent/interleafing cut : All partitions that have no start and no end activity should be merged with another partition
#   The reason is that every partition should be able to start and end the trace if they are concurrent/interleafing
#   maybe its already implemented in the are_in_loop
#   look into minimum self distance relationship

#TODO look into tau/silent-activities/optional-activities when there are empty trace
#   and also look into where empty traces can and should be created

#TODO Fallthroughs, infrequent etc.

#TODO Tree to traces - parser -> Given a tree returns a Log with all possible Traces -> Good to create Testcases








str_input = 'exclusive' # exclusive sequence arbitrary interleafing concurrent parallel loop
test_log = get_log(str_input)

print("-----------------------------------------------------------------------------------------------------------")
print("Discovered Tree")
process_tree = concurrency_miner(test_log)
print(str(process_tree))
print("-----------------------------------------------------------------------------------------------------------")
print("Input Log")
print(str(test_log))
print("-----------------------------------------------------------------------------------------------------------")