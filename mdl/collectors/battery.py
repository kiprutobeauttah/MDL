"""Battery collector."""

from mdl.collectors.base import BaseCollector
from mdl.core.events import EventCategory, EventSeverity
from mdl.models.device import BatteryInfo


class BatteryCollector(BaseCollector):
    """Collects battery information."""
    
    def __init__(self, adb_client):
        super().__init__(adb_client, EventCategory.BATTERY)
        self._last_level = None
    
    def collect(self) -> BatteryInfo:
        """Collect battery metrics."""
        if not self.adb.device:
            return None
        
        try:
            # Get battery dump
            output = self.adb.execute("dumpsys battery")
            data = self._parse_battery_dump(output)
            
            level = int(data.get("level", 0))
            temp = int(data.get("temperature", 0)) / 10.0  # Decidegrees to Celsius
            voltage = int(data.get("voltage", 0)) / 1000.0  # mV to V
            
            info = BatteryInfo(
                level=level,
                temperature=temp,
                voltage=voltage,
                status=data.get("status", "Unknown"),
                health=data.get("health", "Unknown"),
                technology=data.get("technology", "Unknown"),
                plugged=data.get("plugged", "None"),
            )
            
            # Publish with severity based on thresholds
            temp_severity = EventSeverity.WARNING if temp > 40 else EventSeverity.NORMAL
            level_severity = EventSeverity.WARNING if level < 20 else EventSeverity.NORMAL
            
            self.publish("battery", "level", level, level_severity)
            self.publish("battery", "temperature", temp, temp_severity)
            self.publish("battery", "voltage", voltage)
            self.publish("battery", "status", info.status)
            self.publish("battery", "health", info.health)
            self.publish("battery", "technology", info.technology)
            self.publish("battery", "plugged", info.plugged)
            
            return info
            
        except Exception as e:
            print(f"Battery collection error: {e}")
            return None
    
    def _parse_battery_dump(self, output: str) -> dict:
        """Parse dumpsys battery output."""
        data = {}
        for line in output.split("\n"):
            line = line.strip()
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip().lower().replace(" ", "_")
                value = value.strip()
                
                # Map status codes
                if key == "status":
                    status_map = {
                        "1": "Unknown",
                        "2": "Charging",
                        "3": "Discharging",
                        "4": "Not charging",
                        "5": "Full",
                    }
                    value = status_map.get(value, value)
                
                # Map plugged codes
                if key == "plugged":
                    plugged_map = {
                        "0": "None",
                        "1": "AC",
                        "2": "USB",
                        "4": "Wireless",
                    }
                    value = plugged_map.get(value, value)
                
                data[key] = value
        
        return data
