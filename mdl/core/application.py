"""Main application controller."""

from PySide6.QtWidgets import QMainWindow
from mdl.ui.main_window import MainWindow


class MDLApplication(QMainWindow):
    """MDL application."""
    
    def __init__(self):
        super().__init__()
        self.main_window = MainWindow()
    
    def show(self):
        """Show application window."""
        self.main_window.show()
