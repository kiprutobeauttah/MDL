"""Performance monitoring view."""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QProgressBar
from PySide6.QtCore import Qt
import pyqtgraph as pg
from collections import deque
from mdl.core.events import EventCategory, MetricEvent, metric_bus
from mdl.core.config import config


class PerformanceMetricCard(QWidget):
    """Performance metric card."""
    
    def __init__(self, title: str, unit: str = ""):
        super().__init__()
        self.unit = unit
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(8)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"color: {config.text_secondary}; font-size: 11px; font-weight: 600;")
        
        self.value_label = QLabel("--")
        self.value_label.setStyleSheet(f"color: {config.text_primary}; font-size: 32px; font-weight: 700;")
        
        # Progress bar
        self.progress = QProgressBar()
        self.progress.setMaximum(100)
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(6)
        self.progress.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                border-radius: 3px;
                background-color: {config.background_tertiary};
            }}
            QProgressBar::chunk {{
                background-color: {config.accent_blush_red};
                border-radius: 3px;
            }}
        """)
        
        layout.addWidget(title_label)
        layout.addWidget(self.value_label)
        layout.addWidget(self.progress)
        
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {config.background_secondary};
                border: 1px solid {config.border_color};
                border-radius: 10px;
            }}
        """)
        self.setMinimumHeight(120)
    
    def update_value(self, value, max_value=100):
        """Update value and progress."""
        if isinstance(value, float):
            self.value_label.setText(f"{value:.1f}{self.unit}")
            percent = int((value / max_value) * 100) if max_value > 0 else 0
        elif isinstance(value, int):
            self.value_label.setText(f"{value}{self.unit}")
            percent = int((value / max_value) * 100) if max_value > 0 else 0
        else:
            self.value_label.setText(str(value))
            percent = 0
        
        self.progress.setValue(percent)


class PerformanceView(QWidget):
    """Performance monitoring view."""
    
    def __init__(self):
        super().__init__()
        
        # History data
        self.max_points = 60
        self.cpu_data = deque(maxlen=self.max_points)
        self.ram_data = deque(maxlen=self.max_points)
        self.time_data = deque(maxlen=self.max_points)
        self.time_counter = 0
        
        self._ram_total = 1
        
        self._init_ui()
        self._subscribe()
    
    def _init_ui(self):
        """Initialize UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(24)
        
        # Header
        header = QLabel("PERFORMANCE")
        header.setStyleSheet(f"color: {config.text_primary}; font-size: 20px; font-weight: 700;")
        layout.addWidget(header)
        
        # Metrics grid
        metrics_grid = QGridLayout()
        metrics_grid.setSpacing(16)
        
        self.cpu_card = PerformanceMetricCard("CPU", "%")
        self.ram_card = PerformanceMetricCard("RAM", " MB")
        self.storage_card = PerformanceMetricCard("STORAGE", " GB")
        
        metrics_grid.addWidget(self.cpu_card, 0, 0)
        metrics_grid.addWidget(self.ram_card, 0, 1)
        metrics_grid.addWidget(self.storage_card, 0, 2)
        
        layout.addLayout(metrics_grid)
        
        # CPU graph
        cpu_container = self._create_graph_container("CPU USAGE (%)")
        self.cpu_plot = pg.PlotWidget()
        self._setup_plot(self.cpu_plot)
        cpu_container.layout().addWidget(self.cpu_plot)
        layout.addWidget(cpu_container)
        
        # RAM graph
        ram_container = self._create_graph_container("RAM USAGE (MB)")
        self.ram_plot = pg.PlotWidget()
        self._setup_plot(self.ram_plot)
        ram_container.layout().addWidget(self.ram_plot)
        layout.addWidget(ram_container)
    
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
        """Subscribe to performance metrics."""
        metric_bus.subscribe(EventCategory.PERFORMANCE, self._on_performance_metric)
    
    def _on_performance_metric(self, event: MetricEvent):
        """Handle performance metric."""
        if event.metric == "cpu_usage":
            self.cpu_card.update_value(event.value, 100)
            self._update_cpu_graph(event.value)
        
        elif event.metric == "ram_used":
            self.ram_card.update_value(event.value, self._ram_total)
            self._update_ram_graph(event.value)
        
        elif event.metric == "ram_total":
            self._ram_total = event.value
        
        elif event.metric == "storage_used":
            storage_gb = event.value / 1024  # Convert MB to GB
            self.storage_card.update_value(storage_gb, 256)
    
    def _update_cpu_graph(self, value: float):
        """Update CPU graph."""
        self.time_counter += 1
        self.time_data.append(self.time_counter)
        self.cpu_data.append(value)
        
        if len(self.cpu_data) > 1:
            self.cpu_plot.plot(
                list(self.time_data),
                list(self.cpu_data),
                pen=pg.mkPen(color=config.accent_blush_red, width=2),
                clear=True
            )
    
    def _update_ram_graph(self, value: int):
        """Update RAM graph."""
        self.ram_data.append(value)
        
        if len(self.ram_data) > 1:
            time_list = list(range(len(self.ram_data)))
            self.ram_plot.plot(
                time_list,
                list(self.ram_data),
                pen=pg.mkPen(color=config.accent_green, width=2),
                clear=True
            )
