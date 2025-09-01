import sys
from PyQt6.QtWidgets import QApplication, QMessageBox
from ui.main_window import MainWindow

# --- Global Exception Handler is set here ---
def custom_exception_hook(exc_type, exc_value, exc_traceback):
    """
    Catches all unhandled exceptions and displays a message box.
    """
    # Create a message with the exception details
    error_message = f"An unexpected error has occurred.\n\nType: {exc_type.__name__}\nValue: {exc_value}"
    
    # Display the error in a pop-up message box
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Icon.Critical)
    msg_box.setWindowTitle("Application Error")
    msg_box.setText("The application encountered a fatal error.")
    msg_box.setInformativeText(error_message)
    msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg_box.exec()

    # The program will not exit unless you uncomment this line.
    # sys.exit(1)

# Set the custom function as the global exception handler
sys.excepthook = custom_exception_hook
# --- End of Global Exception Handler ---

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())