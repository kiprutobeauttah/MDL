"""Cellular network monitoring view."""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout
from PySide6.QtCore import Qt
import pyqtgraph as pg
from collections import deque
from mdl.core.events import EventCategory, MetricEvent, metric_bus
from mdl.core.config import config


class CellularMetricCard(QWidget):
    """Cellular metric card."""
    
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


class CellularView(QWidget):
    """Cellular network monitoring view."""
    
    def __init__(self):
        super().__init__()
        
        # Signal history
        self.max_points = 60
        self.rsrp_data = deque(maxlen=self.max_points)
        self.rsrq_data = deque(maxlen=self.max_points)
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
        
        header = QLabel("CELLULAR")
        header.setStyleSheet(f"color: {config.text_primary}; font-size: 20px; font-weight: 700;")
        
        self.network_type_label = QLabel("--")
        self.network_type_label.setStyleSheet(f"color: {config.accent_green}; font-size: 16px; font-weight: 600;")
        
        header_layout.addWidget(header)
        header_layout.addStretch()
        header_layout.addWidget(self.network_type_label)
        
        layout.addLayout(header_layout)
        
        # Operator info
        operator_container = QWidget()
        operator_container.setStyleSheet(f"""
            QWidget {{
                background-color: {config.background_secondary};
                border: 1px solid {config.border_color};
                border-radius: 10px;
            }}
        """)
        operator_layout = QVBoxLayout(operator_container)
        operator_layout.setContentsMargins(24, 20, 24, 20)
        operator_layout.setSpacing(12)
        
        operator_header = QLabel("NETWORK OPERATOR")
        operator_header.setStyleSheet(f"color: {config.text_secondary}; font-size: 11px; font-weight: 600;")
        operator_layout.addWidget(operator_header)
        
        self.operator_label = QLabel("--")
        self.operator_label.setStyleSheet(f"color: {config.text_primary}; font-size: 20px; font-weight: 600;")
        operator_layout.addWidget(self.operator_label)
        
        # Operator details
        details_grid = QGridLayout()
        details_grid.setSpacing(16)
        
        self.detail_labels = {}
        details = [
            ("MCC/MNC", "mcc_mnc"),
            ("Network State", "state"),
            ("Data State", "data_state"),
            ("Roaming", "roaming"),
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
        
        operator_layout.addLayout(details_grid)
        layout.addWidget(operator_container)
        
        # Signal metrics
        metrics_grid = QGridLayout()
        metrics_grid.setSpacing(16)
        
        self.rsrp_card = CellularMetricCard("RSRP", " dBm")
        self.rsrq_card = CellularMetricCard("RSRQ", " dB")
        self.rssi_card = CellularMetricCard("RSSI", " dBm")
        self.sinr_card = CellularMetricCard("SINR", " dB")
        
        metrics_grid.addWidget(self.rsrp_card, 0, 0)
        metrics_grid.addWidget(self.rsrq_card, 0, 1)
        metrics_grid.addWidget(self.rssi_card, 1, 0)
        metrics_grid.addWidget(self.sinr_card, 1, 1)
        
        layout.addLayout(metrics_grid)
        
        # Cell info
        cell_container = QWidget()
        cell_container.setStyleSheet(f"""
            QWidget {{
                background-color: {config.background_secondary};
                border: 1px solid {config.border_color};
                border-radius: 10px;
            }}
        """)
        cell_layout = QGridLayout(cell_container)
        cell_layout.setContentsMargins(24, 20, 24, 20)
        cell_layout.setSpacing(16)
        
        cell_header = QLabel("SERVING CELL")
        cell_header.setStyleSheet(f"color: {config.text_secondary}; font-size: 11px; font-weight: 600;")
        cell_layout.addWidget(cell_header, 0, 0, 1, 2)
        
        cell_details = [
            ("Cell ID", "cell_id"),
            ("TAC", "tac"),
            ("PCI", "pci"),
            ("Band", "band"),
        ]
        
        row = 1
        for label_text, key in cell_details:
            label = QLabel(label_text)
            label.setStyleSheet(f"color: {config.text_secondary}; font-size: 11px; font-weight: 600;")
            
            value = QLabel("--")
            value.setStyleSheet(f"color: {config.text_primary}; font-size: 13px;")
            
            cell_layout.addWidget(label, row, 0)
            cell_layout.addWidget(value, row, 1)
            
            self.detail_labels[key] = value
            row += 1
        
        layout.addWidget(cell_container)
        
        # Signal strength graph
        signal_container = self._create_graph_container("SIGNAL QUALITY")
        self.signal_plot = pg.PlotWidget()
        self._setup_plot(self.signal_plot)
        self.rsrp_curve = self.signal_plot.plot(pen=pg.mkPen(color=config.accent_green, width=2), name="RSRP")
        self.rsrq_curve = self.signal_plot.plot(pen=pg.mkPen(color=config.accent_blush_red, width=2), name="RSRQ")
        self.signal_plot.addLegend()
        signal_container.layout().addWidget(self.signal_plot)
        layout.addWidget(signal_container)
    
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
        
        container.setMinimumHeight(250)
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
        """Subscribe to cellular metrics."""
        metric_bus.subscribe(EventCategory.NETWORK, self._on_cellular_metric)
    
    def _on_cellular_metric(self, event: MetricEvent):
        """Handle cellular metric."""
        if event.source != "cellular":
            return
        
        if event.metric == "network_type":
            self.network_type_label.setText(event.value)
        elif event.metric == "operator":
            self.operator_label.setText(event.value)
        elif event.metric == "rsrp":
            self.rsrp_card.update_value(event.value)
            self._update_signal_graph(event.value, "rsrp")
        elif event.metric == "rsrq":
            self.rsrq_card.update_value(event.value)
            self._update_signal_graph(event.value, "rsrq")
        elif event.metric == "rssi":
            self.rssi_card.update_value(event.value)
        elif event.metric == "sinr":
            self.sinr_card.update_value(event.value)
        elif event.metric in self.detail_labels:
            self.detail_labels[event.metric].setText(str(event.value))
    
    def _update_signal_graph(self, value: float, signal_type: str):
        """Update signal graph."""
        if signal_type == "rsrp":
            self.rsrp_data.append(value)
        else:
            self.rsrq_data.append(value)
        
        if signal_type == "rsrp":
            self.time_counter += 1
            self.time_data.append(self.time_counter)
        
        if len(self.rsrp_data) > 1 and len(self.rsrq_data) > 1:
            time_list = list(range(len(self.rsrp_data)))
            self.rsrp_curve.setData(time_list, list(self.rsrp_data))
            self.rsrq_curve.setData(time_list, list(self.rsrq_data))
