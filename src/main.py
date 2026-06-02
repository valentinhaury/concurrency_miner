from log_creation.log_creator import get_log

print(str(get_log("exclusive")))
print(str(get_log("sequence")))
print(str(get_log("interleafing")))
print(str(get_log("concurrent")))
print(str(get_log("parallel")))
print(str(get_log("c_parallel")))
print(str(get_log("loop")))

