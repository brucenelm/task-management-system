import sys
from PyQt5.QtWidgets import QApplication,QWidget, QPushButton, QVBoxLayout,QLabel

app =QApplication(sys.argv) 

class MainWindow(QWidget):
    def __init__(self):
     super().__init__()
     self.setWindowTitle("My PYQT App")
     self.resize(400, 300)
    
    
     self.label = QLabel("Hello PYQT!")
    
     self.button =QPushButton("click me")
     self.button.clicked.connect(self.on_click)
    
     layout =QVBoxLayout()
     layout.addWidget(self.label)
     layout.addWidget(self.button)
    
     self.setLayout(layout)
    
    def on_click(self):
        self.label.setText("Button Clicked")
        
        button = QPushButton("Click Me")
        button.setStyleSheet("""
    QPushButton {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        padding: 10px;
    }
    QPushButton:hover {
        background-color: #45a049;
    }
""")

    button = QPushButton("Click Me")
      
    button.setStyleSheet("""
    QPushButton {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        padding: 10px;
    }
    QPushButton:hover {
        background-color: #45a049;
    }
""")
window = MainWindow()      
window.show()

sys.exit(app.exec_())