from PyQt6.QtWidgets import QMainWindow, QTabWidget
from ui.predictions_tab import PredictionsTab
from ui.graphs_tab import GraphsTab
from ui.about_tab import AboutTab
from ui.retrain import RetrainTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drawl Forecasting Software")
        self.setGeometry(300, 100, 1000, 600)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Add tabs
        self.tabs.addTab(PredictionsTab(), "Predictions")
        self.tabs.addTab(GraphsTab(), "Graphs")
        self.tabs.addTab(RetrainTab(), "Retrain")
        self.tabs.addTab(AboutTab(), "About")
        
