"""Wi-Fi monitoring view."""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QProgressBar
from PySide6.QtCore import Qt
import pyqtgraph as pg
from collections import deque
from mdl.core.events import EventCategory, MetricEvent, metric_bus
from mdl.core.config import config


class WiFiMetricCard(QWidget):
    """Wi-Fi metric card."""
    
    def __init__(self, title: str, unit: str = ""):
        super().__init__()
        self.unit = unit
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(6)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"color: {config.text_secondary}; font-size: 11px; font-weight: 600;")
        
        self.value_label = QLabel("--")
        self.value_label.setStyleSheet(f"color: {config.text_primary}; font-size: 28px; font-weight: 700;")
        
        layout.addWidget(title_label)
        layout.addWidget(self.value_label)
        layout.addStretch()
        
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {config.background_secondary};
                border: 1px solid {config.border_color};
                border-radius: 10px;
            }}
        """)
        self.setMinimumHeight(100)
    
    def update_value(self, value):
        """Update value."""
        if isinstance(value, float):
            self.value_label.setText(f"{value:.1f}{self.unit}")
        elif isinstance(value, int):
            self.value_label.setText(f"{value}{self.unit}")
        else:
            self.value_label.setText(str(value))


class WiFiView(QWidget):
    """Wi-Fi monitoring view."""
    
    def __init__(self):
        super().__init__()
        
        # Signal history
        self.max_points = 60
        self.rssi_data = deque(maxlen=self.max_points)
        self.link_speed_data = deque(maxlen=self.max_points)
        self.time_data = deque(maxlen=self.max_points)
        self.time_counter = 0
        
        self._init_ui()
        self._subscribe()
    
    def _init_ui(self):
        """Initialize UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(24)
        
        # Header
        header_layout = QHBoxLayout()
        
        header = QLabel("WI-FI")
        header.setStyleSheet(f"color: {config.text_primary}; font-size: 20px; font-weight: 700;")
        
        self.status_label = QLabel("● Disconnected")
        self.status_label.setStyleSheet(f"color: {config.text_secondary}; font-size: 14px;")
        
        header_layout.addWidget(header)
        header_layout.addStretch()
        header_layout.addWidget(self.status_label)
        
        layout.addLayout(header_layout)
        
        # Connection info
        conn_container = QWidget()
        conn_container.setStyleSheet(f"""
            QWidget {{
                background-color: {config.background_secondary};
                border: 1px solid {config.border_color};
                border-radius: 10px;
            }}
        """)
        conn_layout = QVBoxLayout(conn_container)
        conn_layout.setContentsMargins(24, 20, 24, 20)
        conn_layout.setSpacing(12)
        
        conn_header = QLabel("CONNECTION")
        conn_header.setStyleSheet(f"color: {config.text_secondary}; font-size: 11px; font-weight: 600;")
        conn_layout.addWidget(conn_header)
        
        self.ssid_label = QLabel("--")
        self.ssid_label.setStyleSheet(f"color: {config.text_primary}; font-size: 20px; font-weight: 600;")
        conn_layout.addWidget(self.ssid_label)
        
        # Connection details grid
        details_grid = QGridLayout()
        details_grid.setSpacing(16)
        
        self.detail_labels = {}
        details = [
            ("BSSID", "bssid"),
            ("Frequency", "frequency"),
            ("Channel", "channel"),
            ("IP Address", "ip_address"),
        ]
        
        row = 0
        for label_text, key in details:
            label = QLabel(label_text)
            label.setStyleSheet(f"color: {config.text_secondary}; font-size: 11px; font-weight: 600;")
            
            value = QLabel("--")
            value.setStyleSheet(f"color: {config.text_primary}; font-size: 13px;")
            
            details_grid.addWidget(label, row, 0)
            details_grid.addWidget(value, row, 1)
            
            self.detail_labels[key] = value
            row += 1
        
        conn_layout.addLayout(details_grid)
        layout.addWidget(conn_container)
        
        # Metrics grid
        metrics_grid = QGridLayout()
        metrics_grid.setSpacing(16)
        
        self.rssi_card = WiFiMetricCard("RSSI", " dBm")
        self.link_speed_card = WiFiMetricCard("LINK SPEED", " Mbps")
        
        metrics_grid.addWidget(self.rssi_card, 0, 0)
        metrics_grid.addWidget(self.link_speed_card, 0, 1)
        
        layout.addLayout(metrics_grid)
        
        # Signal strength graph
        signal_container = self._create_graph_container("SIGNAL STRENGTH (dBm)")
        self.signal_plot = pg.PlotWidget()
        self._setup_plot(self.signal_plot)
        signal_container.layout().addWidget(self.signal_plot)
        layout.addWidget(signal_container)
        
        # Link speed graph
        speed_container = self._create_graph_container("LINK SPEED (Mbps)")
        self.speed_plot = pg.PlotWidget()
        self._setup_plot(self.speed_plot)
        speed_container.layout().addWidget(self.speed_plot)
        layout.addWidget(speed_container)
    
    def _create_graph_container(self, title: str) -> QWidget:
        """Create graph container."""
        container = QWidget()
        container.setStyleSheet(f"""
            QWidget {{
                background-color: {config.background_secondary};
                border: 1px solid {config.border_color};
                border-radius: 10px;
            }}
        """)
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(20, 16, 20, 16)
        container_layout.setSpacing(12)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"color: {config.text_secondary}; font-size: 11px; font-weight: 600;")
        container_layout.addWidget(title_label)
        
        container.setMinimumHeight(220)
        return container
    
    def _setup_plot(self, plot_widget: pg.PlotWidget):
        """Setup plot styling."""
        plot_widget.setBackground(config.background_secondary)
        plot_widget.showGrid(x=True, y=True, alpha=0.2)
        plot_widget.getAxis('bottom').setPen(pg.mkPen(color=config.text_secondary, width=1))
        plot_widget.getAxis('left').setPen(pg.mkPen(color=config.text_secondary, width=1))
        plot_widget.getAxis('bottom').setTextPen(pg.mkPen(color=config.text_secondary))
        plot_widget.getAxis('left').setTextPen(pg.mkPen(color=config.text_secondary))
        plot_widget.setMouseEnabled(x=False, y=False)
        plot_widget.setMenuEnabled(False)
    
    def _subscribe(self):
        """Subscribe to Wi-Fi metrics."""
        metric_bus.subscribe(EventCategory.NETWORK, self._on_wifi_metric)
    
    def _on_wifi_metric(self, event: MetricEvent):
        """Handle Wi-Fi metric."""
        if event.source != "wifi":
            return
        
        if event.metric == "connected":
            if event.value:
                self.status_label.setText("● Connected")
                self.status_label.setStyleSheet(f"color: {config.accent_green}; font-size: 14px;")
            else:
                self.status_label.setText("● Disconnected")
                self.status_label.setStyleSheet(f"color: {config.text_secondary}; font-size: 14px;")
        
        elif event.metric == "ssid":
            self.ssid_label.setText(event.value)
        
        elif event.metric == "rssi":
            self.rssi_card.update_value(event.value)
            self._update_signal_graph(event.value)
        
        elif event.metric == "link_speed":
            self.link_speed_card.update_value(event.value)
            self._update_speed_graph(event.value)
        
        elif event.metric in self.detail_labels:
            self.detail_labels[event.metric].setText(str(event.value))
    
    def _update_signal_graph(self, rssi: int):
        """Update signal strength graph."""
        self.time_counter += 1
        self.time_data.append(self.time_counter)
        self.rssi_data.append(rssi)
        
        if len(self.rssi_data) > 1:
            # Color based on signal strength
            if rssi >= -50:
                color = config.accent_green
            elif rssi >= -70:
                color = config.accent_yellow
            else:
                color = config.accent_red
            
            self.signal_plot.plot(
                list(self.time_data),
                list(self.rssi_data),
                pen=pg.mkPen(color=color, width=2),
                clear=True
            )
    
    def _update_speed_graph(self, speed: int):
        """Update link speed graph."""
        self.link_speed_data.append(speed)
        
        if len(self.link_speed_data) > 1:
            time_list = list(range(len(self.link_speed_data)))
            self.speed_plot.plot(
                time_list,
                list(self.link_speed_data),
                pen=pg.mkPen(color=config.accent_blush_red, width=2),
                clear=True
            )
