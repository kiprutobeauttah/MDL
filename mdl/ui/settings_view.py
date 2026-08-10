"""Settings view."""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout
from PySide6.QtCore import Qt
from mdl.core.config import config


class SettingsGroup(QWidget):
    """Settings group widget."""
    
    def __init__(self, title: str):
        super().__init__()
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet(f"color: {config.text_secondary}; font-size: 11px; font-weight: 600;")
        layout.addWidget(title_label)
        
        # Settings grid
        self.settings_grid = QGridLayout()
        self.settings_grid.setSpacing(16)
        layout.addLayout(self.settings_grid)
        
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {config.background_secondary};
                border: 1px solid {config.border_color};
                border-radius: 10px;
            }}
        """)
    
    def add_setting(self, label: str, value: str):
        """Add setting to grid."""
        row = self.settings_grid.rowCount()
        
        label_widget = QLabel(label)
        label_widget.setStyleSheet(f"color: {config.text_secondary}; font-size: 12px;")
        
        value_widget = QLabel(value)
        value_widget.setStyleSheet(f"color: {config.text_primary}; font-size: 13px; font-weight: 500;")
        
        self.settings_grid.addWidget(label_widget, row, 0)
        self.settings_grid.addWidget(value_widget, row, 1)


class SettingsView(QWidget):
    """System settings view."""
    
    def __init__(self):
        super().__init__()
        self._init_ui()
    
    def _init_ui(self):
        """Initialize UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(24)
        
        # Header
        header = QLabel("SETTINGS")
        header.setStyleSheet(f"color: {config.text_primary}; font-size: 20px; font-weight: 700;")
        layout.addWidget(header)
        
        # Info
        info = QLabel("Read-only view of device system settings")
        info.setStyleSheet(f"color: {config.text_secondary}; font-size: 13px;")
        layout.addWidget(info)
        
        # Display settings
        display_group = SettingsGroup("DISPLAY")
        display_group.add_setting("Brightness", "Auto")
        display_group.add_setting("Screen Timeout", "30 seconds")
        display_group.add_setting("Dark Mode", "Enabled")
        layout.addWidget(display_group)
        
        # Sound settings
        sound_group = SettingsGroup("SOUND")
        sound_group.add_setting("Media Volume", "70%")
        sound_group.add_setting("Ring Volume", "80%")
        sound_group.add_setting("Notification Volume", "60%")
        layout.addWidget(sound_group)
        
        # Developer options
        dev_group = SettingsGroup("DEVELOPER")
        dev_group.add_setting("USB Debugging", "Enabled")
        dev_group.add_setting("Stay Awake", "Disabled")
        dev_group.add_setting("Show Taps", "Disabled")
        layout.addWidget(dev_group)
        
        layout.addStretch()
