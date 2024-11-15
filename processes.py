import threading
import time

def increment_loop(limit, result_dict, thread_name):
    start_time = time.time()
    for i in range(limit):
        pass 
    end_time = time.time()
    result_dict[thread_name] = end_time - start_time

def run_threads():
    execution_times = {}

    threads = [
        threading.Thread(target=increment_loop, args=(100000000, execution_times, 'p1')),
        threading.Thread(target=increment_loop, args=(150000000, execution_times, 'p2')),
        threading.Thread(target=increment_loop, args=(250000000, execution_times, 'p3'))
    ]
    

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    return execution_times
