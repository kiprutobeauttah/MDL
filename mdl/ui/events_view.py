"""Events view."""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QLineEdit, QComboBox
)
from PySide6.QtCore import Qt, QTimer
from datetime import datetime
from mdl.core.events import EventCategory, EventSeverity, MetricEvent, metric_bus
from mdl.core.config import config


class EventItemWidget(QWidget):
    """Event list item widget."""
    
    def __init__(self, metric_event: MetricEvent):
        super().__init__()
        self.metric_event = metric_event
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 10, 16, 10)
        layout.setSpacing(12)
        
        # Severity indicator
        severity_color = {
            EventSeverity.NORMAL: config.text_secondary,
            EventSeverity.INFO: config.accent_green,
            EventSeverity.WARNING: config.accent_yellow,
            EventSeverity.CRITICAL: config.accent_red,
        }.get(metric_event.severity, config.text_secondary)
        
        indicator = QLabel("●")
        indicator.setFixedWidth(20)
        indicator.setStyleSheet(f"color: {severity_color}; font-size: 16px;")
        
        # Event info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)
        
        time_label = QLabel(metric_event.timestamp.strftime("%H:%M:%S"))
        time_label.setStyleSheet(f"color: {config.text_secondary}; font-size: 11px; font-family: monospace;")
        
        message = f"{metric_event.source}.{metric_event.metric} = {metric_event.value}"
        message_label = QLabel(message)
        message_label.setStyleSheet(f"color: {config.text_primary}; font-size: 13px;")
        
        category_label = QLabel(metric_event.category.value.upper())
        category_label.setStyleSheet(f"color: {config.text_secondary}; font-size: 10px; font-weight: 600;")
        
        info_layout.addWidget(time_label)
        info_layout.addWidget(message_label)
        info_layout.addWidget(category_label)
        
        layout.addWidget(indicator)
        layout.addLayout(info_layout)
        layout.addStretch()
        
        self.setMinimumHeight(70)


class EventsView(QWidget):
    """Real-time events view."""
    
    def __init__(self):
        super().__init__()
        self.all_events = []
        self.max_events = 100
        self._init_ui()
        self._subscribe()
    
    def _init_ui(self):
        """Initialize UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        
        header = QLabel("EVENTS")
        header.setStyleSheet(f"color: {config.text_primary}; font-size: 20px; font-weight: 700;")
        
        self.count_label = QLabel("0 events")
        self.count_label.setStyleSheet(f"color: {config.text_secondary}; font-size: 14px;")
        
        header_layout.addWidget(header)
        header_layout.addStretch()
        header_layout.addWidget(self.count_label)
        
        layout.addLayout(header_layout)
        
        # Filters
        filter_layout = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search events...")
        self.search_input.textChanged.connect(self._filter_events)
        self.search_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {config.background_secondary};
                border: 1px solid {config.border_color};
                border-radius: 6px;
                padding: 8px 12px;
                color: {config.text_primary};
            }}
        """)
        
        self.category_filter = QComboBox()
        self.category_filter.addItems(["All Categories", "Device", "Network", "Battery", "Performance", "Sensor"])
        self.category_filter.currentTextChanged.connect(self._filter_events)
        self.category_filter.setStyleSheet(f"""
            QComboBox {{
                background-color: {config.background_secondary};
                border: 1px solid {config.border_color};
                border-radius: 6px;
                padding: 8px 12px;
                color: {config.text_primary};
                min-width: 150px;
            }}
        """)
        
        filter_layout.addWidget(self.search_input)
        filter_layout.addWidget(self.category_filter)
        
        layout.addLayout(filter_layout)
        
        # Events list
        self.events_list = QListWidget()
        self.events_list.setStyleSheet(f"""
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
        """)
        
        layout.addWidget(self.events_list)
    
    def _subscribe(self):
        """Subscribe to all events."""
        for category in EventCategory:
            metric_bus.subscribe(category, self._on_event)
    
    def _on_event(self, event: MetricEvent):
        """Handle new event."""
        self.all_events.insert(0, event)  # Add to front
        
        # Keep only recent events
        if len(self.all_events) > self.max_events:
            self.all_events = self.all_events[:self.max_events]
        
        self._update_display()
    
    def _update_display(self):
        """Update events display."""
        self.count_label.setText(f"{len(self.all_events)} events")
        self._filter_events()
    
    def _filter_events(self):
        """Filter events by search and category."""
        self.events_list.clear()
        
        search_text = self.search_input.text().lower()
        category_filter = self.category_filter.currentText().lower()
        
        for event in self.all_events:
            # Category filter
            if category_filter != "all categories" and event.category.value != category_filter:
                continue
            
            # Search filter
            if search_text:
                search_fields = [
                    event.source.lower(),
                    event.metric.lower(),
                    str(event.value).lower(),
                ]
                if not any(search_text in field for field in search_fields):
                    continue
            
            # Add to list
            item = QListWidgetItem(self.events_list)
            widget = EventItemWidget(event)
            item.setSizeHint(widget.sizeHint())
            self.events_list.addItem(item)
            self.events_list.setItemWidget(item, widget)
