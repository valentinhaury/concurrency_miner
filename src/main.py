from src.data_structures.activity import Activity
from src.data_structures.log import Log
from src.data_structures.trace import Trace
from src.log_creation.log_creator import get_log
from src.split_detection.detect_exclusive import detect_exclusive
from src.split_detection.detect_sequence import detect_sequence

exclusive_log = get_log('parallel')

if detect_sequence(exclusive_log):
    print("neinneinnein")

print("eventually")
for relation in exclusive_log.get_eventually_follows_relations_by_label():
    print(str(relation))

print("overlapping")
for relation in exclusive_log.get_overlapping_relations_by_label():
    print(str(relation))

