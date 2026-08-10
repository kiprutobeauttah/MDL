"""Cellular network collector."""

from mdl.collectors.base import BaseCollector
from mdl.core.events import EventCategory


class CellularCollector(BaseCollector):
    """Collects cellular network information."""
    
    def __init__(self, adb_client):
        super().__init__(adb_client, EventCategory.NETWORK)
    
    def collect(self) -> dict:
        """Collect cellular metrics."""
        if not self.adb.device:
            return None
        
        try:
            # Get telephony info
            cellular_info = self._get_cellular_info()
            
            # Publish metrics
            self.publish("cellular", "network_type", cellular_info.get("network_type", "--"))
            self.publish("cellular", "operator", cellular_info.get("operator", "--"))
            self.publish("cellular", "mcc_mnc", cellular_info.get("mcc_mnc", "--"))
            self.publish("cellular", "state", cellular_info.get("state", "--"))
            self.publish("cellular", "data_state", cellular_info.get("data_state", "--"))
            self.publish("cellular", "roaming", cellular_info.get("roaming", "No"))
            
            # Signal metrics
            self.publish("cellular", "rsrp", cellular_info.get("rsrp", 0))
            self.publish("cellular", "rsrq", cellular_info.get("rsrq", 0))
            self.publish("cellular", "rssi", cellular_info.get("rssi", 0))
            self.publish("cellular", "sinr", cellular_info.get("sinr", 0))
            
            # Cell info
            self.publish("cellular", "cell_id", cellular_info.get("cell_id", "--"))
            self.publish("cellular", "tac", cellular_info.get("tac", "--"))
            self.publish("cellular", "pci", cellular_info.get("pci", "--"))
            self.publish("cellular", "band", cellular_info.get("band", "--"))
            
            return cellular_info
            
        except Exception as e:
            print(f"Cellular collection error: {e}")
            return None
    
    def _get_cellular_info(self) -> dict:
        """Get cellular network info."""
        try:
            output = self.adb.execute("dumpsys telephony.registry")
            
            info = {
                "network_type": "--",
                "operator": "--",
                "mcc_mnc": "--",
                "state": "--",
                "data_state": "--",
                "roaming": "No",
                "rsrp": 0,
                "rsrq": 0,
                "rssi": 0,
                "sinr": 0,
                "cell_id": "--",
                "tac": "--",
                "pci": "--",
                "band": "--",
            }
            
            lines = output.split("\n")
            
            for line in lines:
                line = line.strip()
                
                # Network type
                if "mDataConnectionNetworkType" in line or "VoiceNetworkType" in line:
                    if "LTE" in line or "13" in line:
                        info["network_type"] = "LTE"
                    elif "NR" in line or "20" in line:
                        info["network_type"] = "5G"
                    elif "UMTS" in line or "3" in line:
                        info["network_type"] = "3G"
                    elif "EDGE" in line or "2" in line:
                        info["network_type"] = "2G"
                
                # Operator
                elif "mServiceState" in line and "mOperatorAlphaLong" in line:
                    parts = line.split("mOperatorAlphaLong=")
                    if len(parts) > 1:
                        operator = parts[1].split(",")[0].strip()
                        if operator:
                            info["operator"] = operator
                
                # MCC/MNC
                elif "mccMnc" in line:
                    mcc_mnc = line.split("=")[-1].strip()
                    if mcc_mnc:
                        info["mcc_mnc"] = mcc_mnc
                
                # Service state
                elif "mVoiceRegState" in line:
                    state = line.split("=")[-1].strip().split()[0]
                    if state == "0":
                        info["state"] = "In service"
                    elif state == "1":
                        info["state"] = "Out of service"
                    elif state == "2":
                        info["state"] = "Emergency only"
                    else:
                        info["state"] = "Unknown"
                
                # Data state
                elif "mDataConnectionState" in line:
                    data_state = line.split("=")[-1].strip().split()[0]
                    if data_state == "0":
                        info["data_state"] = "Disconnected"
                    elif data_state == "1":
                        info["data_state"] = "Connecting"
                    elif data_state == "2":
                        info["data_state"] = "Connected"
                    else:
                        info["data_state"] = "Suspended"
                
                # Roaming
                elif "mIsDataRoaming" in line:
                    if "true" in line:
                        info["roaming"] = "Yes"
                
                # Signal strength
                elif "mSignalStrength" in line or "SignalStrength" in line:
                    # Try to parse signal values
                    if "rsrp=" in line or "RSRP:" in line:
                        try:
                            rsrp_str = line.split("rsrp=")[-1].split()[0].replace("RSRP:", "").strip()
                            info["rsrp"] = int(rsrp_str)
                        except:
                            pass
                    
                    if "rsrq=" in line or "RSRQ:" in line:
                        try:
                            rsrq_str = line.split("rsrq=")[-1].split()[0].replace("RSRQ:", "").strip()
                            info["rsrq"] = int(rsrq_str)
                        except:
                            pass
                    
                    if "rssi=" in line or "RSSI:" in line:
                        try:
                            rssi_str = line.split("rssi=")[-1].split()[0].replace("RSSI:", "").strip()
                            info["rssi"] = int(rssi_str)
                        except:
                            pass
            
            return info
            
        except Exception as e:
            print(f"Cellular info error: {e}")
            return info
