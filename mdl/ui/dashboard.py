"""Dashboard view."""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout
from PySide6.QtCore import Qt
from mdl.core.events import EventCategory, MetricEvent, metric_bus
from mdl.core.config import config


class MetricCard(QWidget):
    """Single metric card."""
    
    def __init__(self, title: str, unit: str = ""):
        super().__init__()
        self.unit = unit
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(8)
        
        # Title
        self.title_label = QLabel(title)
        self.title_label.setProperty("class", "metric-label")
        self.title_label.setStyleSheet(f"color: {config.text_secondary}; font-size: 12px; font-weight: 600;")
        
        # Value
        self.value_label = QLabel("--")
        self.value_label.setProperty("class", "metric-value")
        self.value_label.setStyleSheet(f"color: {config.text_primary}; font-size: 42px; font-weight: 700;")
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)
        layout.addStretch()
        
        # Card styling
        self.setStyleSheet(f"""
            MetricCard {{
                background-color: {config.background_secondary};
                border: 1px solid {config.border_color};
                border-radius: 12px;
            }}
        """)
        self.setMinimumHeight(140)
        self.setMinimumWidth(200)
    
    def update_value(self, value):
        """Update displayed value."""
        if isinstance(value, (int, float)):
            if isinstance(value, float):
                display = f"{value:.1f}{self.unit}"
            else:
                display = f"{value}{self.unit}"
        else:
            display = str(value)
        
        self.value_label.setText(display)


class Dashboard(QWidget):
    """Main dashboard."""
    
    def __init__(self):
        super().__init__()
        self._init_ui()
        self._subscribe_metrics()
    
    def _init_ui(self):
        """Initialize UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(28)
        
        # Header
        header = QLabel("OVERVIEW")
        header.setStyleSheet(f"color: {config.text_primary}; font-size: 20px; font-weight: 700; letter-spacing: 0.5px;")
        layout.addWidget(header)
        
        # Top metrics grid
        grid = QGridLayout()
        grid.setSpacing(20)
        grid.setContentsMargins(0, 0, 0, 0)
        
        self.battery_card = MetricCard("BATTERY", "%")
        self.cpu_card = MetricCard("CPU", "%")
        self.ram_card = MetricCard("RAM", "%")
        self.storage_card = MetricCard("STORAGE", "%")
        
        grid.addWidget(self.battery_card, 0, 0)
        grid.addWidget(self.cpu_card, 0, 1)
        grid.addWidget(self.ram_card, 1, 0)
        grid.addWidget(self.storage_card, 1, 1)
        
        layout.addLayout(grid)
        
        # Device info section
        info_container = QWidget()
        info_container.setStyleSheet(f"""
            QWidget {{
                background-color: {config.background_secondary};
                border: 1px solid {config.border_color};
                border-radius: 12px;
            }}
        """)
        info_layout = QVBoxLayout(info_container)
        info_layout.setContentsMargins(24, 20, 24, 20)
        info_layout.setSpacing(8)
        
        info_header = QLabel("DEVICE")
        info_header.setStyleSheet(f"color: {config.text_secondary}; font-size: 12px; font-weight: 600;")
        info_layout.addWidget(info_header)
        
        self.device_label = QLabel("No device connected")
        self.device_label.setStyleSheet(f"color: {config.text_primary}; font-size: 22px; font-weight: 600;")
        info_layout.addWidget(self.device_label)
        
        self.android_label = QLabel("")
        self.android_label.setStyleSheet(f"color: {config.text_secondary}; font-size: 14px;")
        info_layout.addWidget(self.android_label)
        
        # Additional device details
        details_layout = QGridLayout()
        details_layout.setSpacing(16)
        details_layout.setContentsMargins(0, 12, 0, 0)
        
        self.detail_labels = {}
        detail_fields = [
            ("Serial", "serial"),
            ("Build", "build"),
            ("Security Patch", "security_patch"),
            ("CPU Architecture", "cpu_arch"),
            ("Uptime", "uptime"),
        ]
        
        row = 0
        for label_text, key in detail_fields:
            label = QLabel(label_text)
            label.setStyleSheet(f"color: {config.text_secondary}; font-size: 11px; font-weight: 600;")
            
            value = QLabel("--")
            value.setStyleSheet(f"color: {config.text_primary}; font-size: 13px;")
            
            details_layout.addWidget(label, row, 0)
            details_layout.addWidget(value, row, 1)
            
            self.detail_labels[key] = value
            row += 1
        
        info_layout.addLayout(details_layout)
        
        layout.addWidget(info_container)
        layout.addStretch()
    
    def _subscribe_metrics(self):
        """Subscribe to metric events."""
        metric_bus.subscribe(EventCategory.BATTERY, self._on_battery_metric)
        metric_bus.subscribe(EventCategory.PERFORMANCE, self._on_performance_metric)
        metric_bus.subscribe(EventCategory.DEVICE, self._on_device_metric)
    
    def _on_battery_metric(self, event: MetricEvent):
        """Handle battery metrics."""
        if event.metric == "level":
            self.battery_card.update_value(event.value)
    
    def _on_performance_metric(self, event: MetricEvent):
        """Handle performance metrics."""
        if event.metric == "ram_used":
            self._ram_used = event.value
            self._update_ram()
        elif event.metric == "ram_total":
            self._ram_total = event.value
            self._update_ram()
        elif event.metric == "storage_used":
            self._storage_used = event.value
            self._update_storage()
    
    def _on_device_metric(self, event: MetricEvent):
        """Handle device metrics."""
        if event.metric == "model":
            manufacturer = getattr(self, '_manufacturer', '')
            self.device_label.setText(f"{manufacturer} {event.value}")
        elif event.metric == "manufacturer":
            self._manufacturer = event.value
        elif event.metric == "android_version":
            sdk = getattr(self, '_sdk', '')
            self.android_label.setText(f"Android {event.value} (SDK {sdk})")
        elif event.metric == "sdk_level":
            self._sdk = event.value
        elif event.metric in self.detail_labels:
            self.detail_labels[event.metric].setText(str(event.value))
    
    def _update_ram(self):
        """Update RAM percentage."""
        if hasattr(self, '_ram_used') and hasattr(self, '_ram_total'):
            if self._ram_total > 0:
                percent = int((self._ram_used / self._ram_total) * 100)
                self.ram_card.update_value(percent)
    
    def _update_storage(self):
        """Update storage percentage."""
        if hasattr(self, '_storage_used'):
            # Assume 256GB for now - will get from device info later
            total = 256 * 1024  # MB
            percent = int((self._storage_used / total) * 100)
            self.storage_card.update_value(percent)
