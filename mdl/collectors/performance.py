"""Performance collector."""

from mdl.collectors.base import BaseCollector
from mdl.core.events import EventCategory
from mdl.models.device import PerformanceInfo


class PerformanceCollector(BaseCollector):
    """Collects performance metrics."""
    
    def __init__(self, adb_client):
        super().__init__(adb_client, EventCategory.PERFORMANCE)
    
    def collect(self) -> PerformanceInfo:
        """Collect performance metrics."""
        if not self.adb.device:
            return None
        
        try:
            # Memory info
            meminfo = self._get_memory_info()
            
            # Storage info
            storage = self._get_storage_info()
            
            info = PerformanceInfo(
                cpu_usage=0.0,  # TODO: Implement CPU monitoring
                ram_used=meminfo["used"],
                ram_total=meminfo["total"],
                ram_available=meminfo["available"],
                storage_used=storage["used"],
                storage_total=storage["total"],
            )
            
            # Publish metrics
            self.publish("performance", "ram_used", info.ram_used)
            self.publish("performance", "ram_total", info.ram_total)
            self.publish("performance", "storage_used", info.storage_used)
            
            return info
            
        except Exception as e:
            print(f"Performance collection error: {e}")
            return None
    
    def _get_memory_info(self) -> dict:
        """Get memory information."""
        try:
            output = self.adb.execute("cat /proc/meminfo")
            data = {}
            
            for line in output.split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    key = key.strip()
                    # Parse kB value
                    value_kb = int(value.strip().split()[0])
                    data[key] = value_kb // 1024  # Convert to MB
            
            total = data.get("MemTotal", 0)
            available = data.get("MemAvailable", 0)
            used = total - available
            
            return {
                "total": total,
                "used": used,
                "available": available,
            }
        except:
            return {"total": 0, "used": 0, "available": 0}
    
    def _get_storage_info(self) -> dict:
        """Get storage information."""
        try:
            # df shows in 1K blocks by default
            output = self.adb.execute("df /data")
            lines = output.strip().split("\n")
            
            if len(lines) >= 2:
                parts = lines[1].split()
                if len(parts) >= 4:
                    total_kb = int(parts[1])
                    used_kb = int(parts[2])
                    
                    return {
                        "total": total_kb // 1024,  # Convert to MB
                        "used": used_kb // 1024,
                    }
            
            return {"total": 0, "used": 0}
        except:
            return {"total": 0, "used": 0}
