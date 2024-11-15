# Description

A GUI application built using PySide6 that lets users visualize how different scheduling algorithms work. 

Supported Algorithms:

1. FCFS (First Come First Serve)
2. Round Robin
3. SRTF (Shortest Remaining Task First)
4. Priority Scheduling


![image](https://github.com/user-attachments/assets/af9bdb82-90cf-4758-81a0-1b85c26fe62b)


# Usage

Users can add processes manually using the "Add Process" button and load processes(threads) from a Python file. When loading processes from a Python file, that file must run the processes, store their execution times in a dictionary, and return that dictionary. A sample file, processes.py, is provided in this repo and can be imported into the GUI. 
