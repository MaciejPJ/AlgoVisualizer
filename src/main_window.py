from PyQt5.QtWidgets import (QMainWindow, QPushButton, QLabel, QVBoxLayout, 
                             QWidget, QGraphicsView, QGraphicsScene, QGraphicsRectItem,
                             QComboBox, QSlider, QHBoxLayout, QGraphicsSimpleTextItem,
                             QGraphicsColorizeEffect)
from PyQt5.QtCore import QTimer, pyqtSignal, Qt
from PyQt5.QtGui import QBrush, QColor, QFont
from typing import Generator
from pathlib import Path
import random
from sorting import bubble_sort, quick_sort, selection_sort, insertion_sort

# colors
BLUE_COLOR = "#2471A3"
RED_COLOR = "#e11212"
GREEN_COLOR = "#2ecc71"  
YELLOW_COLOR = "#f1c40f"  
PIVOT_COLOR = "#e67e22"   
TEXT_COLOR = "#000000"
SELECT_COLOR = "#e67e22"
INSERT_COLOR = "#2ecc71"     

INTERVAL_TIME = 700

SAMPLES = 30


class CustomGraphicsView(QGraphicsView):
    """
    Custom widget QGraphicsView with signalling of size change.
    """
    # Emitted signal by size change.
    resized = pyqtSignal()

    def resizeEvent(self, event):
        """
        Captures the event resize and emitts the signal.
        """
        super().resizeEvent(event)
        self.resized.emit()


class MainWindow(QMainWindow):
    """
    Main window of the application.
    """
    def __init__(self):
        """
        Initializes the interface and application state.
        """
        super().__init__()
        self.setWindowTitle("Simple Visualizer")
        self.setGeometry(0, 0, 1280, 720)

        # Data and state
        self.original_data = random.sample(range(1, 100), SAMPLES)
        self.data = self.original_data.copy()
        self.is_playing = False
        self.paused = False
        self.generator = None
        self.current_highlighted = None

        # Widgets
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        control_layout = QHBoxLayout()
        self.algorithm_selector = QComboBox()
        self.algorithm_selector.addItems(["BubbleSort", "QuickSort", "SelectionSort",
                                          "InsertionSort"]) # <-- Add new algorithms here

        # Canvas
        self.canvas = CustomGraphicsView()
        self.scene = QGraphicsScene()
        self.canvas.setScene(self.scene)
        self.canvas.resized.connect(self._handle_canvas_resize)

        # Buttons
        self.btn_start = QPushButton("Start")
        self.btn_pause = QPushButton("Pause")
        self.btn_reset = QPushButton("Reset")
        self.label_status = QLabel("Press Start")
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(50, 2000) # in ms
        self.speed_slider.setValue(INTERVAL_TIME)
        self.speed_slider.valueChanged.connect(self._update_speed)

        layout.addWidget(self.algorithm_selector)
        layout.addWidget(self.btn_start)
        layout.addWidget(self.btn_pause)
        layout.addWidget(self.btn_reset)
        layout.addWidget(self.label_status)
        layout.addWidget(self.canvas)
        control_layout.addWidget(QLabel("Animation time:"))
        control_layout.addWidget(self.speed_slider)
        layout.insertLayout(1, control_layout)

        # Connect the signal
        self.btn_start.clicked.connect(self._on_start_clicked)
        self.btn_pause.clicked.connect(self._on_pause_clicked)
        self.btn_reset.clicked.connect(self._on_reset_clicked)

        # Animation Timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_animation)

        # Default buttons state
        self.btn_pause.setEnabled(False)
        self.btn_reset.setEnabled(False)

        # Drawing
        self.draw_bars(self.data)

        # Load styles from .qss file
        self._load_styles()

        

    def _on_start_clicked(self):
        """
        Start button handling
        """
        if not self.is_playing:
            algorithm_name = self.algorithm_selector.currentText()
            self.generator = self._get_algorithm_generator(algorithm_name)
            # Start new animation
            self.data = self.original_data.copy()
            self.generator = self._get_algorithm_generator(algorithm_name)
            self.is_playing = True
            self.paused = False
            self.timer.start(INTERVAL_TIME)
            self.label_status.setText("Executing...")
        elif self.paused:
            # Resume existing animation
            self.paused = False
            self.timer.start(INTERVAL_TIME)
            self.label_status.setText("Executing...")

        # Buttons state update
        self.btn_start.setEnabled(False)
        self.btn_pause.setEnabled(True)
        self.btn_reset.setEnabled(True)

    def _on_pause_clicked(self):
        """
        Pause button handling.
        """
        self.paused = not self.paused # State toggle
        if self.paused:
            self.timer.stop()
            self.label_status.setText("Paused.")
            self.btn_pause.setText("Resume")
        else:
            self.timer.start(INTERVAL_TIME)
            self.label_status.setText("Executing...")
            self.btn_pause.setText("Pause")

    def _on_reset_clicked(self):
        """
        Reset button handling.
        """
        self.timer.stop()
        self.is_playing = False
        self.paused = False
        self.data = self.original_data.copy()
        self.draw_bars(self.data)
        self.label_status.setText("Reset")

        self.btn_start.setEnabled(True)
        self.btn_pause.setEnabled(False)
        self.btn_reset.setEnabled(False)
        self.btn_pause.setText("Pause")

        # Reset the generator when button is pressed
        self.generator = None

    def _update_animation(self):
        """
        Animation update every interval of timer.
        """
        if self.is_playing and not self.paused:
            try:
                # next generator step
                data, highlighted, operation_type = next(self.generator)
                self.data = data
                self.draw_bars(data, highlighted, operation_type)
            except StopIteration:
                # end of the algorithm
                self.draw_bars(self.data, list(range(len(self.data))), 'completed')
                self.timer.stop()
                self.is_playing = False
                self.label_status.setText("Finished!")
                self.btn_start.setEnabled(True)
                self.btn_pause.setEnabled(False)

    def _update_speed(self, value: int):
        """
        Updates the speed of animation.

        Args:
            value (int): Speed of animation in miliseconds.
        """
        global INTERVAL_TIME
        INTERVAL_TIME = value
        if self.timer.isActive():
            self.timer.setInterval(value)

    def _load_styles(self):
        """
        Loads stylees from .qss file
        """
        style_path = Path(__file__).parent / "styles.qss"
        with open(style_path, "r") as f:
            self.setStyleSheet(f.read())

    def _get_algorithm_generator(self, name: str) -> Generator:
        """
        Returns step generator for the choosen algorithm.

        Args:
            name (str): Name of the algorithm from the lsit.

        Returns:
            Generator: Object of the step generator.
        """
        algorithms = {
            "BubbleSort": bubble_sort,
            "QuickSort": quick_sort,
            "SelectionSort": selection_sort,
            "InsertionSort": insertion_sort,
        }
        return algorithms[name](self.data.copy())

    def _handle_canvas_resize(self):
        """
        Updates visualization by change of the canvas' size
        """
        self.draw_bars(self.data, self.current_highlighted)

    def draw_bars(self, data, highlighted=None, operation_type=None):
        """
        Draws bars on the scene.

        Args:
            data (list): List of values to visualize.
            highlighted (list, optional): Indicies of highlighted elements.
            operation_type: Type of operation, important for different colors 
                            ('compare', 'swap', 'pivot')
        """
        self.scene.clear()
        width = self.canvas.width()
        height = self.canvas.height()

        if not data:
            return
        
        bar_width = width / len(data) - 2 # Width of a bar with space between included
        max_value = max(data) if data else 1
        font_size = max(5, int(bar_width * 0.4)) # Dynamic font size
        margin_bottom = 30

        for i, value in enumerate(data):
            x = i * (bar_width + 2) # Spacing of 2px between bars
            bar_height = (value / max_value) * (height - margin_bottom) - 20

            # y coordinate from the bottom of canvas
            y = height - bar_height - margin_bottom + 10

            # Main bra color
            base_color = BLUE_COLOR

            # Coloring logic
            if highlighted and i in highlighted:
                if operation_type == 'compare':
                    base_color = YELLOW_COLOR
                elif operation_type == 'swap':
                    base_color = GREEN_COLOR
                elif operation_type == 'pivot':
                    base_color = PIVOT_COLOR
                elif operation_type == 'select':
                    base_color = SELECT_COLOR
                elif operation_type == 'insert':
                    base_color = INSERT_COLOR
                else:
                    base_color = RED_COLOR

            # bar width - 2 includes 2px space between bars
            rect = QGraphicsRectItem(x, y, bar_width - 2, bar_height)
            rect.setBrush(QBrush(QColor(base_color)))
            self.scene.addItem(rect)

            text = QGraphicsSimpleTextItem(str(value))
            text.setFont(QFont("Arial", font_size))
            text.setPos(x + (bar_width/2 - font_size*0.75), y - font_size - 10)
            text.setBrush(QBrush(QColor(TEXT_COLOR)))
            self.scene.addItem(text)
        
            # A highlight animation
            if highlighted and i in highlighted:
                effect = QGraphicsColorizeEffect()
                effect.setColor(QColor(base_color).darker(150))
                rect.setGraphicsEffect(effect)



