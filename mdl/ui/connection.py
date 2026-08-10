"""Connection manager UI."""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QListWidget, QListWidgetItem
)
from PySide6.QtCore import Qt, Signal
from mdl.adb.client import ConnectionType
from mdl.core.config import config


class DeviceItem(QWidget):
    """Single device list item."""
    
    def __init__(self, serial: str, device_state: str, connection_type: ConnectionType):
        super().__init__()
        self.serial = serial
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        
        # Connection indicator
        indicator = QLabel("●" if device_state == "device" else "○")
        indicator_color = config.accent_green if device_state == "device" else config.text_secondary
        indicator.setStyleSheet(f"color: {indicator_color}; font-size: 20px;")
        indicator.setFixedWidth(30)
        
        # Device info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)
        
        serial_label = QLabel(serial)
        serial_label.setStyleSheet(f"color: {config.text_primary}; font-weight: 500; font-size: 14px;")
        
        type_label = QLabel(f"{connection_type.value.upper()} • {device_state.upper()}")
        type_label.setStyleSheet(f"color: {config.text_secondary}; font-size: 11px;")
        
        info_layout.addWidget(serial_label)
        info_layout.addWidget(type_label)
        
        layout.addWidget(indicator)
        layout.addLayout(info_layout)
        layout.addStretch()
        
        self.setMinimumHeight(60)


class ConnectionPanel(QWidget):
    """Device connection panel."""
    
    device_selected = Signal(str)  # Emits device serial
    
    def __init__(self):
        super().__init__()
        self._init_ui()
    
    def _init_ui(self):
        """Initialize UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        # Header
        header = QLabel("CONNECT DEVICE")
        header.setStyleSheet(f"color: {config.text_primary}; font-size: 18px; font-weight: 600;")
        layout.addWidget(header)
        
        # Instructions
        instructions = QLabel("Connect an Android device via USB or Wireless Debugging")
        instructions.setStyleSheet(f"color: {config.text_secondary}; font-size: 13px;")
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # Device list section
        list_header = QLabel("AVAILABLE DEVICES")
        list_header.setStyleSheet(f"color: {config.text_secondary}; font-size: 11px; margin-top: 10px;")
        layout.addWidget(list_header)
        
        self.device_list = QListWidget()
        self.device_list.setMinimumHeight(300)
        self.device_list.setStyleSheet(f"""
            QListWidget {{
                background-color: {config.background_secondary};
                border: 1px solid {config.border_color};
                border-radius: 8px;
                padding: 8px;
            }}
            QListWidget::item {{
                background-color: transparent;
                border-radius: 6px;
                margin: 2px;
                padding: 4px;
            }}
            QListWidget::item:selected {{
                background-color: {config.background_tertiary};
                border: 1px solid {config.accent_blush_red};
            }}
            QListWidget::item:hover {{
                background-color: {config.background_tertiary};
            }}
        """)
        layout.addWidget(self.device_list)
        
        # Empty state message
        self.empty_label = QLabel("No devices detected\n\nMake sure:\n• ADB is running\n• USB debugging is enabled\n• Device is authorized")
        self.empty_label.setStyleSheet(f"color: {config.text_secondary}; font-size: 13px;")
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.empty_label.setWordWrap(True)
        self.empty_label.hide()
        layout.addWidget(self.empty_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.setMinimumWidth(120)
        
        self.connect_btn = QPushButton("Connect")
        self.connect_btn.setMinimumWidth(120)
        self.connect_btn.setEnabled(False)
        
        button_layout.addWidget(self.refresh_btn)
        button_layout.addWidget(self.connect_btn)
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        # Connect signals
        self.device_list.itemSelectionChanged.connect(self._on_selection_changed)
        self.connect_btn.clicked.connect(self._on_connect_clicked)
    
    def set_devices(self, devices: list[dict]):
        """Update device list."""
        self.device_list.clear()
        
        if not devices:
            self.device_list.hide()
            self.empty_label.show()
        else:
            self.device_list.show()
            self.empty_label.hide()
            
            for device_info in devices:
                item = QListWidgetItem(self.device_list)
                widget = DeviceItem(
                    device_info["serial"],
                    device_info["state"],
                    device_info["connection_type"]
                )
                item.setSizeHint(widget.sizeHint())
                self.device_list.addItem(item)
                self.device_list.setItemWidget(item, widget)
    
    def _on_selection_changed(self):
        """Handle device selection change."""
        self.connect_btn.setEnabled(len(self.device_list.selectedItems()) > 0)
    
    def _on_connect_clicked(self):
        """Handle connect button click."""
        selected = self.device_list.selectedItems()
        if selected:
            item = selected[0]
            widget = self.device_list.itemWidget(item)
            self.device_selected.emit(widget.serial)
