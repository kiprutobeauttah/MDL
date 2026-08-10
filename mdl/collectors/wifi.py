"""Wi-Fi collector."""

from mdl.collectors.base import BaseCollector
from mdl.core.events import EventCategory


class WiFiCollector(BaseCollector):
    """Collects Wi-Fi information."""
    
    def __init__(self, adb_client):
        super().__init__(adb_client, EventCategory.NETWORK)
    
    def collect(self) -> dict:
        """Collect Wi-Fi metrics."""
        if not self.adb.device:
            return None
        
        try:
            # Get Wi-Fi status
            wifi_info = self._get_wifi_info()
            
            if wifi_info["connected"]:
                # Publish metrics
                self.publish("wifi", "connected", True)
                self.publish("wifi", "ssid", wifi_info.get("ssid", "--"))
                self.publish("wifi", "bssid", wifi_info.get("bssid", "--"))
                self.publish("wifi", "rssi", wifi_info.get("rssi", 0))
                self.publish("wifi", "link_speed", wifi_info.get("link_speed", 0))
                self.publish("wifi", "frequency", wifi_info.get("frequency", "--"))
                self.publish("wifi", "channel", wifi_info.get("channel", "--"))
                self.publish("wifi", "ip_address", wifi_info.get("ip_address", "--"))
            else:
                self.publish("wifi", "connected", False)
            
            return wifi_info
            
        except Exception as e:
            print(f"Wi-Fi collection error: {e}")
            return None
    
    def _get_wifi_info(self) -> dict:
        """Get Wi-Fi connection info."""
        try:
            output = self.adb.execute("dumpsys wifi | grep -A 20 'mWifiInfo'")
            
            info = {
                "connected": False,
                "ssid": "--",
                "bssid": "--",
                "rssi": 0,
                "link_speed": 0,
                "frequency": "--",
                "channel": "--",
                "ip_address": "--",
            }
            
            if not output:
                return info
            
            lines = output.split("\n")
            
            for line in lines:
                line = line.strip()
                
                if "SSID:" in line or "ssid:" in line:
                    ssid = line.split(":")[-1].strip().replace('"', '')
                    if ssid and ssid != "<unknown ssid>":
                        info["ssid"] = ssid
                        info["connected"] = True
                
                elif "BSSID:" in line or "bssid:" in line:
                    bssid = line.split(":")[-1].strip()
                    if bssid:
                        info["bssid"] = bssid
                
                elif "RSSI:" in line or "rssi:" in line:
                    try:
                        rssi_str = line.split(":")[-1].strip().split()[0]
                        info["rssi"] = int(rssi_str)
                    except:
                        pass
                
                elif "Link speed:" in line or "link_speed:" in line:
                    try:
                        speed_str = line.split(":")[-1].strip().replace("Mbps", "").strip()
                        info["link_speed"] = int(speed_str)
                    except:
                        pass
                
                elif "Frequency:" in line or "frequency:" in line:
                    freq = line.split(":")[-1].strip()
                    info["frequency"] = freq
                    
                    # Calculate channel from frequency
                    try:
                        freq_mhz = int(freq.replace("MHz", "").strip())
                        if 2400 <= freq_mhz <= 2500:
                            channel = (freq_mhz - 2407) // 5
                        elif 5000 <= freq_mhz <= 6000:
                            channel = (freq_mhz - 5000) // 5
                        else:
                            channel = 0
                        info["channel"] = str(channel)
                    except:
                        pass
            
            # Get IP address
            try:
                ip_output = self.adb.execute("ip addr show wlan0 | grep 'inet '")
                if ip_output:
                    parts = ip_output.strip().split()
                    if len(parts) >= 2:
                        info["ip_address"] = parts[1].split("/")[0]
            except:
                pass
            
            return info
            
        except Exception as e:
            print(f"Wi-Fi info error: {e}")
            return {"connected": False}
