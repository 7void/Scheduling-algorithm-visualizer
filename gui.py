from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from algorithms import fcfs, round_robin, srtf, priority_scheduling
import time
import importlib.util

class GanttChart(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.schedules = []
        self.timestamps = []
        self.current_time = 0
        self.simulation_progress = 0
        self.setMinimumHeight(200)

    def set_schedule(self, schedules, timestamps):
        self.schedules = schedules
        self.timestamps = timestamps
        self.simulation_progress = 0
        self.current_time = 0
        self.update()

    def start_simulation(self, interval=1000):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start(interval)

    def update_simulation(self):
        if self.simulation_progress < len(self.schedules):
            self.simulation_progress += 1
            self.current_time = self.timestamps[self.simulation_progress]
            self.update()
        else:
            self.timer.stop()
            self.update()

    def paintEvent(self, event):
        if not self.schedules or self.simulation_progress == 0:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        width = self.width()
        height = self.height()
        total_duration = self.timestamps[-1] 

        x = 0
        for i, (process, duration) in enumerate(self.schedules[:self.simulation_progress]):
            process_width = (float(duration) / float(total_duration)) * width  
            painter.setBrush(QColor(100, 150, 250))
            painter.drawRect(x, 50, process_width, 50)
            painter.setPen(Qt.black)
            painter.setFont(QFont('Arial', 12))
            painter.drawText(int(x + process_width / 2) - 10, 85, process)
            painter.setPen(Qt.white)
            painter.setFont(QFont('Arial', 10))
            painter.drawText(int(x), 120, str(self.timestamps[i]))
            x += process_width

        if self.simulation_progress == len(self.schedules):
            painter.setPen(Qt.white)
            painter.drawText(int(x), 120, str(self.timestamps[-1]))

        painter.end()

class Scheduler(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Scheduling Algorithm Visualizer")
        self.layout = QVBoxLayout(self)
        self.input_layout = QVBoxLayout()

        self.process_table = QTableWidget(0, 4)
        self.process_table.setHorizontalHeaderLabels(["Process", "Arrival Time", "CPU Burst", "Priority"])
        self.process_table.setMinimumHeight(100)
        self.process_table.verticalHeader().setDefaultSectionSize(30)
        self.input_layout.addWidget(self.process_table)
        self.process_table.setColumnHidden(3, True)  

        self.add_process_button = QPushButton("Add Process")
        self.add_file_button = QPushButton("Add File")
        self.start_button = QPushButton("Start Scheduling")
        self.compare_button = QPushButton("Compare")
        self.clear_table_button = QPushButton("Clear Table")
        self.compare_button.clicked.connect(self.show_comparison_window)
        self.add_file_button.clicked.connect(self.open_file_dialog)
        self.start_button.clicked.connect(self.start_scheduling)
        self.add_process_button.clicked.connect(self.add_process)
        self.clear_table_button.clicked.connect(self.clear_table)

        self.algorithm_select = QComboBox()
        self.algorithm_select.addItems(["FCFS", "Round Robin", "SRTF", "Priority Scheduling"])
        self.algorithm_select.currentIndexChanged.connect(self.update_visibility)

        self.input_layout.addWidget(QLabel("Select Algorithm:"))
        self.input_layout.addWidget(self.algorithm_select)

        self.quantum_input_label = QLabel("Time Quantum:")
        self.quantum_input = QLineEdit(self)
        self.quantum_input.setPlaceholderText("Enter Time Quantum")
        self.quantum_input.setValidator(QDoubleValidator(0.00, 10.00, 2))  

        self.input_layout.addWidget(self.quantum_input_label)
        self.input_layout.addWidget(self.quantum_input)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_process_button)
        button_layout.addWidget(self.add_file_button)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.compare_button)
        button_layout.addWidget(self.clear_table_button) 
        self.input_layout.addLayout(button_layout)

        self.layout.addLayout(self.input_layout)

        self.gantt_chart = GanttChart(self)
        self.layout.addWidget(self.gantt_chart)

        self.total_time_label = QLabel("Total Time: 0")
        self.layout.addWidget(self.total_time_label)

        self.average_waiting_time_label = QLabel("Average Waiting Time: 0.00")
        self.layout.addWidget(self.average_waiting_time_label)
        self.layout.addWidget(self.total_time_label)

        self.update_visibility()


    def update_visibility(self):
        if self.algorithm_select.currentText() == "Round Robin":
            self.quantum_input_label.show()
            self.quantum_input.show()
            self.process_table.setColumnHidden(3, True)

        elif self.algorithm_select.currentText() == "Priority Scheduling":
            self.quantum_input_label.hide()
            self.quantum_input.hide()
            self.process_table.setColumnHidden(3, False)
        else:
            self.quantum_input_label.hide()
            self.quantum_input.hide()
            self.process_table.setColumnHidden(3, True)




    def show_comparison_window(self):
        if not hasattr(self, 'average_waiting_times'):
            self.compute_average_waiting_times()  # Calculate average waiting times if not already calculated

        dialog = QDialog(self)
        dialog.setWindowTitle("Average Waiting Times Comparison")
        dialog.setGeometry(100, 100, 600, 500)

        layout = QVBoxLayout()

        figure = Figure(figsize=(8, 6))
        canvas = FigureCanvas(figure)
        ax = figure.add_subplot(111)

        algorithms = list(self.average_waiting_times.keys())
        avg_waiting_times = list(self.average_waiting_times.values())

        ax.bar(algorithms, avg_waiting_times, color=['blue', 'green', 'red', 'purple'])
        ax.set_xlabel('Algorithms')
        ax.set_ylabel('Average Waiting Time')
        ax.set_title('Comparison of Average Waiting Times')

        layout.addWidget(canvas)

        dialog.setLayout(layout)

        dialog.exec()

    def open_file_dialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Python File", "", "Python Files (*.py)", options=options)
        if file_name:
            self.load_threads_from_file(file_name)



    def start_scheduling(self):
        processes = self.get_process_data()
        self.compute_average_waiting_times()  # Calculate average waiting times for all algorithms
        algorithm = self.algorithm_select.currentText()
        schedule, timestamps, _, waiting_times = [], [], {}, []
        
        if algorithm == "FCFS":
            schedule, timestamps, _, waiting_times = fcfs(processes)
        elif algorithm == "Round Robin":
            time_quantum = float(self.quantum_input.text())
            schedule, timestamps, _, waiting_times = round_robin(processes, time_quantum)
        elif algorithm == "SRTF":
            schedule, timestamps, _, waiting_times = srtf(processes)
        elif algorithm == "Priority Scheduling":
            schedule, timestamps, _, waiting_times = priority_scheduling(processes)

        self.gantt_chart.set_schedule(schedule, timestamps)
        avg_waiting_time = sum(wt for _, wt in waiting_times) / len(waiting_times)
        self.average_waiting_time_label.setText(f"Average Waiting Time: {avg_waiting_time:.2f}")
        self.total_time_label.setText(f"Total Time: {timestamps[-1] - timestamps[0]:.2f}")
        self.gantt_chart.start_simulation(interval=1000)


        self.gantt_chart.set_schedule(schedule, timestamps)
        avg_waiting_time = sum(wt for _, wt in waiting_times) / len(waiting_times)
        self.average_waiting_time_label.setText(f"Average Waiting Time: {avg_waiting_time:.2f}")
        self.total_time_label.setText(f"Total Time: {timestamps[-1] - timestamps[0]:.2f}")
        self.gantt_chart.start_simulation(interval=1000)

    def add_process(self):
        row_position = self.process_table.rowCount()
        self.process_table.insertRow(row_position)
    
    def get_process_data(self):
        processes = []
        for row in range(self.process_table.rowCount()):
            if self.process_table.item(row, 0):
                name = self.process_table.item(row, 0).text()
            else:
                name = ""
            if self.process_table.item(row, 1):
                arrival_time = float(self.process_table.item(row, 1).text())  
            else:
                arrival_time = 0.0
            if self.process_table.item(row, 2):
                cpu_burst = float(self.process_table.item(row, 2).text())  
            else:
                cpu_burst = 0.0
            if self.process_table.item(row, 3):
                priority = int(self.process_table.item(row, 3).text())  
            else:
                priority = 0
            processes.append((name, arrival_time, cpu_burst, priority))
        return processes

    def compute_average_waiting_times(self):
        processes = self.get_process_data()

        self.average_waiting_times = {}

        _, _, _, waiting_times = fcfs(processes)
        self.average_waiting_times["FCFS"] = sum([wt for _, wt in waiting_times]) / len(waiting_times)

        try:
            time_quantum = float(self.quantum_input.text()) if self.quantum_input.text() else 2
        except ValueError:
            time_quantum = 2  # Default value
        _, _, _, waiting_times = round_robin(processes, time_quantum)
        self.average_waiting_times["Round Robin"] = sum([wt for _, wt in waiting_times]) / len(waiting_times)

        _, _, _, waiting_times = srtf(processes)
        self.average_waiting_times["SRTF"] = sum([wt for _, wt in waiting_times]) / len(waiting_times)

        _, _, _, waiting_times = priority_scheduling(processes)
        self.average_waiting_times["Priority Scheduling"] = sum([wt for _, wt in waiting_times]) / len(waiting_times)


    def load_threads_from_file(self, file_path):
        try:
            spec = importlib.util.spec_from_file_location("module.name", file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, 'run_threads') and callable(module.run_threads):

                execution_times = module.run_threads()

                if isinstance(execution_times, dict):
                    self.process_table.setRowCount(len(execution_times))
                    for i, (process_name, exec_time) in enumerate(execution_times.items()):
                        self.process_table.setItem(i, 0, QTableWidgetItem(process_name))
                        self.process_table.setItem(i, 1, QTableWidgetItem(str(i))) 
                        self.process_table.setItem(i, 2, QTableWidgetItem(f"{exec_time:.2f}"))  


                    self.compute_average_waiting_times()

                else:
                    QMessageBox.warning(self, "Error", "Invalid thread execution times format in the file.")
            else:
                QMessageBox.warning(self, "Error", "The file does not have a 'run_threads' function to execute the threads.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load file: {str(e)}")

    def clear_table(self):
        """Clears all rows from the process table."""
        self.process_table.setRowCount(0)