import os
import subprocess
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QListWidget, QListWidgetItem,
                             QMessageBox, QFileDialog, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from utils.json_handler import JSONHandler

class CourseWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(self.current_dir, "..", "data")
        self.courses_file = os.path.join(self.data_dir, "courses.json")
        
        self.init_ui()
        self.load_courses()
        
    def init_ui(self):
        self.setWindowTitle("الدروس - Courses")
        self.setGeometry(100, 100, 900, 700)
        
        # Apply military theme
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #2d5a27, stop: 0.3 #3a6b34, stop: 0.7 #2d5a27, stop: 1 #1e3f1a);
            }
            QLabel {
                background: transparent;
                color: white;
                font-weight: bold;
            }
            QListWidget {
                background: rgba(58, 107, 52, 0.9);
                color: white;
                border: 2px solid #2d5429;
                border-radius: 5px;
                font-size: 16px;
            }
            QListWidget::item {
                padding: 15px;
                border-bottom: 1px solid #3a6635;
            }
            QListWidget::item:selected {
                background: #5d9557;
            }
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #4a7c45, stop: 0.5 #3a6635, stop: 1 #2d5429);
                color: white;
                border: 2px solid #1a3317;
                border-radius: 5px;
                padding: 15px;
                font-weight: bold;
                min-height: 50px;
                font-size: 16px;
            }
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #5d9557, stop: 0.5 #4a7c45, stop: 1 #3a6635);
            }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Title
        title = QLabel("الدروس التعليمية - Training Courses")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 22, QFont.Bold))
        title.setStyleSheet("""
            QLabel {
                color: white;
                background: rgba(58, 107, 52, 0.8);
                padding: 20px;
                border-radius: 10px;
                border: 2px solid #2d5429;
                margin: 10px;
            }
        """)
        layout.addWidget(title)
        
        # Instructions
        instructions = QLabel("اختر درساً من القائمة لعرض ملف الباوربوينت\nSelect a course to open PowerPoint presentation")
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setFont(QFont("Arial", 14))
        instructions.setStyleSheet("color: #c8e6c9; padding: 10px;")
        layout.addWidget(instructions)
        
        # Courses list
        self.courses_list = QListWidget()
        self.courses_list.itemDoubleClicked.connect(self.open_course_powerpoint)
        layout.addWidget(self.courses_list)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        self.open_btn = QPushButton("فتح العرض التقديمي - Open PowerPoint")
        self.add_course_btn = QPushButton("إضافة درس جديد - Add Course")
        self.back_btn = QPushButton("رجوع - Back")
        
        self.open_btn.clicked.connect(self.open_selected_course)
        self.add_course_btn.clicked.connect(self.add_new_course)
        self.back_btn.clicked.connect(self.close)
        
        buttons_layout.addWidget(self.open_btn)
        buttons_layout.addWidget(self.add_course_btn)
        buttons_layout.addWidget(self.back_btn)
        
        layout.addLayout(buttons_layout)
        
    def load_courses(self):
        """Load available courses"""
        self.courses_list.clear()
        courses = JSONHandler.read_json(self.courses_file) or []
        
        if not courses:
            no_courses_label = QLabel("لا توجد دروس متاحة - No courses available")
            no_courses_label.setAlignment(Qt.AlignCenter)
            no_courses_label.setStyleSheet("color: #ff6b6b; padding: 20px;")
            self.courses_list.addItem(no_courses_label.text())
            return
            
        for course in courses:
            title = course.get('title', 'Unknown Course')
            file_path = course.get('file_path', '')
            
            # Show file status in the list
            if file_path and os.path.exists(file_path):
                status = "✅"
            else:
                status = "❌"
                
            item_text = f"{status} {title}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, course)
            self.courses_list.addItem(item)
            
    def open_selected_course(self):
        """Open the selected course PowerPoint"""
        current_item = self.courses_list.currentItem()
        if current_item:
            self.open_course_powerpoint(current_item)
        else:
            QMessageBox.warning(self, "Warning", "Please select a course first\nيرجى اختيار درس أولاً")
            
    def open_course_powerpoint(self, item):
        """Open PowerPoint file for the selected course"""
        course_data = item.data(Qt.UserRole)
        title = course_data.get('title', 'Unknown Course')
        file_path = course_data.get('file_path', '')
        
        # Check if file exists
        if file_path and os.path.exists(file_path):
            self.launch_powerpoint(file_path)
        else:
            # File doesn't exist, ask for new path
            self.ask_for_file_path(course_data, title)
            
    def ask_for_file_path(self, course_data, title):
        """Ask user to locate the PowerPoint file"""
        reply = QMessageBox.question(
            self, 
            "File Not Found", 
            f"PowerPoint file for '{title}' not found.\n\nWould you like to locate the file?\n\nملف الباوربوينت للدرس '{title}' غير موجود.\nهل تريد تحديد موقع الملف؟",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.browse_for_powerpoint_file(course_data, title)
        else:
            QMessageBox.information(
                self, 
                "Information", 
                f"You can set the PowerPoint file later from the admin panel.\n\nيمكنك تعيين ملف الباوربوينت لاحقاً من لوحة التحكم."
            )
            
    def browse_for_powerpoint_file(self, course_data, title):
        """Open file dialog to browse for PowerPoint file"""
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self,
            f"Locate PowerPoint file for: {title}\nتحديد ملف الباوربوينت للدرس: {title}",
            "",
            "PowerPoint Files (*.pptx *.ppt);;All Files (*)"
        )
        
        if file_path:
            # Update course data with new file path
            course_data['file_path'] = file_path
            self.update_course_file_path(course_data)
            QMessageBox.information(
                self, 
                "Success", 
                f"PowerPoint file path updated successfully!\n\nتم تحديث مسار ملف الباوربوينت بنجاح!\n\nFile: {os.path.basename(file_path)}"
            )
            
            # Reload courses to show updated status
            self.load_courses()
            
            # Ask if user wants to open the file now
            reply = QMessageBox.question(
                self,
                "Open File",
                "Would you like to open the PowerPoint file now?\nهل تريد فتح ملف الباوربوينت الآن؟",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.launch_powerpoint(file_path)
                
    def update_course_file_path(self, updated_course):
        """Update course file path in the JSON file"""
        courses = JSONHandler.read_json(self.courses_file) or []
        
        for i, course in enumerate(courses):
            if course.get('id') == updated_course.get('id'):
                courses[i] = updated_course
                break
                
        JSONHandler.write_json(self.courses_file, courses)
        
    def launch_powerpoint(self, file_path):
        """Launch PowerPoint file using system default program"""
        try:
            if os.name == 'nt':  # Windows
                os.startfile(file_path)
            else:  # macOS and Linux
                if sys.platform == 'darwin':  # macOS
                    subprocess.call(('open', file_path))
                else:  # Linux
                    subprocess.call(('xdg-open', file_path))
                    
            QMessageBox.information(
                self,
                "Success",
                f"PowerPoint presentation is opening...\n\nعرض الباوربوينت يفتح الآن...\n\nFile: {os.path.basename(file_path)}"
            )
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to open PowerPoint file:\n{str(e)}\n\nفشل في فتح ملف الباوربوينت:\n{str(e)}"
            )
            
    def add_new_course(self):
        """Add a new course to the system"""
        from PyQt5.QtWidgets import QInputDialog
        
        title, ok = QInputDialog.getText(
            self, 
            "Add New Course - إضافة درس جديد",
            "Enter course title:\nأدخل عنوان الدرس:"
        )
        
        if ok and title:
            # Ask for PowerPoint file
            file_dialog = QFileDialog()
            file_path, _ = file_dialog.getOpenFileName(
                self,
                f"Select PowerPoint file for: {title}\nاختر ملف الباوربوينت للدرس: {title}",
                "",
                "PowerPoint Files (*.pptx *.ppt);;All Files (*)"
            )
            
            if file_path:
                # Create new course
                import random
                new_course = {
                    "title": title,
                    "file_path": file_path,
                    "id": f"course_{random.randint(1000, 9999)}",
                    "added_date": self.get_current_date()
                }
                
                # Add to courses list
                courses = JSONHandler.read_json(self.courses_file) or []
                courses.append(new_course)
                
                if JSONHandler.write_json(self.courses_file, courses):
                    QMessageBox.information(
                        self,
                        "Success",
                        f"Course '{title}' added successfully!\n\nتم إضافة الدرس '{title}' بنجاح!"
                    )
                    self.load_courses()
                else:
                    QMessageBox.warning(
                        self,
                        "Error",
                        "Failed to save course.\n\nفشل في حفظ الدرس."
                    )
            else:
                QMessageBox.warning(
                    self,
                    "Warning",
                    "No file selected. Course was not added.\n\nلم يتم اختيار ملف. لم يتم إضافة الدرس."
                )
                
    def get_current_date(self):
        """Get current date in string format"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")