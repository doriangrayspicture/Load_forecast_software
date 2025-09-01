from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QFileDialog, QMessageBox, QGroupBox, QGridLayout, QDateEdit,
    QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import QDate
import pandas as pd

# Import LSTM backend
from predictions_script.pred_lstm2 import run_prediction as lstm_predict


class PredictionsTab(QWidget):
    def __init__(self):
        super().__init__()

        # MAIN layout
        main_layout = QVBoxLayout()

        # 🔹 DATE SELECTION
        date_layout = QHBoxLayout()
        date_label = QLabel("Select Prediction Date:")
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.date_input)
        main_layout.addLayout(date_layout)

        # 🔸 SPLIT LAYOUT (Left: models | Right: master)
        split_layout = QHBoxLayout()

        # ▶ LEFT: Model Buttons
        models_group = QGroupBox("Run Specific Models")
        models_layout = QGridLayout()
        model_names = [
            "LSTM", "Random Forest", "XGBoost", "ARIMA", "SVR",
            "Prophet", "GRU", "LightGBM", "CatBoost", "Ensemble"
        ]

        for i, name in enumerate(model_names):
            btn = QPushButton(f"Run {name}")
            btn.clicked.connect(lambda checked, n=name: self.run_model(n))
            row, col = divmod(i, 2)  # 2 columns
            models_layout.addWidget(btn, row, col)

        models_group.setLayout(models_layout)
        split_layout.addWidget(models_group)

        # ▶ RIGHT: Master Button
        master_group = QGroupBox("Master Model Control")
        master_layout = QVBoxLayout()
        run_all_btn = QPushButton("Run All Models")
        run_all_btn.clicked.connect(self.run_all_models)
        master_layout.addWidget(run_all_btn)
        master_group.setLayout(master_layout)
        split_layout.addWidget(master_group)

        # Add split layout to main layout
        main_layout.addLayout(split_layout)

        # 🔻 Upload Button
        upload_btn = QPushButton("Upload Data File")
        upload_btn.clicked.connect(self.upload_file)
        main_layout.addWidget(upload_btn)

        # 🔹 Prediction Table
        self.pred_table = QTableWidget()
        self.pred_table.setColumnCount(3)
        self.pred_table.setHorizontalHeaderLabels(["Date", "Block No", "Predicted Drawl"])
        main_layout.addWidget(QLabel("Predictions:"))
        main_layout.addWidget(self.pred_table)

        # 🔹 Metrics Table
        self.metrics_table = QTableWidget()
        self.metrics_table.setColumnCount(2)
        self.metrics_table.setHorizontalHeaderLabels(["Metric", "Value"])
        main_layout.addWidget(QLabel("Metrics:"))
        main_layout.addWidget(self.metrics_table)

        self.setLayout(main_layout)

    def run_all_models(self):
        selected_date = self.date_input.date().toString("yyyy-MM-dd").date()
        QMessageBox.information(self, "Run All", f"Running all models for date: {selected_date}")

    def run_model(self, model_name):
        selected_date = pd.Timestamp(self.date_input.date().toString("yyyy-MM-dd"))

        if not hasattr(self, "data_file"):
            QMessageBox.warning(self, "Error", "Please upload a dataset first.")
            return

        if model_name == "LSTM":
            # Run LSTM backend
            try:
                df_pred, metrics = lstm_predict(self.data_file, selected_date)

            # Display predictions
                self.pred_table.setRowCount(len(df_pred))
                for i, row in df_pred.iterrows():
                    self.pred_table.setItem(i, 0, QTableWidgetItem(str(row["Date"].date())))
                    self.pred_table.setItem(i, 1, QTableWidgetItem(str(row["block_no"])))
                    self.pred_table.setItem(i, 2, QTableWidgetItem(str(round(row["Predicted_Drawl"], 2))))

            # Display metrics
                self.metrics_table.setRowCount(len(metrics))
                for i, (k, v) in enumerate(metrics.items()):
                    self.metrics_table.setItem(i, 0, QTableWidgetItem(k))
                    self.metrics_table.setItem(i, 1, QTableWidgetItem(str(round(v, 4))))

                QMessageBox.information(self, "Done", "LSTM prediction complete and displayed.")
            #else:
            #    QMessageBox.information(self, model_name, f"{model_name} model will run for date: {selected_date.date()}")
            except Exception as e:
                QMessageBox.critical(self, "Prediction Error", str(e))
    def upload_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select File", "", "Excel Files (*.xlsx);;CSV Files (*.csv)")
        if file:
            self.data_file = file  # store it
            QMessageBox.information(self, "File Selected", f"You selected:\n{file}")
