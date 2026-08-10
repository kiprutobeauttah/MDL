"""Sensors laboratory view."""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout,
    QListWidget, QListWidgetItem, QPushButton
)
from PySide6.QtCore import Qt
import pyqtgraph as pg
from collections import deque
from mdl.core.events import EventCategory, MetricEvent, metric_bus
from mdl.core.config import config


class SensorCard(QWidget):
    """Sensor info card."""
    
    def __init__(self, name: str, sensor_type: str):
        super().__init__()
        self.sensor_name = name
        self.sensor_type = sensor_type
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(6)
        
        # Name
        name_label = QLabel(name)
        name_label.setStyleSheet(f"color: {config.text_primary}; font-weight: 600; font-size: 14px;")
        
        # Type
        type_label = QLabel(sensor_type)
        type_label.setStyleSheet(f"color: {config.text_secondary}; font-size: 11px;")
        
        # Values
        self.value_label = QLabel("--")
        self.value_label.setStyleSheet(f"color: {config.text_primary}; font-size: 13px;")
        
        layout.addWidget(name_label)
        layout.addWidget(type_label)
        layout.addWidget(self.value_label)
        
        self.setMinimumHeight(90)
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {config.background_secondary};
                border: 1px solid {config.border_color};
                border-radius: 8px;
            }}
        """)
    
    def update_values(self, values: list):
        """Update sensor values."""
        if len(values) == 3:
            self.value_label.setText(f"X: {values[0]:.2f}\nY: {values[1]:.2f}\nZ: {values[2]:.2f}")
        elif len(values) == 1:
            self.value_label.setText(f"{values[0]:.2f}")
        else:
            self.value_label.setText(", ".join([f"{v:.2f}" for v in values]))


class SensorsView(QWidget):
    """Sensors laboratory view."""
    
    def __init__(self):
        super().__init__()
        self.sensor_cards = {}
        self._init_ui()
        self._subscribe()
    
    def _init_ui(self):
        """Initialize UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(24)
        
        # Header
        header = QLabel("SENSORS")
        header.setStyleSheet(f"color: {config.text_primary}; font-size: 20px; font-weight: 700;")
        layout.addWidget(header)
        
        # Info
        info_label = QLabel("Available device sensors with live readings")
        info_label.setStyleSheet(f"color: {config.text_secondary}; font-size: 13px;")
        layout.addWidget(info_label)
        
        # Sensors grid
        self.sensors_grid = QGridLayout()
        self.sensors_grid.setSpacing(16)
        layout.addLayout(self.sensors_grid)
        
        layout.addStretch()
        
        # Add common sensors as placeholders
        self._add_sensor_placeholders()
    
    def _add_sensor_placeholders(self):
        """Add placeholder sensor cards."""
        common_sensors = [
            ("Accelerometer", "TYPE_ACCELEROMETER"),
            ("Gyroscope", "TYPE_GYROSCOPE"),
            ("Magnetometer", "TYPE_MAGNETIC_FIELD"),
            ("Light", "TYPE_LIGHT"),
            ("Proximity", "TYPE_PROXIMITY"),
            ("Pressure", "TYPE_PRESSURE"),
            ("Temperature", "TYPE_AMBIENT_TEMPERATURE"),
            ("Humidity", "TYPE_RELATIVE_HUMIDITY"),
        ]
        
        row = 0
        col = 0
        for name, sensor_type in common_sensors:
            card = SensorCard(name, sensor_type)
            self.sensor_cards[sensor_type] = card
            self.sensors_grid.addWidget(card, row, col)
            
            col += 1
            if col >= 2:
                col = 0
                row += 1
    
    def _subscribe(self):
        """Subscribe to sensor metrics."""
        metric_bus.subscribe(EventCategory.SENSOR, self._on_sensor_metric)
    
    def _on_sensor_metric(self, event: MetricEvent):
        """Handle sensor metric."""
        if event.metric in self.sensor_cards:
            self.sensor_cards[event.metric].update_values(event.value)
