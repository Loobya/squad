import os
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from windows.test_window import TestWindow

class MilitaryLineEdit(QLineEdit):
    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setMinimumHeight(50)
        self.setFont(QFont("Arial", 14))
        
        self.setStyleSheet("""
            QLineEdit {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #4a7c45, stop: 0.5 #3a6635, stop: 1 #2d5429);
                color: white;
                border: 3px solid #1a3317;
                border-radius: 8px;
                padding: 12px;
                font-size: 16px;
                selection-background-color: #5d9557;
            }
            QLineEdit:focus {
                border: 3px solid #5d9557;
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #5d9557, stop: 0.5 #4a7c45, stop: 1 #3a6635);
            }
            QLineEdit::placeholder {
                color: #c8e6c9;
                font-style: italic;
            }
        """)

class UserEntryWindow(QDialog):
    def __init__(self, mode, parent=None):
        super().__init__(parent)
        self.mode = mode  # 'test' or 'practice'
        self.parent = parent
        self.init_ui()
        
    def init_ui(self):
        title = "اختبار - Test" if self.mode == "test" else "تمرين - Practice"
        self.setWindowTitle(title)
        self.setModal(True)
        self.setFixedSize(600, 500)
        
        # Apply military theme
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #2d5a27, stop: 0.3 #3a6b34, stop: 0.7 #2d5a27, stop: 1 #1e3f1a);
                border: 3px solid #1a3317;
                border-radius: 15px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(25)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Title section
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
        
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setStyleSheet("color: white; padding: 20px;")
        
        subtitle_label = QLabel("أدخل بياناتك - Enter Your Information")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setFont(QFont("Arial", 16))
        subtitle_label.setStyleSheet("color: #e8f5e8; padding: 10px;")
        
        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)
        layout.addWidget(title_frame)
        
        # Input section
        input_frame = QFrame()
        input_frame.setStyleSheet("""
            QFrame {
                background: rgba(58, 107, 52, 0.8);
                border: 2px solid #2d5429;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        input_layout = QVBoxLayout(input_frame)
        input_layout.setSpacing(20)
        
        # Name input
        name_container = QVBoxLayout()
        name_label = QLabel("الاسم الكامل - Full Name:")
        name_label.setFont(QFont("Arial", 14, QFont.Bold))
        name_label.setStyleSheet("color: white; padding: 5px;")
        
        self.name_input = MilitaryLineEdit("أدخل اسمك الكامل - Enter your full name")
        
        name_container.addWidget(name_label)
        name_container.addWidget(self.name_input)
        input_layout.addLayout(name_container)
        
        # ID input
        id_container = QVBoxLayout()
        id_label = QLabel("رقم الهوية - ID Number:")
        id_label.setFont(QFont("Arial", 14, QFont.Bold))
        id_label.setStyleSheet("color: white; padding: 5px;")
        
        self.id_input = MilitaryLineEdit("أدخل رقم الهوية - Enter your ID number")
        
        id_container.addWidget(id_label)
        id_container.addWidget(self.id_input)
        input_layout.addLayout(id_container)
        
        layout.addWidget(input_frame)
        layout.addStretch(1)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        self.start_btn = self.create_military_button("بدء - Start", "#32CD32")
        self.cancel_btn = self.create_military_button("إلغاء - Cancel", "#CD5C5C")
        
        self.start_btn.clicked.connect(self.start_session)
        self.cancel_btn.clicked.connect(self.reject)
        
        buttons_layout.addWidget(self.start_btn)
        buttons_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
        
    def create_military_button(self, text, color):
        """Create military-style button"""
        button = QPushButton(text)
        button.setMinimumHeight(55)
        button.setFont(QFont("Arial", 16, QFont.Bold))
        
        darker_color = self.darken_color(color, 30)
        lighter_color = self.lighten_color(color, 20)
        
        button_style = f"""
            QPushButton {{
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 {lighter_color}, stop: 0.5 {color}, stop: 1 {darker_color});
                color: white;
                border: 3px solid {self.darken_color(color, 40)};
                border-radius: 8px;
                padding: 15px;
                font-weight: bold;
                min-width: 150px;
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
        
    def start_session(self):
        """Start test session"""
        name = self.name_input.text().strip()
        user_id = self.id_input.text().strip()
        
        if not name or not user_id:
            QMessageBox.warning(self, "خطأ - Error", 
                              "يرجى إدخال الاسم ورقم الهوية\nPlease enter both name and ID")
            return
            
        if self.mode == "test":
            self.accept()
            self.open_test_window(name, user_id)
        else:
            # For practice mode, we'll handle this differently
            pass
            
    def open_test_window(self, name, user_id):
        """Open test window with user info"""
        self.test_window = TestWindow(name, user_id, self.parent)
        self.test_window.show()