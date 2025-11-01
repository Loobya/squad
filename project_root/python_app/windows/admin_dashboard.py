import os
import random
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QListWidget, QListWidgetItem,
                             QMessageBox, QInputDialog, QLineEdit, QTabWidget,
                             QTextEdit, QSplitter, QFrame, QFileDialog)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon

from utils.json_handler import JSONHandler
from utils.process_launcher import ProcessLauncher

class AdminDashboard(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(self.current_dir, "..", "data")
        self.scenarios_dir = os.path.join(self.data_dir, "scenarios")
        self.config_file = os.path.join(self.data_dir, "config.json")
        self.courses_file = os.path.join(self.data_dir, "courses.json")
        self.history_file = os.path.join(self.data_dir, "history.json")
        
        # Fix: Use absolute path for Java apps
        project_root = os.path.dirname(os.path.dirname(self.current_dir))
        java_app_path = os.path.join(project_root, "java_app")
        self.process_launcher = ProcessLauncher(java_app_path)
        
        self.init_ui()
        self.load_data()
        
    def init_ui(self):
        self.setWindowTitle("Admin Dashboard - لوحة التحكم")
        self.setGeometry(100, 100, 1000, 700)
        
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
                font-size: 14px;
            }
            QListWidget::item {
                padding: 10px;
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
                padding: 10px;
                font-weight: bold;
                min-height: 35px;
            }
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #5d9557, stop: 0.5 #4a7c45, stop: 1 #3a6635);
            }
            QTabWidget::pane {
                border: 2px solid #2d5429;
                background: rgba(45, 90, 39, 0.9);
            }
            QTabBar::tab {
                background: #3a6635;
                color: white;
                padding: 10px 20px;
                border: 1px solid #2d5429;
                border-bottom: none;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            QTabBar::tab:selected {
                background: #5d9557;
            }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Title
        title = QLabel("لوحة تحكم المدير - Admin Dashboard")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setStyleSheet("color: white; background: rgba(58, 107, 52, 0.8); padding: 15px; border-radius: 10px;")
        layout.addWidget(title)
        
        # Tabs
        self.tabs = QTabWidget()
        
        # Scenarios Tab
        self.scenarios_tab = QWidget()
        self.init_scenarios_tab()
        self.tabs.addTab(self.scenarios_tab, "إدارة السيناريوهات - Scenarios")
        
        # Courses Tab
        self.courses_tab = QWidget()
        self.init_courses_tab()
        self.tabs.addTab(self.courses_tab, "إدارة الدروس - Courses")
        
        # History Tab
        self.history_tab = QWidget()
        self.init_history_tab()
        self.tabs.addTab(self.history_tab, "سجل النتائج - History")
        
        # Settings Tab (Simplified - only password change)
        self.settings_tab = QWidget()
        self.init_settings_tab()
        self.tabs.addTab(self.settings_tab, "الإعدادات - Settings")
        
        layout.addWidget(self.tabs)
        
    def init_scenarios_tab(self):
        layout = QVBoxLayout()
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        self.add_scenario_btn = QPushButton("إضافة سيناريو جديد - Add New Scenario")
        self.edit_scenario_btn = QPushButton("تعديل السيناريو - Edit Scenario")
        self.delete_scenario_btn = QPushButton("حذف السيناريو - Delete Scenario")
        self.view_scenario_btn = QPushButton("عرض السيناريو - View Scenario")
        
        self.add_scenario_btn.clicked.connect(self.add_scenario)
        self.edit_scenario_btn.clicked.connect(self.edit_scenario)
        self.delete_scenario_btn.clicked.connect(self.delete_scenario)
        self.view_scenario_btn.clicked.connect(self.view_scenario)
        
        buttons_layout.addWidget(self.add_scenario_btn)
        buttons_layout.addWidget(self.edit_scenario_btn)
        buttons_layout.addWidget(self.view_scenario_btn)
        buttons_layout.addWidget(self.delete_scenario_btn)
        
        layout.addLayout(buttons_layout)
        
        # Scenarios list
        self.scenarios_list = QListWidget()
        self.scenarios_list.itemDoubleClicked.connect(self.view_scenario)
        layout.addWidget(self.scenarios_list)
        
        self.scenarios_tab.setLayout(layout)
        
    def init_courses_tab(self):
        layout = QVBoxLayout()
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        self.add_course_btn = QPushButton("إضافة درس جديد - Add Course")
        self.edit_course_btn = QPushButton("تعديل الدرس - Edit Course")
        self.delete_course_btn = QPushButton("حذف الدرس - Delete Course")
        self.set_file_btn = QPushButton("تعيين ملف - Set PowerPoint File")
        
        self.add_course_btn.clicked.connect(self.add_course)
        self.edit_course_btn.clicked.connect(self.edit_course)
        self.delete_course_btn.clicked.connect(self.delete_course)
        self.set_file_btn.clicked.connect(self.set_course_file)
        
        buttons_layout.addWidget(self.add_course_btn)
        buttons_layout.addWidget(self.edit_course_btn)
        buttons_layout.addWidget(self.set_file_btn)
        buttons_layout.addWidget(self.delete_course_btn)
        
        layout.addLayout(buttons_layout)
        
        # Courses list
        self.courses_list = QListWidget()
        self.courses_list.itemDoubleClicked.connect(self.edit_course)
        layout.addWidget(self.courses_list)
        
        self.courses_tab.setLayout(layout)
        
    def init_history_tab(self):
        layout = QVBoxLayout()
        
        # History list
        self.history_list = QListWidget()
        layout.addWidget(self.history_list)
        
        # Clear history button
        self.clear_history_btn = QPushButton("مسح السجل - Clear History")
        self.clear_history_btn.clicked.connect(self.clear_history)
        layout.addWidget(self.clear_history_btn)
        
        self.history_tab.setLayout(layout)
        
    def init_settings_tab(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(50, 50, 50, 50)
        
        # Change password section
        password_frame = QFrame()
        password_frame.setStyleSheet("""
            QFrame {
                background: rgba(58, 107, 52, 0.8);
                border: 2px solid #2d5429;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        password_layout = QVBoxLayout(password_frame)
        
        password_title = QLabel("تغيير كلمة المرور - Change Password")
        password_title.setAlignment(Qt.AlignCenter)
        password_title.setFont(QFont("Arial", 16, QFont.Bold))
        password_title.setStyleSheet("color: white; padding: 10px;")
        
        self.change_password_btn = QPushButton("تغيير كلمة المرور - Change Password")
        self.change_password_btn.clicked.connect(self.change_password)
        self.change_password_btn.setMinimumHeight(50)
        
        password_layout.addWidget(password_title)
        password_layout.addWidget(self.change_password_btn)
        
        layout.addWidget(password_frame)
        layout.addStretch(1)
        
        self.settings_tab.setLayout(layout)
        
    def load_data(self):
        """Load all data into the dashboard"""
        self.load_scenarios()
        self.load_courses()
        self.load_history()
        
    def load_scenarios(self):
        """Load scenarios list"""
        self.scenarios_list.clear()
        if not os.path.exists(self.scenarios_dir):
            os.makedirs(self.scenarios_dir, exist_ok=True)
            
        for file in os.listdir(self.scenarios_dir):
            if file.endswith('.json'):
                scenario_path = os.path.join(self.scenarios_dir, file)
                scenario_data = JSONHandler.read_json(scenario_path)
                if scenario_data:
                    title = scenario_data.get('title', 'Unknown Scenario')
                    item = QListWidgetItem(f"{title} - [{file}]")
                    item.setData(Qt.UserRole, file)
                    self.scenarios_list.addItem(item)
                    
    def load_courses(self):
        """Load courses list with file status"""
        self.courses_list.clear()
        courses = JSONHandler.read_json(self.courses_file) or []
        
        if not courses:
            no_courses_item = QListWidgetItem("لا توجد دروس متاحة - No courses available")
            self.courses_list.addItem(no_courses_item)
            return
            
        for course in courses:
            title = course.get('title', 'Unknown Course')
            file_path = course.get('file_path', '')
            
            # Show file status
            if file_path and os.path.exists(file_path):
                status = "✅"
                file_info = os.path.basename(file_path)
            else:
                status = "❌"
                file_info = "No file set"
                
            item_text = f"{status} {title}\n   📁 {file_info}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, course)
            self.courses_list.addItem(item)
            
    def load_history(self):
        """Load history records"""
        self.history_list.clear()
        history = JSONHandler.read_json(self.history_file) or []
        for record in history:
            text = f"{record.get('name')} - {record.get('user_id')} - Score: {record.get('score')}% - {record.get('date')}"
            item = QListWidgetItem(text)
            self.history_list.addItem(item)
            
    def add_scenario(self):
        """Add new scenario using JavaFX editor"""
        try:
            print("🛠️ Admin: Attempting to launch scenario editor...")
            success = self.process_launcher.launch_scenario_editor()
            if success:
                QMessageBox.information(self, "Success", "Scenario editor launched successfully!\nمحرر السيناريو تم تشغيله بنجاح")
                print("✅ Admin: Scenario editor launch reported successful")
            else:
                QMessageBox.warning(self, "Error", "Failed to launch scenario editor\nفشل في تشغيل محرر السيناريو")
                print("❌ Admin: Scenario editor launch reported failed")
        except Exception as e:
            print(f"💥 Admin: Exception in add_scenario: {e}")
            QMessageBox.critical(self, "Error", f"Error launching editor: {str(e)}\nخطأ في تشغيل المحرر: {str(e)}")

    def edit_scenario(self):
        """Edit selected scenario"""
        current_item = self.scenarios_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Error", "Please select a scenario to edit\nيرجى اختيار سيناريو للتعديل")
            return
            
        scenario_file = current_item.data(Qt.UserRole)
        scenario_path = os.path.join(self.scenarios_dir, scenario_file)
        
        try:
            success = self.process_launcher.launch_scenario_editor(scenario_path)
            if success:
                QMessageBox.information(self, "Success", "Scenario editor launched successfully\nمحرر السيناريو تم تشغيله بنجاح")
            else:
                QMessageBox.warning(self, "Error", "Failed to launch scenario editor\nفشل في تشغيل محرر السيناريو")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error launching editor: {str(e)}\nخطأ في تشغيل المحرر: {str(e)}")
            
    def view_scenario(self):
        """View selected scenario in player"""
        current_item = self.scenarios_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Error", "Please select a scenario to view\nيرجى اختيار سيناريو للمعاينة")
            return
            
        scenario_file = current_item.data(Qt.UserRole)
        scenario_path = os.path.join(self.scenarios_dir, scenario_file)
        
        try:
            success = self.process_launcher.launch_scenario_player(scenario_path, "practice")
            if success:
                QMessageBox.information(self, "Success", "Scenario player launched successfully\nمشغل السيناريو تم تشغيله بنجاح")
            else:
                QMessageBox.warning(self, "Error", "Failed to launch scenario player\nفشل في تشغيل مشغل السيناريو")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error launching player: {str(e)}\nخطأ في تشغيل المشغل: {str(e)}")
            
    def delete_scenario(self):
        """Delete selected scenario"""
        current_item = self.scenarios_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Error", "Please select a scenario to delete\nيرجى اختيار سيناريو للحذف")
            return
            
        scenario_file = current_item.data(Qt.UserRole)
        scenario_path = os.path.join(self.scenarios_dir, scenario_file)
        
        reply = QMessageBox.question(self, "Confirm Delete", 
                                   f"Are you sure you want to delete {scenario_file}?\nهل أنت متأكد من حذف {scenario_file}؟",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                os.remove(scenario_path)
                self.load_scenarios()
                QMessageBox.information(self, "Success", "Scenario deleted successfully\nتم حذف السيناريو بنجاح")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to delete scenario: {e}\nفشل في حذف السيناريو: {e}")
                
    def add_course(self):
        """Add new course with PowerPoint file"""
        title, ok = QInputDialog.getText(
            self, 
            "New Course - درس جديد", 
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
                courses = JSONHandler.read_json(self.courses_file) or []
                new_course = {
                    "title": title,
                    "file_path": file_path,
                    "id": f"course_{random.randint(1000, 9999)}",
                    "added_date": self.get_current_date()
                }
                courses.append(new_course)
                
                if JSONHandler.write_json(self.courses_file, courses):
                    self.load_courses()
                    QMessageBox.information(
                        self, 
                        "Success", 
                        "Course added successfully!\nتم إضافة الدرس بنجاح"
                    )
                else:
                    QMessageBox.warning(
                        self, 
                        "Error", 
                        "Failed to add course\nفشل في إضافة الدرس"
                    )
            else:
                QMessageBox.warning(
                    self, 
                    "Warning", 
                    "No file selected. Course was not added.\nلم يتم اختيار ملف. لم يتم إضافة الدرس."
                )

    def edit_course(self):
        """Edit selected course title"""
        current_item = self.courses_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Error", "Please select a course to edit\nيرجى اختيار درس للتعديل")
            return
            
        course_data = current_item.data(Qt.UserRole)
        courses = JSONHandler.read_json(self.courses_file) or []
        
        # Find and update course
        for i, course in enumerate(courses):
            if course.get('id') == course_data.get('id'):
                new_title, ok = QInputDialog.getText(
                    self, 
                    "Edit Course - تعديل الدرس", 
                    "Enter new course title:\nأدخل العنوان الجديد للدرس:", 
                    text=course.get('title', '')
                )
                
                if ok and new_title:
                    courses[i]['title'] = new_title
                    if JSONHandler.write_json(self.courses_file, courses):
                        self.load_courses()
                        QMessageBox.information(
                            self, 
                            "Success", 
                            "Course updated successfully\nتم تحديث الدرس بنجاح"
                        )
                    else:
                        QMessageBox.warning(
                            self, 
                            "Error", 
                            "Failed to update course\nفشل في تحديث الدرس"
                        )
                break
                
    def set_course_file(self):
        """Set PowerPoint file for selected course"""
        current_item = self.courses_list.currentItem()
        if not current_item:
            QMessageBox.warning(
                self, 
                "Error", 
                "Please select a course first\nيرجى اختيار درس أولاً"
            )
            return
            
        course_data = current_item.data(Qt.UserRole)
        title = course_data.get('title', 'Unknown Course')
        
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self,
            f"Select PowerPoint file for: {title}\nاختر ملف الباوربوينت للدرس: {title}",
            "",
            "PowerPoint Files (*.pptx *.ppt);;All Files (*)"
        )
        
        if file_path:
            course_data['file_path'] = file_path
            self.update_course_in_file(course_data)
            QMessageBox.information(
                self,
                "Success",
                f"PowerPoint file updated successfully!\n\nتم تحديث ملف الباوربوينت بنجاح!\n\nFile: {os.path.basename(file_path)}"
            )
            self.load_courses()

    def update_course_in_file(self, updated_course):
        """Update course in JSON file"""
        courses = JSONHandler.read_json(self.courses_file) or []
        
        for i, course in enumerate(courses):
            if course.get('id') == updated_course.get('id'):
                courses[i] = updated_course
                break
                
        JSONHandler.write_json(self.courses_file, courses)
                
    def delete_course(self):
        """Delete selected course"""
        current_item = self.courses_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Error", "Please select a course to delete\nيرجى اختيار درس للحذف")
            return
            
        course_data = current_item.data(Qt.UserRole)
        courses = JSONHandler.read_json(self.courses_file) or []
        
        # Remove course
        courses = [c for c in courses if c.get('id') != course_data.get('id')]
        
        if JSONHandler.write_json(self.courses_file, courses):
            self.load_courses()
            QMessageBox.information(self, "Success", "Course deleted successfully\nتم حذف الدرس بنجاح")
        else:
            QMessageBox.warning(self, "Error", "Failed to delete course\nفشل في حذف الدرس")
            
    def clear_history(self):
        """Clear all history records"""
        reply = QMessageBox.question(self, "Confirm Clear", 
                                   "Are you sure you want to clear all history records?\nهل أنت متأكد من مسح سجل النتائج؟",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            if JSONHandler.write_json(self.history_file, []):
                self.load_history()
                QMessageBox.information(self, "Success", "History cleared successfully\nتم مسح السجل بنجاح")
            else:
                QMessageBox.warning(self, "Error", "Failed to clear history\nفشل في مسح السجل")
                
    def change_password(self):
        """Change admin password"""
        new_password, ok = QInputDialog.getText(self, "Change Password", 
                                              "Enter new password:\nأدخل كلمة المرور الجديدة:", 
                                              QLineEdit.Password)
        if ok and new_password:
            if JSONHandler.update_json(self.config_file, {"admin_password": new_password}):
                QMessageBox.information(self, "Success", "Password changed successfully\nتم تغيير كلمة المرور بنجاح")
            else:
                QMessageBox.warning(self, "Error", "Failed to change password\nفشل في تغيير كلمة المرور")

    def get_current_date(self):
        """Get current date in string format"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")