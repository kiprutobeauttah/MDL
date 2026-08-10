"""ADB client abstraction."""

from enum import Enum
from typing import Optional
import adbutils
from adbutils import AdbDevice


class DeviceState(Enum):
    """Device connection states."""
    NO_DEVICE = "no_device"
    DETECTING = "detecting"
    DEVICE_FOUND = "device_found"
    UNAUTHORIZED = "unauthorized"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    MONITORING = "monitoring"
    DISCONNECTING = "disconnecting"
    ERROR = "error"


class ConnectionType(Enum):
    """Connection type."""
    USB = "usb"
    WIRELESS = "wireless"


class ADBClient:
    """ADB client wrapper."""
    
    def __init__(self):
        self._adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
        self._device: Optional[AdbDevice] = None
        self._state = DeviceState.NO_DEVICE
    
    @property
    def state(self) -> DeviceState:
        """Current device state."""
        return self._state
    
    @property
    def device(self) -> Optional[AdbDevice]:
        """Connected device."""
        return self._device
    
    def detect_devices(self) -> list[dict]:
        """Detect available devices.
        
        Returns:
            List of device info dicts with serial, state, connection_type
        """
        try:
            devices = []
            # list() returns AdbDeviceInfo objects with serial and state attributes
            device_list = self._adb.list()
            
            for device_info in device_list:
                connection_type = (
                    ConnectionType.WIRELESS 
                    if ":" in device_info.serial 
                    else ConnectionType.USB
                )
                
                devices.append({
                    "serial": device_info.serial,
                    "state": device_info.state,
                    "connection_type": connection_type,
                })
            
            return devices
        except Exception as e:
            print(f"Error detecting devices: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def connect(self, serial: str) -> bool:
        """Connect to device by serial.
        
        Args:
            serial: Device serial number
            
        Returns:
            True if connected successfully
        """
        try:
            self._state = DeviceState.CONNECTING
            self._device = self._adb.device(serial=serial)
            
            # Verify connection
            if self._device.serial:
                self._state = DeviceState.CONNECTED
                return True
            else:
                self._state = DeviceState.ERROR
                return False
                
        except Exception as e:
            print(f"Connection error: {e}")
            self._state = DeviceState.ERROR
            return False
    
    def disconnect(self):
        """Disconnect from device."""
        self._state = DeviceState.DISCONNECTING
        self._device = None
        self._state = DeviceState.NO_DEVICE
    
    def execute(self, command: str) -> str:
        """Execute shell command on device.
        
        Args:
            command: Shell command
            
        Returns:
            Command output
        """
        if not self._device:
            raise RuntimeError("No device connected")
        
        try:
            return self._device.shell(command).strip()
        except Exception as e:
            raise RuntimeError(f"Command execution failed: {e}")
    
    def get_property(self, prop: str) -> str:
        """Get device property.
        
        Args:
            prop: Property name (e.g., 'ro.product.model')
            
        Returns:
            Property value
        """
        return self.execute(f"getprop {prop}")
