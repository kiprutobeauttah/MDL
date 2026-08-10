"""Device information collector."""

from mdl.collectors.base import BaseCollector
from mdl.core.events import EventCategory
from mdl.models.device import DeviceInfo


class DeviceCollector(BaseCollector):
    """Collects device information."""
    
    def __init__(self, adb_client):
        super().__init__(adb_client, EventCategory.DEVICE)
    
    def collect(self) -> DeviceInfo:
        """Collect device information."""
        if not self.adb.device:
            return None
        
        try:
            info = DeviceInfo(
                serial=self.adb.device.serial,
                manufacturer=self._get_prop("ro.product.manufacturer", "Unknown"),
                model=self._get_prop("ro.product.model", "Unknown"),
                product=self._get_prop("ro.product.name", "Unknown"),
                board=self._get_prop("ro.product.board", "Unknown"),
                
                android_version=self._get_prop("ro.build.version.release", "Unknown"),
                sdk_level=self._get_prop("ro.build.version.sdk", "Unknown"),
                build_number=self._get_prop("ro.build.display.id", "Unknown"),
                security_patch=self._get_prop("ro.build.version.security_patch", "Unknown"),
                
                cpu_arch=self._get_prop("ro.product.cpu.abi", "Unknown"),
                abi=self._get_prop("ro.product.cpu.abilist", "Unknown"),
                
                uptime=self._get_uptime(),
            )
            
            # Publish metrics
            self.publish("device", "manufacturer", info.manufacturer)
            self.publish("device", "model", info.model)
            self.publish("device", "android_version", info.android_version)
            self.publish("device", "sdk_level", info.sdk_level)
            self.publish("device", "serial", info.serial)
            self.publish("device", "build", info.build_number)
            self.publish("device", "security_patch", info.security_patch)
            self.publish("device", "cpu_arch", info.cpu_arch)
            self.publish("device", "uptime", info.uptime)
            
            return info
            
        except Exception as e:
            print(f"Device collection error: {e}")
            return None
    
    def _get_prop(self, prop: str, default: str = "Unknown") -> str:
        """Get device property safely."""
        try:
            value = self.adb.get_property(prop)
            return value if value else default
        except:
            return default
    
    def _get_uptime(self) -> str:
        """Get device uptime."""
        try:
            uptime_sec = float(self.adb.execute("cat /proc/uptime").split()[0])
            days = int(uptime_sec // 86400)
            hours = int((uptime_sec % 86400) // 3600)
            minutes = int((uptime_sec % 3600) // 60)
            
            if days > 0:
                return f"{days}d {hours}h {minutes}m"
            elif hours > 0:
                return f"{hours}h {minutes}m"
            else:
                return f"{minutes}m"
        except:
            return "Unknown"
