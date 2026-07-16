from algorithm_components.fall_throughs.activitiy_once_per_trace import get_activities_once_per_trace, \
    detect_activity_once_per_trace
from algorithm_components.helper_functions.sublog_functions import get_log_without_activity
from data_structures.directly_follows_relation import DirectlyFollowsRelation
from src.algorithm_components.split_detection.detect_arbitrary_order import create_arbitrary_order_partitions
from src.algorithm_components.split_detection.detect_sequence import get_sequence_sublogs
from src.data_structures.activity import Activity
from src.data_structures.trace import Trace
from src.data_structures.log import Log
from src.concurrency_miner import concurrency_miner

#TODO Fallthroughs,
# done  Empty Log -> Tau
# done  Empty Trace -> x(Tau,...)
#       activity once per trace -> if an acitivity is in every trace put it in concurrent and continue
#       concurrent activity -> put one activity in concurrent and see if a cut is found with the rest, if yes continue
#       strict tau loop ?
#       tau loop ?
#       flower model -> return all activities concurrent

#TODO data handling
#       infrequent
#       incompletness

#TODO Add good test cases (bigger constructs with all operators mixed)
#TODO correct and incorrect test cases
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

#get_log_without_activity
#detect_activity_once_per_trace
#get_activities_once_per_trace
print("-----------------------------------------------------------------------------------------------------------")

print(str(get_activities_once_per_trace(test_log)))

print("-----------------------------------------------------------------------------------------------------------")

if detect_activity_once_per_trace(test_log):
    print("True")

print("-----------------------------------------------------------------------------------------------------------")

print("test log: " + str(test_log))

activity = get_activities_once_per_trace(test_log)[0]
print("test log without " + activity.get_label() + ": " + str(get_log_without_activity(test_log, activity)))

print("-----------------------------------------------------------------------------------------------------------")
if False:
    i = 1
    for log in get_sequence_sublogs(test_log):
        print("Log " + str(i))
        i +=1
        for trace in log.get_traces():
            print(str(trace))

    print("-----------------------------------------------------------------------------------------------------------")

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