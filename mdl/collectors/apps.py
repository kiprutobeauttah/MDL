"""Applications collector."""

from mdl.collectors.base import BaseCollector
from mdl.core.events import EventCategory


class AppsCollector(BaseCollector):
    """Collects installed applications."""
    
    def __init__(self, adb_client):
        super().__init__(adb_client, EventCategory.APPLICATION)
    
    def collect(self) -> list[dict]:
        """Collect installed applications."""
        if not self.adb.device:
            return []
        
        try:
            # Get list of packages
            output = self.adb.execute("pm list packages")
            packages = []
            
            for line in output.split("\n"):
                if line.startswith("package:"):
                    package_name = line.replace("package:", "").strip()
                    if package_name:
                        # Get app label
                        label = self._get_app_label(package_name)
                        packages.append({
                            "package": package_name,
                            "label": label,
                        })
            
            # Sort by label
            packages.sort(key=lambda x: x["label"].lower())
            
            return packages
            
        except Exception as e:
            print(f"Apps collection error: {e}")
            return []
    
    def _get_app_label(self, package: str) -> str:
        """Get human-readable app label."""
        try:
            # Try to get application label
            output = self.adb.execute(f"pm dump {package} | grep -A1 'labelRes'")
            # This is a simplified approach - real implementation would parse properly
            # For now, return package name
            return package.split(".")[-1].title()
        except:
            return package.split(".")[-1].title()
