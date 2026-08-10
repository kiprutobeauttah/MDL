"""Battery monitoring view."""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QProgressBar
from PySide6.QtCore import Qt
from mdl.core.events import EventCategory, MetricEvent, metric_bus
from mdl.core.config import config
import pyqtgraph as pg


class BatteryMetricCard(QWidget):
    """Battery metric card."""
    
    def __init__(self, title: str, unit: str = ""):
        super().__init__()
        self.unit = unit
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(6)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet(f"color: {config.text_secondary}; font-size: 11px; font-weight: 600;")
        
        # Value
        self.value_label = QLabel("--")
        self.value_label.setStyleSheet(f"color: {config.text_primary}; font-size: 28px; font-weight: 700;")
        
        layout.addWidget(title_label)
        layout.addWidget(self.value_label)
        layout.addStretch()
        
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {config.background_secondary};
                border: 1px solid {config.border_color};
                border-radius: 10px;
            }}
        """)
        self.setMinimumHeight(100)
    
    def update_value(self, value):
        """Update value."""
        if isinstance(value, float):
            self.value_label.setText(f"{value:.1f}{self.unit}")
        elif isinstance(value, int):
            self.value_label.setText(f"{value}{self.unit}")
        else:
            self.value_label.setText(str(value))


class BatteryView(QWidget):
    """Battery monitoring view."""
    
    def __init__(self):
        super().__init__()
        self._init_ui()
        self._subscribe()
        
        # History data
        self.level_history = []
        self.temp_history = []
        self.voltage_history = []
        self.max_history = 60  # Keep 60 data points
    
    def _init_ui(self):
        """Initialize UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(24)
        
        # Header
        header = QLabel("BATTERY")
        header.setStyleSheet(f"color: {config.text_primary}; font-size: 20px; font-weight: 700;")
        layout.addWidget(header)
        
        # Metrics grid
        grid = QGridLayout()
        grid.setSpacing(16)
        
        self.level_card = BatteryMetricCard("LEVEL", "%")
        self.temp_card = BatteryMetricCard("TEMPERATURE", "°C")
        self.voltage_card = BatteryMetricCard("VOLTAGE", "V")
        self.status_card = BatteryMetricCard("STATUS")
        
        grid.addWidget(self.level_card, 0, 0)
        grid.addWidget(self.temp_card, 0, 1)
        grid.addWidget(self.voltage_card, 1, 0)
        grid.addWidget(self.status_card, 1, 1)
        
        layout.addLayout(grid)
        
        # Battery level progress bar
        progress_container = QWidget()
        progress_container.setStyleSheet(f"""
            QWidget {{
                background-color: {config.background_secondary};
                border: 1px solid {config.border_color};
                border-radius: 10px;
            }}
        """)
        progress_layout = QVBoxLayout(progress_container)
        progress_layout.setContentsMargins(20, 16, 20, 16)
        
        progress_label = QLabel("CHARGE LEVEL")
        progress_label.setStyleSheet(f"color: {config.text_secondary}; font-size: 11px; font-weight: 600;")
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFixedHeight(30)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                border-radius: 6px;
                background-color: {config.background_tertiary};
                text-align: center;
                color: {config.text_primary};
                font-weight: 600;
            }}
            QProgressBar::chunk {{
                background-color: {config.accent_green};
                border-radius: 6px;
            }}
        """)
        
        progress_layout.addWidget(progress_label)
        progress_layout.addWidget(self.progress_bar)
        
        layout.addWidget(progress_container)
        
        # Additional info
        info_container = QWidget()
        info_container.setStyleSheet(f"""
            QWidget {{
                background-color: {config.background_secondary};
                border: 1px solid {config.border_color};
                border-radius: 10px;
            }}
        """)
        info_layout = QGridLayout(info_container)
        info_layout.setContentsMargins(20, 16, 20, 16)
        info_layout.setSpacing(12)
        
        self.detail_labels = {}
        details = [
            ("Health", "health"),
            ("Technology", "technology"),
            ("Plugged", "plugged"),
        ]
        
        row = 0
        for label_text, key in details:
            label = QLabel(label_text)
            label.setStyleSheet(f"color: {config.text_secondary}; font-size: 11px; font-weight: 600;")
            
            value = QLabel("--")
            value.setStyleSheet(f"color: {config.text_primary}; font-size: 14px;")
            
            info_layout.addWidget(label, row, 0)
            info_layout.addWidget(value, row, 1)
            
            self.detail_labels[key] = value
            row += 1
        
        layout.addWidget(info_container)
        layout.addStretch()
    
    def _subscribe(self):
        """Subscribe to battery metrics."""
        metric_bus.subscribe(EventCategory.BATTERY, self._on_battery_metric)
    
    def _on_battery_metric(self, event: MetricEvent):
        """Handle battery metric."""
        if event.metric == "level":
            self.level_card.update_value(event.value)
            self.progress_bar.setValue(event.value)
            
            # Update progress bar color based on level
            if event.value < 20:
                chunk_color = config.accent_red
            elif event.value < 50:
                chunk_color = config.accent_yellow
            else:
                chunk_color = config.accent_green
            
            self.progress_bar.setStyleSheet(f"""
                QProgressBar {{
                    border: none;
                    border-radius: 6px;
                    background-color: {config.background_tertiary};
                    text-align: center;
                    color: {config.text_primary};
                    font-weight: 600;
                }}
                QProgressBar::chunk {{
                    background-color: {chunk_color};
                    border-radius: 6px;
                }}
            """)
            
        elif event.metric == "temperature":
            self.temp_card.update_value(event.value)
        elif event.metric == "voltage":
            self.voltage_card.update_value(event.value)
        elif event.metric == "status":
            self.status_card.update_value(event.value)
        elif event.metric in self.detail_labels:
            self.detail_labels[event.metric].setText(str(event.value))
