"""Dark theme stylesheet."""

from mdl.core.config import config


def get_stylesheet() -> str:
    """Get MDL light theme stylesheet."""
    return f"""
    QMainWindow {{
        background-color: {config.background_primary};
    }}
    
    QWidget {{
        background-color: {config.background_primary};
        color: {config.text_primary};
        font-family: 'Segoe UI', 'SF Pro', system-ui, sans-serif;
        font-size: 13px;
    }}
    
    QPushButton {{
        background-color: {config.accent_blush_red};
        border: none;
        border-radius: 6px;
        padding: 10px 20px;
        color: #FFFFFF;
        font-weight: 500;
        font-size: 13px;
    }}
    
    QPushButton:hover {{
        background-color: {config.accent_blush_red_hover};
    }}
    
    QPushButton:pressed {{
        background-color: {config.accent_blush_red_pressed};
    }}
    
    QPushButton:disabled {{
        background-color: {config.background_tertiary};
        color: {config.text_secondary};
    }}
    
    QLabel {{
        background-color: transparent;
        color: {config.text_primary};
    }}
    
    .card {{
        background-color: {config.background_secondary};
        border: 1px solid {config.border_color};
        border-radius: 12px;
        padding: 16px;
    }}
    
    .metric-label {{
        color: {config.text_secondary};
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
    }}
    
    .metric-value {{
        color: {config.text_primary};
        font-size: 24px;
        font-weight: 600;
    }}
    
    .status-connected {{
        color: {config.accent_green};
    }}
    
    .status-disconnected {{
        color: {config.text_secondary};
    }}
    
    QScrollArea {{
        border: none;
        background-color: {config.background_primary};
    }}
    
    QScrollBar:vertical {{
        background: {config.background_secondary};
        width: 10px;
        border-radius: 5px;
        border: none;
    }}
    
    QScrollBar::handle:vertical {{
        background: {config.background_tertiary};
        border-radius: 5px;
        min-height: 20px;
    }}
    
    QScrollBar::handle:vertical:hover {{
        background: {config.text_secondary};
    }}
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
    """
