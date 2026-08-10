"""Device information models."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class DeviceInfo:
    """Device information."""
    serial: str
    manufacturer: str = "Unknown"
    model: str = "Unknown"
    product: str = "Unknown"
    board: str = "Unknown"
    
    android_version: str = "Unknown"
    sdk_level: str = "Unknown"
    build_number: str = "Unknown"
    security_patch: str = "Unknown"
    
    cpu_arch: str = "Unknown"
    abi: str = "Unknown"
    
    ram_total: Optional[int] = None  # MB
    storage_total: Optional[int] = None  # MB
    
    display_resolution: str = "Unknown"
    display_density: str = "Unknown"
    
    uptime: str = "Unknown"


@dataclass
class BatteryInfo:
    """Battery information."""
    level: int  # Percentage
    temperature: float  # Celsius
    voltage: float  # Volts
    status: str  # Charging, Discharging, etc.
    health: str
    technology: str
    plugged: str  # USB, AC, Wireless, None


@dataclass
class PerformanceInfo:
    """Performance metrics."""
    cpu_usage: float  # Percentage
    ram_used: int  # MB
    ram_total: int  # MB
    ram_available: int  # MB
    storage_used: int  # MB
    storage_total: int  # MB
