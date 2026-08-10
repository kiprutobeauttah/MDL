"""Application configuration."""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class MDLConfig:
    """MDL configuration."""
    
    # Application
    app_name: str = "MDL"
    version: str = "0.1.0"
    
    # Paths
    data_dir: Path = Path.home() / ".mdl"
    db_path: Path = data_dir / "mdl.db"
    
    # Theme colors - Light theme
    background_primary: str = "#FFFFFF"
    background_secondary: str = "#F5F7FA"
    background_tertiary: str = "#E8ECF1"
    accent_blush_red: str = "#C75B6F"
    accent_blush_red_hover: str = "#B34D60"
    accent_blush_red_pressed: str = "#9F4354"
    accent_green: str = "#2E7D32"
    accent_yellow: str = "#F57C00"
    accent_red: str = "#D32F2F"
    text_primary: str = "#1A1A1A"
    text_secondary: str = "#64748B"
    border_color: str = "#DFE3E8"
    
    # Collection frequencies (Hz)
    freq_device_info: float = 0.0  # On connection only
    freq_battery: float = 0.2  # Every 5 seconds
    freq_performance: float = 1.0
    freq_network: float = 1.0
    
    def __post_init__(self):
        """Ensure data directory exists."""
        self.data_dir.mkdir(parents=True, exist_ok=True)


config = MDLConfig()
