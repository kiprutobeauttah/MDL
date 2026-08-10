"""Sessions view."""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QPushButton
)
from PySide6.QtCore import Qt
from mdl.core.config import config


class SessionItem(QWidget):
    """Session list item."""
    
    def __init__(self, session_id: int, start_time: str, duration: str):
        super().__init__()
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        
        # Session info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)
        
        title_label = QLabel(f"Session #{session_id}")
        title_label.setStyleSheet(f"color: {config.text_primary}; font-weight: 600; font-size: 14px;")
        
        time_label = QLabel(f"Started: {start_time}")
        time_label.setStyleSheet(f"color: {config.text_secondary}; font-size: 11px;")
        
        duration_label = QLabel(f"Duration: {duration}")
        duration_label.setStyleSheet(f"color: {config.text_secondary}; font-size: 11px;")
        
        info_layout.addWidget(title_label)
        info_layout.addWidget(time_label)
        info_layout.addWidget(duration_label)
        
        layout.addLayout(info_layout)
        layout.addStretch()
        
        self.setMinimumHeight(75)


class SessionsView(QWidget):
    """Sessions monitoring and replay view."""
    
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
        
        header = QLabel("SESSIONS")
        header.setStyleSheet(f"color: {config.text_primary}; font-size: 20px; font-weight: 700;")
        
        self.count_label = QLabel("0 sessions")
        self.count_label.setStyleSheet(f"color: {config.text_secondary}; font-size: 14px;")
        
        header_layout.addWidget(header)
        header_layout.addStretch()
        header_layout.addWidget(self.count_label)
        
        layout.addLayout(header_layout)
        
        # Info
        info = QLabel("Monitoring sessions record device metrics for later analysis and replay")
        info.setStyleSheet(f"color: {config.text_secondary}; font-size: 13px;")
        info.setWordWrap(True)
        layout.addWidget(info)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        new_session_btn = QPushButton("New Session")
        export_btn = QPushButton("Export")
        
        button_layout.addWidget(new_session_btn)
        button_layout.addWidget(export_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # Sessions list
        self.sessions_list = QListWidget()
        self.sessions_list.setStyleSheet(f"""
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
        
        layout.addWidget(self.sessions_list)
        
        # Add sample sessions
        self._add_sample_sessions()
    
    def _add_sample_sessions(self):
        """Add sample sessions."""
        samples = [
            (1, "2026-08-10 14:30", "1h 23m"),
            (2, "2026-08-09 10:15", "45m"),
            (3, "2026-08-08 16:00", "2h 10m"),
        ]
        
        self.count_label.setText(f"{len(samples)} sessions")
        
        for session_id, start, duration in samples:
            item = QListWidgetItem(self.sessions_list)
            widget = SessionItem(session_id, start, duration)
            item.setSizeHint(widget.sizeHint())
            self.sessions_list.addItem(item)
            self.sessions_list.setItemWidget(item, widget)
