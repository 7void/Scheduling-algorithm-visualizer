def fcfs(processes):
    processes.sort(key=lambda x: x[1]) 
    current_time = 0
    schedule = []
    timestamps = []
    completion_times = {}
    waiting_times = []
    burst_times = {p[0]: p[2] for p in processes}  
        
    for process, arrival_time, cpu_burst, _ in processes:
        start_time = max(current_time, arrival_time)
        timestamps.append(start_time)
        schedule.append((process, cpu_burst))
        current_time = start_time + cpu_burst
        completion_times[process] = current_time  
        
    timestamps.append(current_time)


    for process, completion_time in completion_times.items():
        burst_time = burst_times[process]
        arrival_time = next(p[1] for p in processes if p[0] == process)
        waiting_time = completion_time - burst_time - arrival_time
        waiting_times.append((process, waiting_time))
    
    timestamps = [round(time, 2) for time in timestamps]
    return schedule, timestamps, completion_times, waiting_times

def round_robin(processes, time_quantum):
    queue = []
    schedule = []
    timestamps = []
    current_time = 0
    completion_times = {}
    waiting_times = []
    remaining_time_dict = {p[0]: p[2] for p in processes}  
    
    processes.sort(key=lambda x: x[1])
    queue.extend(processes)
    arrival_times = {p[0]: p[1] for p in processes}  

    while queue:
        process, arrival_time, cpu_burst, _ = queue.pop(0)
        if current_time < arrival_time:
            current_time = arrival_time
        timestamps.append(current_time)
        if cpu_burst <= time_quantum:
            schedule.append((process, cpu_burst))
            current_time += cpu_burst
            completion_times[process] = current_time  
        else:
            schedule.append((process, time_quantum))
            current_time += time_quantum
            remaining_time_dict[process] -= time_quantum
            queue.append((process, arrival_time, remaining_time_dict[process], _))

    timestamps.append(current_time)
    

    for process, completion_time in completion_times.items():
        burst_time = remaining_time_dict[process] + time_quantum 
        arrival_time = arrival_times[process]
        waiting_time = completion_time - burst_time - arrival_time
        waiting_times.append((process, waiting_time))

    timestamps = [round(time, 2) for time in timestamps]
    return schedule, timestamps, completion_times, waiting_times

def srtf(processes):
    processes.sort(key=lambda x: x[1]) 
    current_time = 0
    schedule = []
    timestamps = []
    completion_times = {}
    waiting_times = []
    remaining_processes = [(p[0], p[1], p[2]) for p in processes]  
    waiting_queue = []
    burst_times = {p[0]: p[2] for p in processes}  
    
    while remaining_processes or waiting_queue:
        while remaining_processes and remaining_processes[0][1] <= current_time:
            waiting_queue.append(remaining_processes.pop(0))

        if waiting_queue:
            waiting_queue.sort(key=lambda x: x[2])  
            process, arrival_time, remaining_time = waiting_queue.pop(0)
            next_arrival_time = remaining_processes[0][1] if remaining_processes else float('inf')
            time_to_next_arrival = next_arrival_time - current_time

            if remaining_time <= time_to_next_arrival:
                timestamps.append(current_time)
                schedule.append((process, remaining_time))  
                current_time += remaining_time
                completion_times[process] = current_time  
            else:
                timestamps.append(current_time)
                schedule.append((process, time_to_next_arrival))  
                remaining_time -= time_to_next_arrival
                current_time += time_to_next_arrival
                waiting_queue.append((process, arrival_time, remaining_time))  
        else:
            if remaining_processes:
                next_arrival_time = remaining_processes[0][1]
                if current_time != next_arrival_time:
                    schedule.append(("Idle", next_arrival_time - current_time))
                    current_time = next_arrival_time
                    timestamps.append(current_time)
        
    timestamps.append(current_time)


    for process, completion_time in completion_times.items():
        burst_time = burst_times[process]
        arrival_time = next(p[1] for p in processes if p[0] == process)
        waiting_time = completion_time - burst_time - arrival_time
        waiting_times.append((process, waiting_time))

    timestamps = [round(time, 2) for time in timestamps]
    return schedule, timestamps, completion_times, waiting_times

def priority_scheduling(processes):
    processes.sort(key=lambda x: x[1])  
    current_time = 0
    schedule = []
    timestamps = []
    completion_times = {}
    waiting_times = []
    remaining_processes = [(p[0], p[1], p[2], p[3]) for p in processes]  
    waiting_queue = []
    burst_times = {p[0]: p[2] for p in processes}  

    while remaining_processes or waiting_queue:
        while remaining_processes and remaining_processes[0][1] <= current_time:
            waiting_queue.append(remaining_processes.pop(0))

        if waiting_queue:
            waiting_queue.sort(key=lambda x: x[3])  
            process, arrival_time, remaining_time, priority = waiting_queue.pop(0)
            timestamps.append(current_time)
            next_arrival_time = remaining_processes[0][1] if remaining_processes else float('inf')
            time_to_next_arrival = next_arrival_time - current_time

            if remaining_time <= time_to_next_arrival:
                schedule.append((process, remaining_time)) 
                current_time += remaining_time
                completion_times[process] = current_time  
            else:
                schedule.append((process, time_to_next_arrival))  
                remaining_time -= time_to_next_arrival
                current_time += time_to_next_arrival
                waiting_queue.append((process, arrival_time, remaining_time, priority))  
        else:
            if remaining_processes:
                next_arrival_time = remaining_processes[0][1]
                if current_time != next_arrival_time:
                    schedule.append(("Idle", next_arrival_time - current_time))
                    current_time = next_arrival_time
                    timestamps.append(current_time)

    timestamps.append(current_time)

    for process, completion_time in completion_times.items():
        burst_time = burst_times[process]
        arrival_time = next(p[1] for p in processes if p[0] == process)
        waiting_time = completion_time - burst_time - arrival_time
        waiting_times.append((process, waiting_time))

    timestamps = [round(time, 2) for time in timestamps]
    return schedule, timestamps, completion_times, waiting_times