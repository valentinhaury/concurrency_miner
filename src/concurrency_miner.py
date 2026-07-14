from split_detection.handle_empty_traces import handle_empty_traces
from src.data_structures.activity import Activity
from src.split_detection.detect_single_activity import detect_single_activity, get_single_activity
from src.data_structures.process_tree_operator import Operator
from src.data_structures.process_tree import Node
from src.split_detection.detect_arbitrary_order import detect_arbitrary_order, get_arbitrary_order_sublogs
from src.split_detection.detect_loop import detect_loop, get_loop_sublogs
from src.split_detection.detect_parallel import detect_parallel, get_parallel_sublogs
from src.split_detection.detect_concurrent import detect_concurrent, get_concurrent_sublogs
from src.split_detection.detect_interleafing import get_interleafing_sublogs, detect_interleafing
from src.split_detection.detect_exclusive import detect_exclusive, get_exclusive_choice_sublogs
from src.split_detection.detect_sequence import detect_sequence, get_sequence_sublogs
from src.split_detection.detect_multi_instance import get_multi_instance_activities


def concurrency_miner(log, multi_instance_activities=None):
# check for multi_instance activities
    if not multi_instance_activities:
        multi_instance_activities = get_multi_instance_activities(log)
# add Activity("tau") to empty traces
    handle_empty_traces(log)
# end recursion and add single activity node
    if detect_single_activity(log):
        activity = get_single_activity(log)
        if activity.activity_exists_by_label(multi_instance_activities):
            process_tree = Node(Operator.Multi)
            process_tree.add_child(Node(activity))
        else:
            process_tree = Node(activity)
        return process_tree
# split the log with an exclusive choice operator
    elif detect_exclusive(log):
        process_tree = Node(Operator.Exclusive)
        for sublog in get_exclusive_choice_sublogs(log):
            process_tree.add_child(concurrency_miner(sublog, multi_instance_activities))
        return process_tree
# split the log with a sequence operator
    elif detect_sequence(log):
        process_tree = Node(Operator.Sequence)
        for sublog in get_sequence_sublogs(log):
            process_tree.add_child(concurrency_miner(sublog, multi_instance_activities))
        return process_tree
# split the log with an arbitrary order operator
    elif detect_arbitrary_order(log):
        process_tree = Node(Operator.Arbitrary)
        for sublog in get_arbitrary_order_sublogs(log):
            process_tree.add_child(concurrency_miner(sublog, multi_instance_activities))
        return process_tree
# split the log with an interleaving operator
    elif detect_interleafing(log):
        process_tree = Node(Operator.Interleafing)
        for sublog in get_interleafing_sublogs(log):
            process_tree.add_child(concurrency_miner(sublog, multi_instance_activities))
        return process_tree
# split the log with a concurrent operator
    elif detect_concurrent(log):
        process_tree = Node(Operator.Concurrent)
        for sublog in get_concurrent_sublogs(log):
            process_tree.add_child(concurrency_miner(sublog, multi_instance_activities))
        return process_tree
# split the log with a parallel operator
    elif detect_parallel(log):
        process_tree = Node(Operator.Parallel)
        for sublog in get_parallel_sublogs(log):
            process_tree.add_child(concurrency_miner(sublog, multi_instance_activities))
        return process_tree
# split the log with a loop operator
    elif detect_loop(log):
        process_tree = Node(Operator.Loop)
        for sublog in get_loop_sublogs(log):
            process_tree.add_child(concurrency_miner(sublog, multi_instance_activities))
        return process_tree
    else:
        return Node("Fall-Through")
