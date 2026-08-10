"""Applications view."""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QLineEdit, QPushButton
)
from PySide6.QtCore import Qt, QTimer
from mdl.core.config import config
from mdl.collectors.apps import AppsCollector


class AppItem(QWidget):
    """Application list item."""
    
    def __init__(self, package: str, label: str):
        super().__init__()
        self.package = package
        self.label = label
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        
        # App info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)
        
        label_widget = QLabel(label if label else package)
        label_widget.setStyleSheet(f"color: {config.text_primary}; font-weight: 500; font-size: 14px;")
        
        package_widget = QLabel(package)
        package_widget.setStyleSheet(f"color: {config.text_secondary}; font-size: 11px;")
        
        info_layout.addWidget(label_widget)
        info_layout.addWidget(package_widget)
        
        layout.addLayout(info_layout)
        layout.addStretch()
        
        self.setMinimumHeight(60)


class AppsView(QWidget):
    """Applications view."""
    
    def __init__(self, adb_client):
        super().__init__()
        self.adb = adb_client
        self.apps_collector = AppsCollector(adb_client)
        self.all_apps = []
        self._init_ui()
    
    def _init_ui(self):
        """Initialize UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        
        header = QLabel("APPLICATIONS")
        header.setStyleSheet(f"color: {config.text_primary}; font-size: 20px; font-weight: 700;")
        
        self.count_label = QLabel("0 apps")
        self.count_label.setStyleSheet(f"color: {config.text_secondary}; font-size: 14px;")
        
        header_layout.addWidget(header)
        header_layout.addStretch()
        header_layout.addWidget(self.count_label)
        
        layout.addLayout(header_layout)
        
        # Search bar
        search_layout = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search applications...")
        self.search_input.textChanged.connect(self._filter_apps)
        self.search_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {config.background_secondary};
                border: 1px solid {config.border_color};
                border-radius: 6px;
                padding: 10px 14px;
                color: {config.text_primary};
                font-size: 14px;
            }}
            QLineEdit:focus {{
                border-color: {config.accent_blush_red};
            }}
        """)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self._load_apps)
        
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(refresh_btn)
        
        layout.addLayout(search_layout)
        
        # Apps list
        self.apps_list = QListWidget()
        self.apps_list.setStyleSheet(f"""
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
        
        layout.addWidget(self.apps_list)
        
        # Load apps on next tick
        QTimer.singleShot(100, self._load_apps)
    
    def _load_apps(self):
        """Load applications."""
        self.apps_list.clear()
        self.all_apps = self.apps_collector.collect()
        
        if not self.all_apps:
            return
        
        self.count_label.setText(f"{len(self.all_apps)} apps")
        self._display_apps(self.all_apps)
    
    def _display_apps(self, apps: list):
        """Display apps in list."""
        self.apps_list.clear()
        
        for app in apps:
            item = QListWidgetItem(self.apps_list)
            widget = AppItem(app["package"], app["label"])
            item.setSizeHint(widget.sizeHint())
            self.apps_list.addItem(item)
            self.apps_list.setItemWidget(item, widget)
    
    def _filter_apps(self, text: str):
        """Filter apps by search text."""
        if not text:
            self._display_apps(self.all_apps)
            return
        
        text_lower = text.lower()
        filtered = [
            app for app in self.all_apps
            if text_lower in app["package"].lower() or text_lower in app["label"].lower()
        ]
        
        self._display_apps(filtered)
