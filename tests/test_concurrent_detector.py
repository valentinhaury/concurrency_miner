from src.log_creation.log_creator import get_log
from src.split_detection.detect_concurrent import detect_concurrent
from src.data_structures.log import Log

def test_empty_log():
    assert detect_concurrent(Log([])) == False

def test_exclusive_log():
    assert detect_concurrent(get_log("exclusive")) == False

def test_sequence_log():
    assert detect_concurrent(get_log("sequence")) == False

def test_arbitrary_order_log():
    assert detect_concurrent(get_log("arbitrary")) == False

def test_interleafing_log():
    assert detect_concurrent(get_log("interleafing")) == False

def test_concurrent_log():
    assert detect_concurrent(get_log("concurrent")) == True

def test_parallel_log():
    assert detect_concurrent(get_log("parallel")) == False

def test_loop_log():
    assert detect_concurrent(get_log("loop")) == False