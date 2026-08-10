"""Monitoring service."""

from PySide6.QtCore import QObject, QTimer
from mdl.adb.client import ADBClient, DeviceState
from mdl.collectors.device import DeviceCollector
from mdl.collectors.battery import BatteryCollector
from mdl.collectors.performance import PerformanceCollector
from mdl.collectors.network import NetworkCollector
from mdl.collectors.wifi import WiFiCollector
from mdl.collectors.cellular import CellularCollector
from mdl.collectors.bluetooth import BluetoothCollector
from mdl.core.config import config


class MonitoringService(QObject):
    """Manages metric collection."""
    
    def __init__(self, adb_client: ADBClient):
        super().__init__()
        self.adb = adb_client
        
        # Collectors
        self.device_collector = DeviceCollector(adb_client)
        self.battery_collector = BatteryCollector(adb_client)
        self.performance_collector = PerformanceCollector(adb_client)
        self.network_collector = NetworkCollector(adb_client)
        self.wifi_collector = WiFiCollector(adb_client)
        self.cellular_collector = CellularCollector(adb_client)
        self.bluetooth_collector = BluetoothCollector(adb_client)
        
        # Timers
        self._battery_timer = QTimer()
        self._battery_timer.timeout.connect(self._collect_battery)
        
        self._performance_timer = QTimer()
        self._performance_timer.timeout.connect(self._collect_performance)
        
        self._network_timer = QTimer()
        self._network_timer.timeout.connect(self._collect_network)
        
        self._wifi_timer = QTimer()
        self._wifi_timer.timeout.connect(self._collect_wifi)
        
        self._cellular_timer = QTimer()
        self._cellular_timer.timeout.connect(self._collect_cellular)
        
        self._bluetooth_timer = QTimer()
        self._bluetooth_timer.timeout.connect(self._collect_bluetooth)
        
        self._monitoring = False
    
    def start_monitoring(self):
        """Start monitoring."""
        if self.adb.state != DeviceState.CONNECTED:
            print("Cannot start monitoring: device not connected")
            return
        
        self._monitoring = True
        
        # Collect device info once
        self.device_collector.collect()
        
        # Start periodic collection with integer intervals
        battery_interval = max(1000, int(1000 / config.freq_battery))  # Convert Hz to ms
        self._battery_timer.start(battery_interval)
        
        performance_interval = max(500, int(1000 / config.freq_performance))
        self._performance_timer.start(performance_interval)
        
        network_interval = max(500, int(1000 / config.freq_network))
        self._network_timer.start(network_interval)
        self._wifi_timer.start(network_interval)
        self._cellular_timer.start(network_interval)
        
        # Bluetooth less frequently (every 5 seconds)
        self._bluetooth_timer.start(5000)
        
        # Update ADB state
        self.adb._state = DeviceState.MONITORING
        
        print("Monitoring started")
    
    def stop_monitoring(self):
        """Stop monitoring."""
        self._monitoring = False
        self._battery_timer.stop()
        self._performance_timer.stop()
        self._network_timer.stop()
        self._wifi_timer.stop()
        self._cellular_timer.stop()
        self._bluetooth_timer.stop()
        
        if self.adb.state == DeviceState.MONITORING:
            self.adb._state = DeviceState.CONNECTED
        
        print("Monitoring stopped")
    
    def _collect_battery(self):
        """Battery collection callback."""
        if self._monitoring:
            self.battery_collector.collect()
    
    def _collect_performance(self):
        """Performance collection callback."""
        if self._monitoring:
            self.performance_collector.collect()
    
    def _collect_network(self):
        """Network collection callback."""
        if self._monitoring:
            self.network_collector.collect()
    
    def _collect_wifi(self):
        """Wi-Fi collection callback."""
        if self._monitoring:
            self.wifi_collector.collect()
    
    def _collect_cellular(self):
        """Cellular collection callback."""
        if self._monitoring:
            self.cellular_collector.collect()
    
    def _collect_bluetooth(self):
        """Bluetooth collection callback."""
        if self._monitoring:
            self.bluetooth_collector.collect()
    
    @property
    def is_monitoring(self) -> bool:
        """Whether monitoring is active."""
        return self._monitoring
