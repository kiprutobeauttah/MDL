"""Network diagnostics collector."""

import time
import subprocess
from mdl.collectors.base import BaseCollector
from mdl.core.events import EventCategory, EventSeverity
from mdl.models.network import NetworkMetrics


class NetworkCollector(BaseCollector):
    """Collects network diagnostics."""
    
    def __init__(self, adb_client):
        super().__init__(adb_client, EventCategory.NETWORK)
        self._last_rx_bytes = 0
        self._last_tx_bytes = 0
        self._last_time = time.time()
    
    def collect(self) -> NetworkMetrics:
        """Collect network metrics."""
        if not self.adb.device:
            return None
        
        try:
            # Get connectivity info
            connectivity = self._get_connectivity()
            
            # Get network stats
            rx_bytes, tx_bytes = self._get_network_bytes()
            
            # Calculate throughput
            current_time = time.time()
            time_delta = current_time - self._last_time
            
            if time_delta > 0 and self._last_rx_bytes > 0:
                rx_rate = (rx_bytes - self._last_rx_bytes) / time_delta  # bytes/sec
                tx_rate = (tx_bytes - self._last_tx_bytes) / time_delta
            else:
                rx_rate = 0
                tx_rate = 0
            
            self._last_rx_bytes = rx_bytes
            self._last_tx_bytes = tx_bytes
            self._last_time = current_time
            
            # Ping test for latency
            latency, packet_loss = self._ping_test()
            
            metrics = NetworkMetrics(
                connected=connectivity["connected"],
                connection_type=connectivity["type"],
                latency=latency,
                packet_loss=packet_loss,
                rx_rate=rx_rate / 1024,  # Convert to KB/s
                tx_rate=tx_rate / 1024,
                rx_bytes=rx_bytes,
                tx_bytes=tx_bytes,
            )
            
            # Publish metrics
            self.publish("network", "connected", metrics.connected)
            self.publish("network", "type", metrics.connection_type)
            self.publish("network", "latency", metrics.latency)
            self.publish("network", "packet_loss", metrics.packet_loss)
            self.publish("network", "rx_rate", metrics.rx_rate)
            self.publish("network", "tx_rate", metrics.tx_rate)
            
            # Calculate health score
            health = self._calculate_health(metrics)
            self.publish("network", "health", health)
            
            return metrics
            
        except Exception as e:
            print(f"Network collection error: {e}")
            return None
    
    def _get_connectivity(self) -> dict:
        """Check network connectivity."""
        try:
            output = self.adb.execute("dumpsys connectivity | grep 'NetworkAgentInfo'")
            
            connected = "CONNECTED" in output
            
            # Determine connection type
            if "WIFI" in output.upper():
                conn_type = "Wi-Fi"
            elif "MOBILE" in output.upper() or "CELLULAR" in output.upper():
                conn_type = "Cellular"
            else:
                conn_type = "Unknown"
            
            return {
                "connected": connected,
                "type": conn_type,
            }
        except:
            return {"connected": False, "type": "None"}
    
    def _get_network_bytes(self) -> tuple[int, int]:
        """Get network RX/TX bytes."""
        try:
            # Get total network stats
            rx_output = self.adb.execute("cat /sys/class/net/wlan0/statistics/rx_bytes")
            tx_output = self.adb.execute("cat /sys/class/net/wlan0/statistics/tx_bytes")
            
            rx_bytes = int(rx_output.strip())
            tx_bytes = int(tx_output.strip())
            
            return rx_bytes, tx_bytes
        except:
            # Try alternative for cellular
            try:
                rx_output = self.adb.execute("cat /sys/class/net/rmnet0/statistics/rx_bytes")
                tx_output = self.adb.execute("cat /sys/class/net/rmnet0/statistics/tx_bytes")
                return int(rx_output.strip()), int(tx_output.strip())
            except:
                return 0, 0
    
    def _ping_test(self, count: int = 3) -> tuple[float, float]:
        """Ping test to measure latency and packet loss."""
        try:
            # Ping Google DNS
            output = self.adb.execute(f"ping -c {count} -W 1 8.8.8.8")
            
            # Parse output
            lines = output.split("\n")
            
            # Find packet loss line
            packet_loss = 0.0
            for line in lines:
                if "packet loss" in line:
                    parts = line.split("%")
                    if len(parts) > 0:
                        loss_part = parts[0].split()[-1]
                        try:
                            packet_loss = float(loss_part)
                        except:
                            pass
            
            # Find latency (avg)
            latency = 0.0
            for line in lines:
                if "rtt min/avg/max" in line or "round-trip" in line:
                    # Parse: rtt min/avg/max/mdev = 12.3/23.4/34.5/6.7 ms
                    parts = line.split("=")
                    if len(parts) > 1:
                        values = parts[1].strip().split("/")
                        if len(values) >= 2:
                            try:
                                latency = float(values[1])  # avg
                            except:
                                pass
            
            return latency, packet_loss
            
        except Exception as e:
            print(f"Ping test error: {e}")
            return 0.0, 0.0
    
    def _calculate_health(self, metrics: NetworkMetrics) -> int:
        """Calculate network health score (0-100)."""
        if not metrics.connected:
            return 0
        
        score = 100
        
        # Latency impact (0-40 points penalty)
        if metrics.latency > 100:
            score -= 40
        elif metrics.latency > 50:
            score -= 20
        elif metrics.latency > 30:
            score -= 10
        
        # Packet loss impact (0-40 points penalty)
        if metrics.packet_loss > 5:
            score -= 40
        elif metrics.packet_loss > 2:
            score -= 20
        elif metrics.packet_loss > 0.5:
            score -= 10
        
        # Connection type impact
        if metrics.connection_type == "Unknown":
            score -= 20
        
        return max(0, min(100, score))
