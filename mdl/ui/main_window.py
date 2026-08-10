"""Main application window."""

from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QStackedWidget
from PySide6.QtCore import Qt
from mdl.adb.client import ADBClient, DeviceState
from mdl.services.monitoring import MonitoringService
from mdl.ui.connection import ConnectionPanel
from mdl.ui.dashboard import Dashboard
from mdl.ui.sidebar import Sidebar
from mdl.ui.placeholder import PlaceholderView
from mdl.ui.battery_view import BatteryView
from mdl.ui.apps_view import AppsView
from mdl.ui.network_view import NetworkView
from mdl.ui.wifi_view import WiFiView
from mdl.ui.cellular_view import CellularView
from mdl.ui.bluetooth_view import BluetoothView
from mdl.ui.sensors_view import SensorsView
from mdl.ui.performance_view import PerformanceView
from mdl.ui.storage_view import StorageView
from mdl.ui.settings_view import SettingsView
from mdl.ui.sessions_view import SessionsView
from mdl.ui.events_view import EventsView
from mdl.ui.alerts_view import AlertsView
from mdl.ui.theme import get_stylesheet
from mdl.core.config import config


class StatusBar(QWidget):
    """Status bar showing connection state."""
    
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 8, 16, 8)
        
        self.status_indicator = QLabel("●")
        self.status_label = QLabel("No device")
        
        self.status_indicator.setStyleSheet(f"color: {config.text_secondary}; font-size: 12px;")
        self.status_label.setStyleSheet(f"color: {config.text_secondary}; font-size: 12px;")
        
        layout.addWidget(self.status_indicator)
        layout.addWidget(self.status_label)
        layout.addStretch()
        
        # Version info
        version_label = QLabel("v0.1.0 by Beauttah K.")
        version_label.setStyleSheet(f"color: {config.text_secondary}; font-size: 10px;")
        layout.addWidget(version_label)
        
        self.setStyleSheet(f"background-color: {config.background_secondary};")
        self.setMaximumHeight(32)
    
    def update_status(self, state: DeviceState, device_name: str = ""):
        """Update status display."""
        if state == DeviceState.CONNECTED or state == DeviceState.MONITORING:
            self.status_indicator.setStyleSheet(f"color: {config.accent_green}; font-size: 12px;")
            self.status_label.setText(f"{device_name} — Connected")
        elif state == DeviceState.CONNECTING:
            self.status_indicator.setStyleSheet(f"color: {config.accent_yellow}; font-size: 12px;")
            self.status_label.setText("Connecting...")
        elif state == DeviceState.ERROR:
            self.status_indicator.setStyleSheet(f"color: {config.accent_red}; font-size: 12px;")
            self.status_label.setText("Connection error")
        else:
            self.status_indicator.setStyleSheet(f"color: {config.text_secondary}; font-size: 12px;")
            self.status_label.setText("No device")


class MainWindow(QMainWindow):
    """MDL main window."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MDL — Mobile Diagnostic Lab")
        self.setMinimumSize(900, 700)
        self.resize(1000, 750)
        
        # Apply theme
        self.setStyleSheet(get_stylesheet())
        
        # Initialize services
        self.adb = ADBClient()
        self.monitoring = MonitoringService(self.adb)
        
        self._init_ui()
        self._show_connection_panel()
    
    def _init_ui(self):
        """Initialize UI."""
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Main content area
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = Sidebar()
        self.sidebar.hide()  # Hidden until connected
        
        # Connect sidebar navigation
        self.sidebar.nav_overview.connect(lambda: self.content_stack.setCurrentWidget(self.dashboard))
        self.sidebar.nav_network.connect(self._show_network)
        self.sidebar.nav_wifi.connect(self._show_wifi)
        self.sidebar.nav_cellular.connect(self._show_cellular)
        self.sidebar.nav_bluetooth.connect(self._show_bluetooth)
        self.sidebar.nav_apps.connect(self._show_apps)
        self.sidebar.nav_sensors.connect(self._show_sensors)
        self.sidebar.nav_battery.connect(self._show_battery)
        self.sidebar.nav_performance.connect(self._show_performance)
        self.sidebar.nav_storage.connect(self._show_storage)
        self.sidebar.nav_settings.connect(self._show_settings)
        self.sidebar.nav_sessions.connect(self._show_sessions)
        self.sidebar.nav_events.connect(self._show_events)
        self.sidebar.nav_alerts.connect(self._show_alerts)
        
        content_layout.addWidget(self.sidebar)
        
        # Stacked widget for main views
        self.stack = QStackedWidget()
        
        # Connection panel
        self.connection_panel = ConnectionPanel()
        self.connection_panel.refresh_btn.clicked.connect(self._refresh_devices)
        self.connection_panel.device_selected.connect(self._connect_device)
        self.stack.addWidget(self.connection_panel)
        
        # Content stack (for connected views)
        self.content_stack = QStackedWidget()
        
        # Dashboard
        self.dashboard = Dashboard()
        self.content_stack.addWidget(self.dashboard)
        
        # Battery view
        self.battery_view = BatteryView()
        self.content_stack.addWidget(self.battery_view)
        
        # Apps view
        self.apps_view = AppsView(self.adb)
        self.content_stack.addWidget(self.apps_view)
        
        # Network view
        self.network_view = NetworkView()
        self.content_stack.addWidget(self.network_view)
        
        # Wi-Fi view
        self.wifi_view = WiFiView()
        self.content_stack.addWidget(self.wifi_view)
        
        # Cellular view
        self.cellular_view = CellularView()
        self.content_stack.addWidget(self.cellular_view)
        
        # Bluetooth view
        self.bluetooth_view = BluetoothView()
        self.content_stack.addWidget(self.bluetooth_view)
        
        # Sensors view
        self.sensors_view = SensorsView()
        self.content_stack.addWidget(self.sensors_view)
        
        # Performance view
        self.performance_view = PerformanceView()
        self.content_stack.addWidget(self.performance_view)
        
        # Storage view
        self.storage_view = StorageView()
        self.content_stack.addWidget(self.storage_view)
        
        # Settings view
        self.settings_view = SettingsView()
        self.content_stack.addWidget(self.settings_view)
        
        # Sessions view
        self.sessions_view = SessionsView()
        self.content_stack.addWidget(self.sessions_view)
        
        # Events view
        self.events_view = EventsView()
        self.content_stack.addWidget(self.events_view)
        
        # Alerts view
        self.alerts_view = AlertsView()
        self.content_stack.addWidget(self.alerts_view)
        
        # Placeholder views
        self.placeholder = PlaceholderView("Feature")
        self.content_stack.addWidget(self.placeholder)
        
        self.stack.addWidget(self.content_stack)
        
        content_layout.addWidget(self.stack)
        
        layout.addLayout(content_layout)
        
        # Status bar
        self.status_bar = StatusBar()
        layout.addWidget(self.status_bar)
    
    def _show_connection_panel(self):
        """Show connection panel."""
        self.stack.setCurrentWidget(self.connection_panel)
        self._refresh_devices()
    
    def _show_dashboard(self):
        """Show dashboard with sidebar."""
        self.sidebar.show()
        self.stack.setCurrentWidget(self.content_stack)
        self.content_stack.setCurrentWidget(self.dashboard)
        self.sidebar.btn_overview.setChecked(True)
    
    def _show_placeholder(self, feature: str):
        """Show placeholder for unimplemented feature."""
        self.placeholder.set_feature(feature)
        self.content_stack.setCurrentWidget(self.placeholder)
    
    def _show_battery(self):
        """Show battery view."""
        self.content_stack.setCurrentWidget(self.battery_view)
    
    def _show_apps(self):
        """Show apps view."""
        self.content_stack.setCurrentWidget(self.apps_view)
    
    def _show_network(self):
        """Show network view."""
        self.content_stack.setCurrentWidget(self.network_view)
    
    def _show_wifi(self):
        """Show Wi-Fi view."""
        self.content_stack.setCurrentWidget(self.wifi_view)
    
    def _show_cellular(self):
        """Show cellular view."""
        self.content_stack.setCurrentWidget(self.cellular_view)
    
    def _show_bluetooth(self):
        """Show bluetooth view."""
        self.content_stack.setCurrentWidget(self.bluetooth_view)
    
    def _show_sensors(self):
        """Show sensors view."""
        self.content_stack.setCurrentWidget(self.sensors_view)
    
    def _show_performance(self):
        """Show performance view."""
        self.content_stack.setCurrentWidget(self.performance_view)
    
    def _show_storage(self):
        """Show storage view."""
        self.content_stack.setCurrentWidget(self.storage_view)
    
    def _show_settings(self):
        """Show settings view."""
        self.content_stack.setCurrentWidget(self.settings_view)
    
    def _show_sessions(self):
        """Show sessions view."""
        self.content_stack.setCurrentWidget(self.sessions_view)
    
    def _show_events(self):
        """Show events view."""
        self.content_stack.setCurrentWidget(self.events_view)
    
    def _show_alerts(self):
        """Show alerts view."""
        self.content_stack.setCurrentWidget(self.alerts_view)
    
    def _refresh_devices(self):
        """Refresh device list."""
        devices = self.adb.detect_devices()
        self.connection_panel.set_devices(devices)
        
        if not devices:
            print("No devices detected. Make sure:")
            print("  1. ADB is running (adb devices)")
            print("  2. USB debugging is enabled")
            print("  3. Device is authorized")
    
    def _connect_device(self, serial: str):
        """Connect to selected device."""
        print(f"Connecting to {serial}...")
        self.status_bar.update_status(DeviceState.CONNECTING)
        
        if self.adb.connect(serial):
            print(f"Connected to {serial}")
            device_model = self.adb.get_property("ro.product.model")
            self.status_bar.update_status(DeviceState.CONNECTED, device_model)
            
            # Start monitoring
            self.monitoring.start_monitoring()
            self.status_bar.update_status(DeviceState.MONITORING, device_model)
            
            # Show dashboard
            self._show_dashboard()
        else:
            print(f"Failed to connect to {serial}")
            self.status_bar.update_status(DeviceState.ERROR)
