import os
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QStackedWidget, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QTimer
from PyQt5.QtGui import QFont, QPalette, QColor, QPixmap, QBrush
from PyQt5.QtCore import QRect, QSize

from windows.login_window import LoginWindow
from windows.admin_dashboard import AdminDashboard
from windows.user_entry import UserEntryWindow
from windows.course_window import CourseWindow
from utils.json_handler import JSONHandler

class AnimatedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(80)
        self.setFont(QFont("Arial", 18, QFont.Bold))
        
        # Animation setup
        self.animation = QPropertyAnimation(self, b"size")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.OutBack)
        
        self.original_size = QSize(300, 80)
        self.hover_size = QSize(320, 85)
        
        self.setFixedSize(self.original_size)
        
    def enterEvent(self, event):
        self.animation.setStartValue(self.size())
        self.animation.setEndValue(self.hover_size)
        self.animation.start()
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        self.animation.setStartValue(self.size())
        self.animation.setEndValue(self.original_size)
        self.animation.start()
        super().leaveEvent(event)

class BackgroundLabel(QLabel):
    """Custom QLabel for background that stretches to fill the window"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScaledContents(True)  # This makes the image stretch to fill the label
        self.setAlignment(Qt.AlignCenter)
        
    def set_background_image(self, image_path):
        """Load and set background image"""
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                self.setPixmap(pixmap)
                return True
        return False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(self.current_dir, "..", "data")
        self.assets_dir = os.path.join(self.current_dir, "..", "assets")
        self.config_file = os.path.join(self.data_dir, "config.json")
        
        self.background_label = None
        
        self.init_ui()
        self.load_config()
        self.setup_animations()
        
    def load_config(self):
        """Load configuration"""
        config = JSONHandler.read_json(self.config_file)
        # Always use military theme
        
    def init_ui(self):
        self.setWindowTitle("Interactive Tactical Training System - نظام التدريب التكتيكي التفاعلي")
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Set up the background first
        self.setup_background(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(50, 30, 50, 50)
        
        # Title section
        title_layout = QVBoxLayout()
        
        # Main title with military style
        title_label = QLabel("نظام التدريب التكتيكي التفاعلي")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 28, QFont.Bold))
        title_label.setStyleSheet("""
            QLabel {
                background: rgba(45, 90, 39, 0.85);
                color: #ffffff;
                font-size: 32px;
                border: 3px solid #2d5429;
                border-radius: 15px;
                padding: 25px;
                margin: 10px;
            }
        """)
        
        # Subtitle
        subtitle_label = QLabel("Interactive Tactical Training System")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setFont(QFont("Arial", 18, QFont.StyleItalic))
        subtitle_label.setStyleSheet("""
            QLabel {
                background: rgba(58, 107, 52, 0.8);
                color: #e8f5e8;
                font-size: 18px;
                border: 2px solid #2d5429;
                border-radius: 10px;
                padding: 15px;
                margin: 5px;
            }
        """)
        
        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)
        main_layout.addLayout(title_layout)
        
        # Add spacer
        main_layout.addStretch(1)
        
        # Buttons layout - using grid for better positioning
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(30)
        buttons_layout.setContentsMargins(100, 0, 100, 0)
        
        # Left column
        left_column = QVBoxLayout()
        left_column.setSpacing(20)
        
        # Right column
        right_column = QVBoxLayout()
        right_column.setSpacing(20)
        
        # Create animated buttons with different colors
        self.admin_btn = self.create_military_button("ADMIN", "#8B4513")  # Saddle Brown
        self.test_btn = self.create_military_button("اختبار", "#CD5C5C")   # Indian Red
        self.practice_btn = self.create_military_button("تمرين", "#4682B4") # Steel Blue
        self.lessons_btn = self.create_military_button("دروس", "#32CD32")   # Lime Green
        
        # Connect buttons
        self.admin_btn.clicked.connect(self.open_admin_login)
        self.test_btn.clicked.connect(self.open_test_mode)
        self.practice_btn.clicked.connect(self.open_practice_mode)
        self.lessons_btn.clicked.connect(self.open_lessons)
        
        # Distribute buttons between columns
        left_column.addWidget(self.admin_btn)
        left_column.addWidget(self.test_btn)
        right_column.addWidget(self.practice_btn)
        right_column.addWidget(self.lessons_btn)
        
        buttons_layout.addLayout(left_column)
        buttons_layout.addLayout(right_column)
        
        main_layout.addLayout(buttons_layout)
        
        # Add bottom spacer
        main_layout.addStretch(1)
        
        # Add tactical footer
        footer_label = QLabel("ⓘ نظام التدريب التكتيكي - الإصدار 1.0 | © 2024 القوات المسلحة")
        footer_label.setAlignment(Qt.AlignCenter)
        footer_label.setStyleSheet("""
            QLabel {
                background: rgba(30, 63, 26, 0.9);
                color: #90EE90;
                font-size: 14px;
                padding: 12px;
                border: 1px solid #2d5429;
                border-radius: 5px;
                margin: 5px;
            }
        """)
        main_layout.addWidget(footer_label)
        
        # Set window to fullscreen after UI is created
        self.showMaximized()
        
    def setup_background(self, central_widget):
        """Setup background image that stretches to fill the window"""
        try:
            # Create background label
            self.background_label = BackgroundLabel(central_widget)
            
            # Set background image
            background_path = os.path.join(self.assets_dir, "backgrounds", "military_background.jpg")
            
            if os.path.exists(background_path):
                success = self.background_label.set_background_image(background_path)
                if success:
                    print("✓ Background image loaded and stretched successfully")
                else:
                    print("✗ Failed to load background image, using fallback")
                    self.set_fallback_background()
            else:
                print("ℹ No background image found, using fallback gradient")
                self.set_fallback_background()
                
            # Make sure background stays behind other widgets
            self.background_label.lower()
            self.background_label.setAttribute(Qt.WA_TransparentForMouseEvents)
            
        except Exception as e:
            print(f"✗ Error setting up background: {e}")
            self.set_fallback_background()
            
    def set_fallback_background(self):
        """Set fallback gradient background"""
        if self.background_label:
            self.background_label.setStyleSheet("""
                QLabel {
                    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                        stop: 0 #1e3f1a, stop: 0.3 #2d5a27, stop: 0.7 #1e3f1a, stop: 1 #0f1f0d);
                }
            """)
        
    def resizeEvent(self, event):
        """Handle window resize to update background size"""
        super().resizeEvent(event)
        
        if self.background_label:
            # Resize background to match window size
            self.background_label.setGeometry(0, 0, self.width(), self.height())
        
    def create_military_button(self, text, base_color):
        """Create a military-style animated button with specific color"""
        button = AnimatedButton(text)
        
        # Convert base color to darker and lighter variants
        darker_color = self.darken_color(base_color, 30)
        lighter_color = self.lighten_color(base_color, 20)
        
        button_style = f"""
            QPushButton {{
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 {lighter_color}, stop: 0.1 {base_color}, stop: 0.5 {base_color}, 
                    stop: 0.9 {darker_color}, stop: 1 {self.darken_color(darker_color, 20)});
                color: white;
                border: 3px solid {self.darken_color(base_color, 40)};
                border-radius: 10px;
                padding: 20px;
                font-size: 20px;
                font-weight: bold;
                text-align: center;
                min-height: 80px;
                min-width: 250px;
            }}
            
            QPushButton:hover {{
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 {self.lighten_color(base_color, 30)}, stop: 0.1 {self.lighten_color(base_color, 10)}, 
                    stop: 0.5 {self.lighten_color(base_color, 10)}, stop: 0.9 {base_color}, stop: 1 {darker_color});
                border: 3px solid {self.darken_color(base_color, 20)};
            }}
            
            QPushButton:pressed {{
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 {darker_color}, stop: 0.1 {self.darken_color(darker_color, 10)}, 
                    stop: 0.5 {darker_color}, stop: 0.9 {base_color}, stop: 1 {lighter_color});
            }}
        """
        
        button.setStyleSheet(button_style)
        return button
        
    def darken_color(self, hex_color, percent):
        """Darken a hex color by given percentage"""
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        
        r = max(0, int(r * (100 - percent) / 100))
        g = max(0, int(g * (100 - percent) / 100))
        b = max(0, int(b * (100 - percent) / 100))
        
        return f"#{r:02x}{g:02x}{b:02x}"
        
    def lighten_color(self, hex_color, percent):
        """Lighten a hex color by given percentage"""
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        
        r = min(255, int(r + (255 - r) * percent / 100))
        g = min(255, int(g + (255 - g) * percent / 100))
        b = min(255, int(b + (255 - b) * percent / 100))
        
        return f"#{r:02x}{g:02x}{b:02x}"
        
    def setup_animations(self):
        """Setup pulsing animations for buttons"""
        self.pulse_timer = QTimer()
        self.pulse_timer.timeout.connect(self.pulse_buttons)
        self.pulse_timer.start(2000)  # Pulse every 2 seconds
        
        self.pulse_state = 0
        
    def pulse_buttons(self):
        """Create pulsing effect on buttons"""
        buttons = [self.admin_btn, self.test_btn, self.practice_btn, self.lessons_btn]
        
        for i, button in enumerate(buttons):
            animation = QPropertyAnimation(button, b"geometry")
            animation.setDuration(500)
            animation.setEasingCurve(QEasingCurve.OutInSine)
            
            current_geo = button.geometry()
            if (i + self.pulse_state) % 4 == 0:
                # Slight grow effect
                animation.setStartValue(current_geo)
                animation.setEndValue(QRect(
                    current_geo.x() - 2, current_geo.y() - 2,
                    current_geo.width() + 4, current_geo.height() + 4
                ))
            else:
                # Return to normal
                animation.setStartValue(current_geo)
                animation.setEndValue(QRect(
                    current_geo.x() + 2, current_geo.y() + 2,
                    current_geo.width() - 4, current_geo.height() - 4
                ))
            
            animation.start()
        
        self.pulse_state = (self.pulse_state + 1) % 4
        
    def open_admin_login(self):
        """Open admin login window"""
        self.login_window = LoginWindow(self)
        self.login_window.show()
        
    def open_test_mode(self):
        """Open test mode - first ask for user info"""
        self.user_entry_window = UserEntryWindow("test", self)
        self.user_entry_window.show()
        
    def open_practice_mode(self):
        """Open practice mode - show scenario selection"""
        from windows.practice_window import PracticeWindow
        self.practice_window = PracticeWindow(self)
        self.practice_window.show()
        
    def open_lessons(self):
        """Open lessons/courses window"""
        self.course_window = CourseWindow(self)
        self.course_window.show()