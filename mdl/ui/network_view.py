"""Network diagnostics view with real-time graphs."""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import pyqtgraph as pg
from collections import deque
from mdl.core.events import EventCategory, MetricEvent, metric_bus
from mdl.core.config import config


class NetworkMetricCard(QWidget):
    """Network metric card."""
    
    def __init__(self, title: str, unit: str = ""):
        super().__init__()
        self.unit = unit
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(6)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet(f"color: {config.text_secondary}; font-size: 11px; font-weight: 600;")
        
        # Value
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


class HealthScoreCard(QWidget):
    """Network health score card."""
    
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(12)
        
        # Title
        title = QLabel("NETWORK HEALTH")
        title.setStyleSheet(f"color: {config.text_secondary}; font-size: 12px; font-weight: 600;")
        
        # Score
        self.score_label = QLabel("--")
        self.score_label.setStyleSheet(f"color: {config.text_primary}; font-size: 56px; font-weight: 700;")
        self.score_label.setAlignment(Qt.AlignCenter)
        
        # Status
        self.status_label = QLabel("Unknown")
        self.status_label.setStyleSheet(f"color: {config.text_secondary}; font-size: 14px;")
        self.status_label.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(title)
        layout.addWidget(self.score_label)
        layout.addWidget(self.status_label)
        layout.addStretch()
        
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {config.background_secondary};
                border: 1px solid {config.border_color};
                border-radius: 10px;
            }}
        """)
        self.setMinimumHeight(180)
    
    def update_score(self, score: int):
        """Update health score."""
        self.score_label.setText(f"{score}")
        
        # Update color and status
        if score >= 90:
            color = config.accent_green
            status = "Excellent"
        elif score >= 75:
            color = config.accent_green
            status = "Good"
        elif score >= 50:
            color = config.accent_yellow
            status = "Fair"
        elif score >= 25:
            color = config.accent_yellow
            status = "Poor"
        else:
            color = config.accent_red
            status = "Critical"
        
        self.score_label.setStyleSheet(f"color: {color}; font-size: 56px; font-weight: 700;")
        self.status_label.setText(status)


class NetworkView(QWidget):
    """Network diagnostics view."""
    
    def __init__(self):
        super().__init__()
        
        # Data buffers
        self.max_points = 60
        self.latency_data = deque(maxlen=self.max_points)
        self.rx_data = deque(maxlen=self.max_points)
        self.tx_data = deque(maxlen=self.max_points)
        self.packet_loss_data = deque(maxlen=self.max_points)
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
        header = QLabel("NETWORK DIAGNOSTICS")
        header.setStyleSheet(f"color: {config.text_primary}; font-size: 20px; font-weight: 700;")
        layout.addWidget(header)
        
        # Top row: Health score + metrics
        top_row = QHBoxLayout()
        top_row.setSpacing(16)
        
        self.health_card = HealthScoreCard()
        top_row.addWidget(self.health_card)
        
        # Metrics grid
        metrics_grid = QGridLayout()
        metrics_grid.setSpacing(16)
        
        self.latency_card = NetworkMetricCard("LATENCY", " ms")
        self.packet_loss_card = NetworkMetricCard("PACKET LOSS", "%")
        self.rx_rate_card = NetworkMetricCard("DOWNLOAD", " KB/s")
        self.tx_rate_card = NetworkMetricCard("UPLOAD", " KB/s")
        
        metrics_grid.addWidget(self.latency_card, 0, 0)
        metrics_grid.addWidget(self.packet_loss_card, 0, 1)
        metrics_grid.addWidget(self.rx_rate_card, 1, 0)
        metrics_grid.addWidget(self.tx_rate_card, 1, 1)
        
        top_row.addLayout(metrics_grid, stretch=2)
        layout.addLayout(top_row)
        
        # Latency graph
        latency_container = self._create_graph_container("LATENCY (ms)")
        self.latency_plot = pg.PlotWidget()
        self._setup_plot(self.latency_plot, "Latency", config.accent_blush_red)
        latency_container.layout().addWidget(self.latency_plot)
        layout.addWidget(latency_container)
        
        # Throughput graph
        throughput_container = self._create_graph_container("THROUGHPUT (KB/s)")
        self.throughput_plot = pg.PlotWidget()
        self._setup_plot(self.throughput_plot, "Throughput", config.accent_green)
        self.rx_curve = self.throughput_plot.plot(pen=pg.mkPen(color=config.accent_green, width=2), name="Download")
        self.tx_curve = self.throughput_plot.plot(pen=pg.mkPen(color=config.accent_blush_red, width=2), name="Upload")
        self.throughput_plot.addLegend()
        throughput_container.layout().addWidget(self.throughput_plot)
        layout.addWidget(throughput_container)
    
    def _create_graph_container(self, title: str) -> QWidget:
        """Create graph container widget."""
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
        
        container.setMinimumHeight(250)
        return container
    
    def _setup_plot(self, plot_widget: pg.PlotWidget, name: str, color: str):
        """Setup plot styling."""
        plot_widget.setBackground(config.background_secondary)
        plot_widget.showGrid(x=True, y=True, alpha=0.2)
        
        # Style axes
        plot_widget.getAxis('bottom').setPen(pg.mkPen(color=config.text_secondary, width=1))
        plot_widget.getAxis('left').setPen(pg.mkPen(color=config.text_secondary, width=1))
        plot_widget.getAxis('bottom').setTextPen(pg.mkPen(color=config.text_secondary))
        plot_widget.getAxis('left').setTextPen(pg.mkPen(color=config.text_secondary))
        
        # Remove padding
        plot_widget.setMouseEnabled(x=False, y=False)
        plot_widget.setMenuEnabled(False)
        
        return plot_widget
    
    def _subscribe(self):
        """Subscribe to network metrics."""
        metric_bus.subscribe(EventCategory.NETWORK, self._on_network_metric)
    
    def _on_network_metric(self, event: MetricEvent):
        """Handle network metric."""
        if event.metric == "health":
            self.health_card.update_score(event.value)
        elif event.metric == "latency":
            self.latency_card.update_value(event.value)
            self._update_latency_graph(event.value)
        elif event.metric == "packet_loss":
            self.packet_loss_card.update_value(event.value)
        elif event.metric == "rx_rate":
            self.rx_rate_card.update_value(event.value)
            self._update_throughput_graph(event.value, "rx")
        elif event.metric == "tx_rate":
            self.tx_rate_card.update_value(event.value)
            self._update_throughput_graph(event.value, "tx")
    
    def _update_latency_graph(self, value: float):
        """Update latency graph."""
        self.time_counter += 1
        self.time_data.append(self.time_counter)
        self.latency_data.append(value)
        
        if len(self.latency_data) > 1:
            self.latency_plot.plot(
                list(self.time_data),
                list(self.latency_data),
                pen=pg.mkPen(color=config.accent_blush_red, width=2),
                clear=True
            )
    
    def _update_throughput_graph(self, value: float, data_type: str):
        """Update throughput graph."""
        if data_type == "rx":
            self.rx_data.append(value)
        else:
            self.tx_data.append(value)
        
        if len(self.rx_data) > 1 and len(self.tx_data) > 1:
            time_list = list(range(len(self.rx_data)))
            
            # Update curves
            self.rx_curve.setData(time_list, list(self.rx_data))
            self.tx_curve.setData(time_list, list(self.tx_data))
