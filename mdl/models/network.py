"""Network models."""

from dataclasses import dataclass


@dataclass
class NetworkMetrics:
    """Network metrics."""
    connected: bool = False
    connection_type: str = "None"
    latency: float = 0.0  # ms
    packet_loss: float = 0.0  # percentage
    rx_rate: float = 0.0  # KB/s
    tx_rate: float = 0.0  # KB/s
    rx_bytes: int = 0
    tx_bytes: int = 0
