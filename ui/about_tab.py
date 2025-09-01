from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

class AboutTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        text = QLabel("""
        <h2>Drawl Forecasting Software</h2>
        <p><b>Version:</b> 1.0</p>
        <p><b>Purpose:</b> Predict energy drawl using ML models.</p>
        <p><b>Author:</b> Your Name</p>
        <p><b>Email:</b> your.email@example.com</p>
        """)
        text.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(text)

        self.setLayout(layout)
