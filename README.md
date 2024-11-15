# Description

A GUI application built using PySide6 that lets users visualize how different scheduling algorithms work. 

Supported Algorithms:

1. FCFS (First Come First Serve)
2. Round Robin
3. SRTF (Shortest Remaining Task First)
4. Priority Scheduling


![image](https://github.com/user-attachments/assets/af9bdb82-90cf-4758-81a0-1b85c26fe62b)


# Usage

1. Download the zip file, extract the contents, and run the main file to open the GUI.

2. Add Process Manually:

  Users can manually add individual processes by clicking an "Add Process" button in the GUI.

3. Load Processes from a Python File:

  Users have the option to load multiple processes from a Python file.

4. File Requirements:

  The file for loading processes (e.g., processes.py) should:
  Run each process.
  Track and store the execution times for each process in a dictionary.
  Return this dictionary of execution times.

A sample Python file named processes.py is provided in the repository to demonstrate the expected format and functionality.
