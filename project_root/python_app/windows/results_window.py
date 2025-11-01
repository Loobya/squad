import os
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor

class ResultsWindow(QMainWindow):
    def __init__(self, result_data, parent=None):
        super().__init__(parent)
        self.result_data = result_data
        self.parent = parent
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("نتائج الاختبار - Test Results")
        self.setGeometry(150, 150, 600, 500)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Title
        title = QLabel("نتائج الاختبار")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 20, QFont.Bold))
        layout.addWidget(title)
        
        # User info
        user_info = QLabel(f"المستخدم: {self.result_data['name']} - الرقم: {self.result_data['user_id']}")
        user_info.setAlignment(Qt.AlignCenter)
        user_info.setFont(QFont("Arial", 14))
        layout.addWidget(user_info)
        
        # Date
        date_label = QLabel(f"التاريخ: {self.result_data['date']}")
        date_label.setAlignment(Qt.AlignCenter)
        date_label.setFont(QFont("Arial", 12))
        layout.addWidget(date_label)
        
        # Score frame
        score_frame = QFrame()
        score_frame.setFrameStyle(QFrame.Box)
        score_frame.setStyleSheet("background-color: #f0f0f0; border-radius: 10px; padding: 20px;")
        score_layout = QVBoxLayout(score_frame)
        
        # Score
        score_text = QLabel(f"النتيجة النهائية: {self.result_data['score']}%")
        score_text.setAlignment(Qt.AlignCenter)
        score_text.setFont(QFont("Arial", 24, QFont.Bold))
        
        # Color code based on score
        if self.result_data['score'] >= 80:
            score_text.setStyleSheet("color: green;")
        elif self.result_data['score'] >= 60:
            score_text.setStyleSheet("color: orange;")
        else:
            score_text.setStyleSheet("color: red;")
            
        score_layout.addWidget(score_text)
        layout.addWidget(score_frame)
        
        # Details
        details_layout = QVBoxLayout()
        
        correct_label = QLabel(f"الإجابات الصحيحة: {self.result_data['right']}")
        correct_label.setFont(QFont("Arial", 14))
        details_layout.addWidget(correct_label)
        
        wrong_label = QLabel(f"الإجابات الخاطئة: {self.result_data['wrong']}")
        wrong_label.setFont(QFont("Arial", 14))
        details_layout.addWidget(wrong_label)
        
        total_label = QLabel(f"إجمالي الأسئلة: {self.result_data['right'] + self.result_data['wrong']}")
        total_label.setFont(QFont("Arial", 14))
        details_layout.addWidget(total_label)
        
        scenarios_label = QLabel(f"عدد السيناريوهات: {self.result_data.get('scenarios_played', 'N/A')}")
        scenarios_label.setFont(QFont("Arial", 14))
        details_layout.addWidget(scenarios_label)
        
        layout.addLayout(details_layout)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        self.close_btn = QPushButton("إغلاق")
        self.restart_btn = QPushButton("اختبار جديد")
        
        self.close_btn.clicked.connect(self.close)
        self.restart_btn.clicked.connect(self.restart_test)
        
        buttons_layout.addWidget(self.close_btn)
        buttons_layout.addWidget(self.restart_btn)
        
        layout.addLayout(buttons_layout)
        
    def restart_test(self):
        """Restart test mode"""
        if self.parent:
            from windows.user_entry import UserEntryWindow
            self.user_entry = UserEntryWindow("test", self.parent)
            self.user_entry.show()
        self.close()