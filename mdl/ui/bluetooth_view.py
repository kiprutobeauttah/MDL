"""Bluetooth monitoring view."""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout,
    QListWidget, QListWidgetItem
)
from PySide6.QtCore import Qt
from mdl.core.events import EventCategory, MetricEvent, metric_bus
from mdl.core.config import config


class BluetoothDeviceItem(QWidget):
    """Bluetooth device list item."""
    
    def __init__(self, name: str, address: str, paired: bool, connected: bool):
        super().__init__()
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        
        # Status indicator
        if connected:
            indicator = QLabel("●")
            indicator.setStyleSheet(f"color: {config.accent_green}; font-size: 18px;")
        elif paired:
            indicator = QLabel("○")
            indicator.setStyleSheet(f"color: {config.accent_blush_red}; font-size: 18px;")
        else:
            indicator = QLabel("○")
            indicator.setStyleSheet(f"color: {config.text_secondary}; font-size: 18px;")
        
        # Device info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)
        
        name_label = QLabel(name if name else "Unknown Device")
        name_label.setStyleSheet(f"color: {config.text_primary}; font-weight: 500; font-size: 14px;")
        
        address_label = QLabel(address)
        address_label.setStyleSheet(f"color: {config.text_secondary}; font-size: 11px;")
        
        status_text = "Connected" if connected else ("Paired" if paired else "Available")
        status_label = QLabel(status_text)
        status_label.setStyleSheet(f"color: {config.text_secondary}; font-size: 11px;")
        
        info_layout.addWidget(name_label)
        info_layout.addWidget(address_label)
        info_layout.addWidget(status_label)
        
        layout.addWidget(indicator)
        layout.addLayout(info_layout)
        layout.addStretch()
        
        self.setMinimumHeight(80)


class BluetoothView(QWidget):
    """Bluetooth monitoring view."""
    
    def __init__(self):
        super().__init__()
        self._init_ui()
        self._subscribe()
    
    def _init_ui(self):
        """Initialize UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(24)
        
        # Header
        header_layout = QHBoxLayout()
        
        header = QLabel("BLUETOOTH")
        header.setStyleSheet(f"color: {config.text_primary}; font-size: 20px; font-weight: 700;")
        
        self.status_label = QLabel("● Disabled")
        self.status_label.setStyleSheet(f"color: {config.text_secondary}; font-size: 14px;")
        
        header_layout.addWidget(header)
        header_layout.addStretch()
        header_layout.addWidget(self.status_label)
        
        layout.addLayout(header_layout)
        
        # Adapter info
        adapter_container = QWidget()
        adapter_container.setStyleSheet(f"""
            QWidget {{
                background-color: {config.background_secondary};
                border: 1px solid {config.border_color};
                border-radius: 10px;
            }}
        """)
        adapter_layout = QGridLayout(adapter_container)
        adapter_layout.setContentsMargins(24, 20, 24, 20)
        adapter_layout.setSpacing(16)
        
        adapter_header = QLabel("ADAPTER")
        adapter_header.setStyleSheet(f"color: {config.text_secondary}; font-size: 11px; font-weight: 600;")
        adapter_layout.addWidget(adapter_header, 0, 0, 1, 2)
        
        self.detail_labels = {}
        details = [
            ("Address", "adapter_address"),
            ("Name", "adapter_name"),
            ("State", "adapter_state"),
        ]
        
        row = 1
        for label_text, key in details:
            label = QLabel(label_text)
            label.setStyleSheet(f"color: {config.text_secondary}; font-size: 11px; font-weight: 600;")
            
            value = QLabel("--")
            value.setStyleSheet(f"color: {config.text_primary}; font-size: 14px;")
            
            adapter_layout.addWidget(label, row, 0)
            adapter_layout.addWidget(value, row, 1)
            
            self.detail_labels[key] = value
            row += 1
        
        layout.addWidget(adapter_container)
        
        # Devices section
        devices_header_layout = QHBoxLayout()
        
        devices_title = QLabel("DEVICES")
        devices_title.setStyleSheet(f"color: {config.text_secondary}; font-size: 12px; font-weight: 600;")
        
        self.device_count_label = QLabel("0 devices")
        self.device_count_label.setStyleSheet(f"color: {config.text_secondary}; font-size: 12px;")
        
        devices_header_layout.addWidget(devices_title)
        devices_header_layout.addStretch()
        devices_header_layout.addWidget(self.device_count_label)
        
        layout.addLayout(devices_header_layout)
        
        # Devices list
        self.devices_list = QListWidget()
        self.devices_list.setStyleSheet(f"""
            QListWidget {{
                background-color: {config.background_secondary};
                border: 1px solid {config.border_color};
                border-radius: 10px;
                padding: 8px;
            }}
            QListWidget::item {{
                background-color: transparent;
                border-radius: 6px;
                margin: 2px;
            }}
            QListWidget::item:hover {{
                background-color: {config.background_tertiary};
            }}
            QListWidget::item:selected {{
                background-color: {config.background_tertiary};
                border: 1px solid {config.accent_blush_red};
            }}
        """)
        
        layout.addWidget(self.devices_list)
    
    def _subscribe(self):
        """Subscribe to bluetooth metrics."""
        metric_bus.subscribe(EventCategory.NETWORK, self._on_bluetooth_metric)
    
    def _on_bluetooth_metric(self, event: MetricEvent):
        """Handle bluetooth metric."""
        if event.source != "bluetooth":
            return
        
        if event.metric == "enabled":
            if event.value:
                self.status_label.setText("● Enabled")
                self.status_label.setStyleSheet(f"color: {config.accent_green}; font-size: 14px;")
            else:
                self.status_label.setText("● Disabled")
                self.status_label.setStyleSheet(f"color: {config.text_secondary}; font-size: 14px;")
        
        elif event.metric == "devices":
            self._update_devices(event.value)
        
        elif event.metric in self.detail_labels:
            self.detail_labels[event.metric].setText(str(event.value))
    
    def _update_devices(self, devices: list):
        """Update devices list."""
        self.devices_list.clear()
        self.device_count_label.setText(f"{len(devices)} devices")
        
        for device in devices:
            item = QListWidgetItem(self.devices_list)
            widget = BluetoothDeviceItem(
                device.get("name", "Unknown"),
                device.get("address", ""),
                device.get("paired", False),
                device.get("connected", False)
            )
            item.setSizeHint(widget.sizeHint())
            self.devices_list.addItem(item)
            self.devices_list.setItemWidget(item, widget)
