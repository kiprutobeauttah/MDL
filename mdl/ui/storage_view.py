"""Storage monitoring view."""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Qt
from mdl.core.events import EventCategory, MetricEvent, metric_bus
from mdl.core.config import config


class StorageCard(QWidget):
    """Storage partition card."""
    
    def __init__(self, name: str):
        super().__init__()
        self.partition_name = name
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(12)
        
        # Title
        title = QLabel(name)
        title.setStyleSheet(f"color: {config.text_secondary}; font-size: 11px; font-weight: 600;")
        
        # Usage
        usage_layout = QHBoxLayout()
        
        self.used_label = QLabel("-- GB")
        self.used_label.setStyleSheet(f"color: {config.text_primary}; font-size: 24px; font-weight: 700;")
        
        of_label = QLabel("of")
        of_label.setStyleSheet(f"color: {config.text_secondary}; font-size: 14px;")
        
        self.total_label = QLabel("-- GB")
        self.total_label.setStyleSheet(f"color: {config.text_secondary}; font-size: 16px;")
        
        usage_layout.addWidget(self.used_label)
        usage_layout.addWidget(of_label)
        usage_layout.addWidget(self.total_label)
        usage_layout.addStretch()
        
        # Progress bar
        self.progress = QProgressBar()
        self.progress.setMaximum(100)
        self.progress.setValue(0)
        self.progress.setTextVisible(True)
        self.progress.setFixedHeight(24)
        self.progress.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                border-radius: 6px;
                background-color: {config.background_tertiary};
                text-align: center;
                color: {config.text_primary};
                font-weight: 600;
            }}
            QProgressBar::chunk {{
                background-color: {config.accent_blush_red};
                border-radius: 6px;
            }}
        """)
        
        layout.addWidget(title)
        layout.addLayout(usage_layout)
        layout.addWidget(self.progress)
        
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {config.background_secondary};
                border: 1px solid {config.border_color};
                border-radius: 10px;
            }}
        """)
        self.setMinimumHeight(140)
    
    def update_storage(self, used_mb: int, total_mb: int):
        """Update storage info."""
        used_gb = used_mb / 1024
        total_gb = total_mb / 1024
        
        self.used_label.setText(f"{used_gb:.1f} GB")
        self.total_label.setText(f"{total_gb:.1f} GB")
        
        if total_mb > 0:
            percent = int((used_mb / total_mb) * 100)
            self.progress.setValue(percent)


class StorageView(QWidget):
    """Storage monitoring view."""
    
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
        header = QLabel("STORAGE")
        header.setStyleSheet(f"color: {config.text_primary}; font-size: 20px; font-weight: 700;")
        layout.addWidget(header)
        
        # Internal storage card
        self.internal_card = StorageCard("INTERNAL STORAGE")
        layout.addWidget(self.internal_card)
        
        # Info note
        info = QLabel("Storage information is collected from the device's file system")
        info.setStyleSheet(f"color: {config.text_secondary}; font-size: 12px;")
        info.setWordWrap(True)
        layout.addWidget(info)
        
        layout.addStretch()
    
    def _subscribe(self):
        """Subscribe to storage metrics."""
        metric_bus.subscribe(EventCategory.PERFORMANCE, self._on_storage_metric)
    
    def _on_storage_metric(self, event: MetricEvent):
        """Handle storage metric."""
        if event.metric == "storage_used":
            used = event.value
            if hasattr(self, '_storage_total'):
                self.internal_card.update_storage(used, self._storage_total)
        elif event.metric == "storage_total":
            self._storage_total = event.value
            if hasattr(self, '_storage_used'):
                self.internal_card.update_storage(self._storage_used, event.value)
