"""Placeholder view for unimplemented features."""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from mdl.core.config import config


class PlaceholderView(QWidget):
    """Placeholder view."""
    
    def __init__(self, feature: str = "Feature"):
        super().__init__()
        self.feature = feature
        self._init_ui()
    
    def _init_ui(self):
        """Initialize UI."""
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        
        # Icon
        icon = QLabel("🚧")
        icon.setStyleSheet("font-size: 64px;")
        icon.setAlignment(Qt.AlignCenter)
        
        # Title
        self.title = QLabel(f"{self.feature}")
        self.title.setStyleSheet(f"""
            color: {config.text_primary};
            font-size: 24px;
            font-weight: 700;
        """)
        self.title.setAlignment(Qt.AlignCenter)
        
        # Message
        message = QLabel("This feature is coming in a future release")
        message.setStyleSheet(f"""
            color: {config.text_secondary};
            font-size: 14px;
        """)
        message.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(icon)
        layout.addWidget(self.title)
        layout.addWidget(message)
    
    def set_feature(self, feature: str):
        """Set feature name."""
        self.feature = feature
        self.title.setText(feature)
