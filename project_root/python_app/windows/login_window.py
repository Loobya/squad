import os
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QFrame)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QPalette, QColor

from windows.admin_dashboard import AdminDashboard
from utils.json_handler import JSONHandler

class MilitaryLineEdit(QLineEdit):
    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setMinimumHeight(40)
        self.setFont(QFont("Arial", 12))
        
        self.setStyleSheet("""
            QLineEdit {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #4a7c45, stop: 0.5 #3a6635, stop: 1 #2d5429);
                color: white;
                border: 2px solid #1a3317;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
                selection-background-color: #5d9557;
            }
            QLineEdit:focus {
                border: 2px solid #5d9557;
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #5d9557, stop: 0.5 #4a7c45, stop: 1 #3a6635);
            }
        """)

class LoginWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(self.current_dir, "..", "data")
        self.config_file = os.path.join(self.data_dir, "config.json")
        
        self.init_ui()
        self.setup_animations()
        
    def init_ui(self):
        self.setWindowTitle("Admin Access - الوصول الإداري")
        self.setModal(True)
        self.setFixedSize(600, 500)
        
        # Apply military theme
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #2d5a27, stop: 0.5 #3a6b34, stop: 1 #1e3f1a);
                border: 3px solid #1a3317;
                border-radius: 10px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title frame
        title_frame = QFrame()
        title_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 transparent, stop: 0.4 #3a6b34, stop: 0.6 #3a6b34, stop: 1 transparent);
                border: 2px solid #2d5429;
                border-radius: 10px;
            }
        """)
        title_layout = QVBoxLayout(title_frame)
        
        title = QLabel("Admin Authentication")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setStyleSheet("color: white; padding: 15px;")
        
        subtitle = QLabel("المصادقة الإدارية")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setFont(QFont("Arial", 16, QFont.Bold))
        subtitle.setStyleSheet("color: #c8e6c9; padding: 5px;")
        
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        layout.addWidget(title_frame)
        
        # Add spacer
        layout.addStretch(1)
        
        # Password input section
        input_frame = QFrame()
        input_frame.setStyleSheet("""
            QFrame {
                background: rgba(58, 107, 52, 0.8);
                border: 2px solid #2d5429;
                border-radius: 8px;
            }
        """)
        input_layout = QVBoxLayout(input_frame)
        input_layout.setSpacing(15)
        input_layout.setContentsMargins(20, 20, 20, 20)
        
        password_label = QLabel("Enter Admin Password:")
        password_label.setAlignment(Qt.AlignCenter)
        password_label.setFont(QFont("Arial", 14, QFont.Bold))
        password_label.setStyleSheet("color: white;")
        
        arabic_label = QLabel("أدخل كلمة مرور المدير:")
        arabic_label.setAlignment(Qt.AlignCenter)
        arabic_label.setFont(QFont("Arial", 12))
        arabic_label.setStyleSheet("color: #e8f5e8;")
        
        self.password_input = MilitaryLineEdit("Password - كلمة المرور")
        self.password_input.setEchoMode(QLineEdit.Password)
        
        input_layout.addWidget(password_label)
        input_layout.addWidget(arabic_label)
        input_layout.addWidget(self.password_input)
        
        layout.addWidget(input_frame)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        self.login_btn = self.create_military_button("Login - دخول", "#32CD32")
        self.cancel_btn = self.create_military_button("Cancel - إلغاء", "#CD5C5C")
        
        self.login_btn.clicked.connect(self.authenticate)
        self.cancel_btn.clicked.connect(self.reject)
        
        buttons_layout.addWidget(self.login_btn)
        buttons_layout.addWidget(self.cancel_btn)
        layout.addLayout(buttons_layout)
        
        # Add bottom spacer
        layout.addStretch(1)
        
        self.setLayout(layout)
        
    def create_military_button(self, text, color):
        """Create military-style button"""
        button = QPushButton(text)
        button.setMinimumHeight(45)
        button.setFont(QFont("Arial", 12, QFont.Bold))
        
        darker_color = self.darken_color(color, 30)
        lighter_color = self.lighten_color(color, 20)
        
        button_style = f"""
            QPushButton {{
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 {lighter_color}, stop: 0.5 {color}, stop: 1 {darker_color});
                color: white;
                border: 2px solid {self.darken_color(color, 40)};
                border-radius: 6px;
                padding: 10px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 {self.lighten_color(color, 30)}, stop: 0.5 {self.lighten_color(color, 10)}, stop: 1 {color});
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 {darker_color}, stop: 0.5 {self.darken_color(darker_color, 10)}, stop: 1 {color});
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
        """Setup animations for the login window"""
        # Add a subtle glow animation to the title
        self.title_animation = QPropertyAnimation(self, b"windowOpacity")
        self.title_animation.setDuration(1500)
        self.title_animation.setStartValue(0.9)
        self.title_animation.setEndValue(1.0)
        self.title_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.title_animation.start()
        
    def authenticate(self):
        """Check admin password"""
        password = self.password_input.text()
        config = JSONHandler.read_json(self.config_file)
        
        if config and config.get("admin_password") == password:
            # Success animation
            self.login_btn.setStyleSheet(self.login_btn.styleSheet().replace("color", "#32CD32"))
            
            self.accept()
            self.open_admin_dashboard()
        else:
            # Error animation
            error_animation = QPropertyAnimation(self.password_input, b"pos")
            error_animation.setDuration(100)
            error_animation.setEasingCurve(QEasingCurve.InOutSine)
            current_pos = self.password_input.pos()
            error_animation.setStartValue(current_pos)
            error_animation.setKeyValueAt(0.3, current_pos + self.password_input.mapToParent(self.password_input.rect().topRight() * 0.1))
            error_animation.setEndValue(current_pos)
            error_animation.start()
            
            QMessageBox.warning(self, "Error", "Incorrect password! - كلمة مرور خاطئة")
            
    def open_admin_dashboard(self):
        """Open admin dashboard"""
        self.admin_dashboard = AdminDashboard(self.parent)
        self.admin_dashboard.show()