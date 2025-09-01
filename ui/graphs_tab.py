from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class GraphsTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Graphs will be shown here (e.g., forecast output)."))
        self.setLayout(layout)
