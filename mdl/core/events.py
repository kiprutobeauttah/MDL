"""Event bus for metric distribution."""

from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable
from PySide6.QtCore import QObject, Signal


class EventCategory(Enum):
    """Event categories."""
    DEVICE = "device"
    NETWORK = "network"
    BATTERY = "battery"
    PERFORMANCE = "performance"
    SENSOR = "sensor"
    APPLICATION = "application"
    SYSTEM = "system"


class EventSeverity(Enum):
    """Event severity levels."""
    NORMAL = "normal"
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass
class MetricEvent:
    """Metric event."""
    timestamp: datetime
    category: EventCategory
    source: str
    metric: str
    value: Any
    severity: EventSeverity = EventSeverity.NORMAL
    old_value: Any = None
    message: str = ""


class MetricBus(QObject):
    """Central metric event bus using Qt signals."""
    
    # Qt signals for thread-safe metric distribution
    device_metric = Signal(MetricEvent)
    network_metric = Signal(MetricEvent)
    battery_metric = Signal(MetricEvent)
    performance_metric = Signal(MetricEvent)
    sensor_metric = Signal(MetricEvent)
    application_metric = Signal(MetricEvent)
    system_metric = Signal(MetricEvent)
    
    def __init__(self):
        super().__init__()
        self._subscribers = {}
    
    def publish(self, event: MetricEvent):
        """Publish metric event to appropriate signal."""
        signal_map = {
            EventCategory.DEVICE: self.device_metric,
            EventCategory.NETWORK: self.network_metric,
            EventCategory.BATTERY: self.battery_metric,
            EventCategory.PERFORMANCE: self.performance_metric,
            EventCategory.SENSOR: self.sensor_metric,
            EventCategory.APPLICATION: self.application_metric,
            EventCategory.SYSTEM: self.system_metric,
        }
        
        signal = signal_map.get(event.category)
        if signal:
            signal.emit(event)
    
    def subscribe(self, category: EventCategory, callback: Callable[[MetricEvent], None]):
        """Subscribe to metric events."""
        signal_map = {
            EventCategory.DEVICE: self.device_metric,
            EventCategory.NETWORK: self.network_metric,
            EventCategory.BATTERY: self.battery_metric,
            EventCategory.PERFORMANCE: self.performance_metric,
            EventCategory.SENSOR: self.sensor_metric,
            EventCategory.APPLICATION: self.application_metric,
            EventCategory.SYSTEM: self.system_metric,
        }
        
        signal = signal_map.get(category)
        if signal:
            signal.connect(callback)


# Global metric bus instance
metric_bus = MetricBus()
