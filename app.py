"""MDL - Mobile Diagnostic Lab entry point."""

import sys
from PySide6.QtWidgets import QApplication
from mdl.core.application import MDLApplication


def main():
    """Launch MDL application."""
    app = QApplication(sys.argv)
    app.setApplicationName("MDL")
    app.setOrganizationName("Beauttah K.")
    
    mdl = MDLApplication()
    mdl.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
