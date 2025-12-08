import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
    QLineEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt

TASKS_FILE = "tasks.json"

class TaskManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt Task Manager")
        self.setGeometry(300, 100, 400, 400)
        self.tasks = []

        self.init_ui()
        self.load_tasks()

    def init_ui(self):
        layout = QVBoxLayout()

        # Task list
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        # Input + buttons
        input_layout = QHBoxLayout()
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter a new task...")
        input_layout.addWidget(self.task_input)

        add_btn = QPushButton("Add")
        add_btn.clicked.connect(self.add_task)
        input_layout.addWidget(add_btn)

        remove_btn = QPushButton("Remove")
        remove_btn.clicked.connect(self.remove_task)
        input_layout.addWidget(remove_btn)

        layout.addLayout(input_layout)

        self.setLayout(layout)

    def add_task(self):
        task_text = self.task_input.text().strip()
        if task_text:
            self.tasks.append(task_text)
            self.list_widget.addItem(task_text)
            self.task_input.clear()
            self.save_tasks()
        else:
            QMessageBox.warning(self, "Warning", "Task cannot be empty!")

    def remove_task(self):
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "Select a task to remove!")
            return
        for item in selected_items:
            self.tasks.remove(item.text())
            self.list_widget.takeItem(self.list_widget.row(item))
        self.save_tasks()

    def load_tasks(self):
        try:
            with open(TASKS_FILE, "r") as f:
                self.tasks = json.load(f)
                self.list_widget.addItems(self.tasks)
        except FileNotFoundError:
            self.tasks = []

    def save_tasks(self):
        with open(TASKS_FILE, "w") as f:
            json.dump(self.tasks, f, indent=4)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TaskManager()
    window.show()
    sys.exit(app.exec())
