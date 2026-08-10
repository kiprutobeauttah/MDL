"""Alerts view."""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout,
    QListWidget, QListWidgetItem, QPushButton
)
from PySide6.QtCore import Qt
from mdl.core.config import config


class AlertCard(QWidget):
    """Alert configuration card."""
    
    def __init__(self, name: str, condition: str, severity: str):
        super().__init__()
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(8)
        
        # Header
        header_layout = QHBoxLayout()
        
        name_label = QLabel(name)
        name_label.setStyleSheet(f"color: {config.text_primary}; font-size: 14px; font-weight: 600;")
        
        severity_color = {
            "INFO": config.accent_green,
            "WARNING": config.accent_yellow,
            "CRITICAL": config.accent_red,
        }.get(severity, config.text_secondary)
        
        severity_label = QLabel(severity)
        severity_label.setStyleSheet(f"color: {severity_color}; font-size: 11px; font-weight: 600;")
        
        header_layout.addWidget(name_label)
        header_layout.addStretch()
        header_layout.addWidget(severity_label)
        
        # Condition
        condition_label = QLabel(condition)
        condition_label.setStyleSheet(f"color: {config.text_secondary}; font-size: 12px;")
        condition_label.setWordWrap(True)
        
        # Status
        status_label = QLabel("● Active")
        status_label.setStyleSheet(f"color: {config.accent_green}; font-size: 11px;")
        
        layout.addLayout(header_layout)
        layout.addWidget(condition_label)
        layout.addWidget(status_label)
        
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {config.background_secondary};
                border: 1px solid {config.border_color};
                border-radius: 10px;
            }}
        """)
        self.setMinimumHeight(110)


class AlertsView(QWidget):
    """Alerts configuration and monitoring view."""
    
    def __init__(self):
        super().__init__()
        self._init_ui()
    
    def _init_ui(self):
        """Initialize UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(24)
        
        # Header
        header_layout = QHBoxLayout()
        
        header = QLabel("ALERTS")
        header.setStyleSheet(f"color: {config.text_primary}; font-size: 20px; font-weight: 700;")
        
        add_btn = QPushButton("+ New Alert")
        
        header_layout.addWidget(header)
        header_layout.addStretch()
        header_layout.addWidget(add_btn)
        
        layout.addLayout(header_layout)
        
        # Info
        info = QLabel("Configure alerts for device metrics and network conditions")
        info.setStyleSheet(f"color: {config.text_secondary}; font-size: 13px;")
        layout.addWidget(info)
        
        # Alerts grid
        alerts_grid = QGridLayout()
        alerts_grid.setSpacing(16)
        
        # Sample alerts
        battery_alert = AlertCard(
            "Low Battery",
            "Battery level < 20%",
            "WARNING"
        )
        
        temp_alert = AlertCard(
            "High Temperature",
            "Battery temp > 40°C",
            "CRITICAL"
        )
        
        signal_alert = AlertCard(
            "Poor Wi-Fi Signal",
            "Wi-Fi RSSI < -70 dBm",
            "WARNING"
        )
        
        latency_alert = AlertCard(
            "High Latency",
            "Network latency > 100ms",
            "INFO"
        )
        
        alerts_grid.addWidget(battery_alert, 0, 0)
        alerts_grid.addWidget(temp_alert, 0, 1)
        alerts_grid.addWidget(signal_alert, 1, 0)
        alerts_grid.addWidget(latency_alert, 1, 1)
        
        layout.addLayout(alerts_grid)
        layout.addStretch()
