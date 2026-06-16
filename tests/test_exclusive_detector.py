from src.log_creation.log_creator import get_log
from src.split_detection.detect_exclusive import detect_exclusive

def test_empty_log():
    assert True

def test_exclusive_log():
    assert detect_exclusive(get_log("exclusive")) == True

def test_sequence_log():
    assert detect_exclusive(get_log("sequence")) == False

def test_concurrent_log():
    assert detect_exclusive(get_log("concurrent")) == False

def test_interleafing_log():
    assert detect_exclusive(get_log("interleafing")) == False

def test_parallel_log():
    assert detect_exclusive(get_log("parallel")) == False

def test_certain_parallel_log():
    assert detect_exclusive(get_log("certain_parallel")) == False
