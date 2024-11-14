import sys
from PySide6.QtWidgets import QApplication
from gui import Scheduler

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Scheduler()
    window.resize(600, 500)
    window.show()
    sys.exit(app.exec())
