"""Bluetooth collector."""

from mdl.collectors.base import BaseCollector
from mdl.core.events import EventCategory


class BluetoothCollector(BaseCollector):
    """Collects Bluetooth information."""
    
    def __init__(self, adb_client):
        super().__init__(adb_client, EventCategory.NETWORK)
    
    def collect(self) -> dict:
        """Collect Bluetooth metrics."""
        if not self.adb.device:
            return None
        
        try:
            # Get Bluetooth state
            bt_info = self._get_bluetooth_info()
            
            # Publish metrics
            self.publish("bluetooth", "enabled", bt_info.get("enabled", False))
            self.publish("bluetooth", "adapter_address", bt_info.get("adapter_address", "--"))
            self.publish("bluetooth", "adapter_name", bt_info.get("adapter_name", "--"))
            self.publish("bluetooth", "adapter_state", bt_info.get("adapter_state", "--"))
            self.publish("bluetooth", "devices", bt_info.get("devices", []))
            
            return bt_info
            
        except Exception as e:
            print(f"Bluetooth collection error: {e}")
            return None
    
    def _get_bluetooth_info(self) -> dict:
        """Get Bluetooth adapter and device info."""
        try:
            output = self.adb.execute("dumpsys bluetooth_manager")
            
            info = {
                "enabled": False,
                "adapter_address": "--",
                "adapter_name": "--",
                "adapter_state": "OFF",
                "devices": [],
            }
            
            lines = output.split("\n")
            
            for line in lines:
                line = line.strip()
                
                # Bluetooth state
                if "enabled:" in line.lower() or "state:" in line.lower():
                    if "true" in line.lower() or "on" in line.lower() or "12" in line:
                        info["enabled"] = True
                        info["adapter_state"] = "ON"
                
                # Adapter address
                elif "address:" in line.lower() and ":" in line:
                    parts = line.split(":")
                    if len(parts) >= 2:
                        # Check if it looks like a MAC address
                        addr_part = ":".join(parts[1:]).strip()
                        if len(addr_part) == 17:  # MAC address length
                            info["adapter_address"] = addr_part
                
                # Adapter name
                elif "name:" in line.lower() and "adapter" not in line.lower():
                    name = line.split(":")[-1].strip()
                    if name and len(name) < 50:
                        info["adapter_name"] = name
            
            # Get bonded devices
            try:
                devices_output = self.adb.execute("dumpsys bluetooth_manager | grep -A 5 'Bonded devices'")
                devices = self._parse_bonded_devices(devices_output)
                info["devices"] = devices
            except:
                pass
            
            return info
            
        except Exception as e:
            print(f"Bluetooth info error: {e}")
            return info
    
    def _parse_bonded_devices(self, output: str) -> list:
        """Parse bonded Bluetooth devices."""
        devices = []
        
        lines = output.split("\n")
        current_device = {}
        
        for line in lines:
            line = line.strip()
            
            # Device address pattern
            if ":" in line and len(line.split(":")) >= 6:
                if current_device:
                    devices.append(current_device)
                current_device = {
                    "address": line.split()[0] if " " in line else line,
                    "name": "Unknown Device",
                    "paired": True,
                    "connected": False,
                }
            
            # Device name
            elif "name:" in line.lower() and current_device:
                name = line.split(":")[-1].strip()
                if name:
                    current_device["name"] = name
            
            # Connection state
            elif "connected" in line.lower() and current_device:
                if "true" in line.lower():
                    current_device["connected"] = True
        
        if current_device:
            devices.append(current_device)
        
        return devices
