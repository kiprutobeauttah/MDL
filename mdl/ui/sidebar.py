"""Sidebar navigation."""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFrame
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QIcon
from mdl.core.config import config
from mdl.ui.icons import create_icon


class NavButton(QPushButton):
    """Navigation button."""
    
    def __init__(self, text: str, icon_name: str = ""):
        super().__init__(f"  {text}")
        self.setCheckable(True)
        self.setFixedHeight(40)
        self.setCursor(Qt.PointingHandCursor)
        
        # Set icon if provided
        if icon_name:
            self.setIcon(create_icon(icon_name, config.text_secondary, 18))
            self.setIconSize(QSize(18, 18))
        
        self.setStyleSheet(f"""
            NavButton {{
                background-color: transparent;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                color: {config.text_secondary};
                font-weight: 500;
                font-size: 14px;
                text-align: left;
            }}
            NavButton:hover {{
                background-color: {config.background_tertiary};
                color: {config.text_primary};
            }}
            NavButton:checked {{
                background-color: {config.accent_blush_red};
                color: #FFFFFF;
            }}
        """)


class NavSection(QWidget):
    """Navigation section with header."""
    
    def __init__(self, title: str):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 8, 0, 8)
        layout.setSpacing(4)
        
        # Section header
        header = QLabel(title)
        header.setStyleSheet(f"""
            color: {config.text_secondary};
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.5px;
            padding: 8px 16px 4px 16px;
        """)
        layout.addWidget(header)
        
        self.layout = layout
    
    def add_button(self, button: NavButton):
        """Add button to section."""
        self.layout.addWidget(button)


class Sidebar(QWidget):
    """Navigation sidebar."""
    
    # Signals for navigation
    nav_overview = Signal()
    nav_network = Signal()
    nav_wifi = Signal()
    nav_cellular = Signal()
    nav_bluetooth = Signal()
    nav_apps = Signal()
    nav_sensors = Signal()
    nav_battery = Signal()
    nav_performance = Signal()
    nav_storage = Signal()
    nav_settings = Signal()
    nav_sessions = Signal()
    nav_events = Signal()
    nav_alerts = Signal()
    
    def __init__(self):
        super().__init__()
        self.setFixedWidth(240)
        self._init_ui()
    
    def _init_ui(self):
        """Initialize UI."""
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {config.background_secondary};
                border-right: 1px solid {config.border_color};
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 20, 16, 20)
        layout.setSpacing(0)
        
        # App title
        title = QLabel("MDL")
        title.setStyleSheet(f"""
            color: {config.text_primary};
            font-size: 24px;
            font-weight: 700;
            padding: 0 16px 12px 16px;
        """)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Mobile Diagnostic Lab")
        subtitle.setStyleSheet(f"""
            color: {config.text_secondary};
            font-size: 10px;
            font-weight: 500;
            padding: 0 16px 20px 16px;
        """)
        layout.addWidget(subtitle)
        
        # Overview
        self.btn_overview = NavButton("Overview", "home")
        self.btn_overview.setChecked(True)
        self.btn_overview.clicked.connect(self.nav_overview.emit)
        layout.addWidget(self.btn_overview)
        
        # Separator
        layout.addWidget(self._separator())
        
        # Network section
        network_section = NavSection("NETWORK")
        
        self.btn_network = NavButton("Network", "activity")
        self.btn_network.clicked.connect(self.nav_network.emit)
        network_section.add_button(self.btn_network)
        
        self.btn_wifi = NavButton("Wi-Fi", "wifi")
        self.btn_wifi.clicked.connect(self.nav_wifi.emit)
        network_section.add_button(self.btn_wifi)
        
        self.btn_cellular = NavButton("Cellular", "smartphone")
        self.btn_cellular.clicked.connect(self.nav_cellular.emit)
        network_section.add_button(self.btn_cellular)
        
        self.btn_bluetooth = NavButton("Bluetooth", "bluetooth")
        self.btn_bluetooth.clicked.connect(self.nav_bluetooth.emit)
        network_section.add_button(self.btn_bluetooth)
        
        layout.addWidget(network_section)
        layout.addWidget(self._separator())
        
        # Device section
        device_section = NavSection("DEVICE")
        
        self.btn_apps = NavButton("Applications", "package")
        self.btn_apps.clicked.connect(self.nav_apps.emit)
        device_section.add_button(self.btn_apps)
        
        self.btn_sensors = NavButton("Sensors", "compass")
        self.btn_sensors.clicked.connect(self.nav_sensors.emit)
        device_section.add_button(self.btn_sensors)
        
        self.btn_battery = NavButton("Battery", "battery")
        self.btn_battery.clicked.connect(self.nav_battery.emit)
        device_section.add_button(self.btn_battery)
        
        self.btn_performance = NavButton("Performance", "cpu")
        self.btn_performance.clicked.connect(self.nav_performance.emit)
        device_section.add_button(self.btn_performance)
        
        self.btn_storage = NavButton("Storage", "hard-drive")
        self.btn_storage.clicked.connect(self.nav_storage.emit)
        device_section.add_button(self.btn_storage)
        
        self.btn_settings = NavButton("Settings", "settings")
        self.btn_settings.clicked.connect(self.nav_settings.emit)
        device_section.add_button(self.btn_settings)
        
        layout.addWidget(device_section)
        layout.addWidget(self._separator())
        
        # Analysis section
        analysis_section = NavSection("ANALYSIS")
        
        self.btn_sessions = NavButton("Sessions", "bar-chart-2")
        self.btn_sessions.clicked.connect(self.nav_sessions.emit)
        analysis_section.add_button(self.btn_sessions)
        
        self.btn_events = NavButton("Events", "file-text")
        self.btn_events.clicked.connect(self.nav_events.emit)
        analysis_section.add_button(self.btn_events)
        
        self.btn_alerts = NavButton("Alerts", "alert-triangle")
        self.btn_alerts.clicked.connect(self.nav_alerts.emit)
        analysis_section.add_button(self.btn_alerts)
        
        layout.addWidget(analysis_section)
        layout.addStretch()
        
        # Group buttons for exclusive selection
        self.nav_buttons = [
            self.btn_overview, self.btn_network, self.btn_wifi, self.btn_cellular,
            self.btn_bluetooth, self.btn_apps, self.btn_sensors, self.btn_battery,
            self.btn_performance, self.btn_storage, self.btn_settings,
            self.btn_sessions, self.btn_events, self.btn_alerts
        ]
        
        for btn in self.nav_buttons:
            btn.clicked.connect(lambda checked, b=btn: self._on_nav_clicked(b))
    
    def _separator(self) -> QFrame:
        """Create separator line."""
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet(f"background-color: {config.border_color}; max-height: 1px;")
        return line
    
    def _on_nav_clicked(self, button: NavButton):
        """Handle navigation button click."""
        for btn in self.nav_buttons:
            if btn != button:
                btn.setChecked(False)
