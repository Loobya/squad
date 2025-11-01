import os
import random
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QProgressBar, QMessageBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

from utils.json_handler import JSONHandler
from utils.process_launcher import ProcessLauncher
from windows.results_window import ResultsWindow

class TestWindow(QMainWindow):
    def __init__(self, user_name, user_id, parent=None):
        super().__init__(parent)
        self.user_name = user_name
        self.user_id = user_id
        self.parent = parent
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(self.current_dir, "..", "data")
        self.scenarios_dir = os.path.join(self.data_dir, "scenarios")
        self.history_file = os.path.join(self.data_dir, "history.json")
        self.temp_result_file = os.path.join(self.data_dir, "temp_result.json")
        
        self.process_launcher = ProcessLauncher(
            os.path.join(os.path.dirname(self.current_dir), "..", "java_app")
        )
        
        self.current_scenario_index = 0
        self.scenarios_to_play = []
        self.user_answers = []
        self.total_scenarios = 0
        
        self.init_ui()
        self.prepare_test()
        
    def init_ui(self):
        self.setWindowTitle("اختبار - Test Mode")
        self.setGeometry(100, 100, 800, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # User info
        user_info = QLabel(f"المستخدم: {self.user_name} - الرقم: {self.user_id}")
        user_info.setAlignment(Qt.AlignCenter)
        user_info.setFont(QFont("Arial", 14))
        layout.addWidget(user_info)
        
        # Progress
        self.progress_label = QLabel("جاري تحضير الاختبار...")
        self.progress_label.setAlignment(Qt.AlignCenter)
        self.progress_label.setFont(QFont("Arial", 16))
        layout.addWidget(self.progress_label)
        
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)
        
        # Status
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Start button
        self.start_btn = QPushButton("بدء الاختبار")
        self.start_btn.clicked.connect(self.start_next_scenario)
        self.start_btn.setMinimumHeight(50)
        self.start_btn.setFont(QFont("Arial", 16))
        layout.addWidget(self.start_btn)
        
    def prepare_test(self):
        """Prepare random scenarios for the test"""
        # Get all available scenarios
        scenario_files = []
        if os.path.exists(self.scenarios_dir):
            for file in os.listdir(self.scenarios_dir):
                if file.endswith('.json'):
                    scenario_files.append(file)
        
        if not scenario_files:
            QMessageBox.warning(self, "Error", "No scenarios found! Please add scenarios first.")
            self.close()
            return
            
        # Select 3-4 random scenarios
        num_scenarios = min(random.randint(3, 4), len(scenario_files))
        self.scenarios_to_play = random.sample(scenario_files, num_scenarios)
        self.total_scenarios = len(self.scenarios_to_play)
        
        self.progress_label.setText(f"الاختبار سيتضمن {self.total_scenarios} سيناريوهات")
        self.progress_bar.setMaximum(self.total_scenarios)
        self.progress_bar.setValue(0)
        self.status_label.setText("جاهز للبدء")
        
    def start_next_scenario(self):
        """Start the next scenario in the test"""
        if self.current_scenario_index >= len(self.scenarios_to_play):
            self.finish_test()
            return
            
        self.start_btn.setEnabled(False)
        scenario_file = self.scenarios_to_play[self.current_scenario_index]
        scenario_path = os.path.join(self.scenarios_dir, scenario_file)
        
        # Update progress
        self.progress_label.setText(f"السيناريو {self.current_scenario_index + 1} من {self.total_scenarios}")
        self.progress_bar.setValue(self.current_scenario_index + 1)
        self.status_label.setText("جاري تشغيل السيناريو...")
        
        # Launch Java player
        success = self.process_launcher.launch_scenario_player(scenario_path, "test")
        if not success:
            QMessageBox.warning(self, "Error", "Failed to launch scenario player")
            self.start_btn.setEnabled(True)
            return
            
        # Start checking for result
        self.check_result_timer = QTimer()
        self.check_result_timer.timeout.connect(self.check_scenario_result)
        self.check_result_timer.start(1000)  # Check every second
        
    def check_scenario_result(self):
        """Check if scenario result is available"""
        result = self.process_launcher.get_scenario_result(self.temp_result_file)
        if result:
            self.check_result_timer.stop()
            self.user_answers.append(result)
            self.current_scenario_index += 1
            self.status_label.setText("تم الانتهاء من السيناريو")
            self.start_btn.setEnabled(True)
            self.start_btn.setText("السيناريو التالي" if self.current_scenario_index < self.total_scenarios else "إنهاء الاختبار")
            
    def finish_test(self):
        """Calculate results and show results window"""
        # Calculate score
        correct_answers = sum(1 for answer in self.user_answers if answer.get('correct', False))
        total_questions = len(self.user_answers)
        score_percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
        
        # Create result record
        result_record = {
            "user_id": self.user_id,
            "name": self.user_name,
            "score": round(score_percentage),
            "right": correct_answers,
            "wrong": total_questions - correct_answers,
            "date": self.get_current_date(),
            "scenarios_played": len(self.scenarios_to_play)
        }
        
        # Save to history
        self.save_to_history(result_record)
        
        # Show results
        self.results_window = ResultsWindow(result_record, self.parent)
        self.results_window.show()
        self.close()
        
    def save_to_history(self, result_record):
        """Save test result to history"""
        history = JSONHandler.read_json(self.history_file) or []
        history.append(result_record)
        JSONHandler.write_json(self.history_file, history)
        
    def get_current_date(self):
        """Get current date in string format"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")