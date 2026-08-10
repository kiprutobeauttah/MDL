"""Base collector."""

from abc import ABC, abstractmethod
from datetime import datetime
from mdl.adb.client import ADBClient
from mdl.core.events import MetricEvent, EventCategory, EventSeverity, metric_bus


class BaseCollector(ABC):
    """Base metric collector."""
    
    def __init__(self, adb_client: ADBClient, category: EventCategory):
        self.adb = adb_client
        self.category = category
        self._enabled = True
    
    @abstractmethod
    def collect(self):
        """Collect metrics. Override in subclass."""
        pass
    
    def publish(self, source: str, metric: str, value, severity=EventSeverity.NORMAL):
        """Publish metric to event bus."""
        event = MetricEvent(
            timestamp=datetime.now(),
            category=self.category,
            source=source,
            metric=metric,
            value=value,
            severity=severity,
        )
        metric_bus.publish(event)
    
    @property
    def enabled(self) -> bool:
        """Whether collector is enabled."""
        return self._enabled
    
    def enable(self):
        """Enable collector."""
        self._enabled = True
    
    def disable(self):
        """Disable collector."""
        self._enabled = False
