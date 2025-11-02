import os
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QListWidget, QListWidgetItem,
                             QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from utils.json_handler import JSONHandler
from utils.process_launcher import ProcessLauncher

class PracticeWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(self.current_dir, "..", "data")
        self.scenarios_dir = os.path.join(self.data_dir, "scenarios")
        
        self.process_launcher = ProcessLauncher(
            os.path.join(os.path.dirname(self.current_dir), "..", "java_app")
        )
        
        self.init_ui()
        self.load_scenarios()
        
    def init_ui(self):
        self.setWindowTitle("تمرين - Practice Mode")
        self.setGeometry(100, 100, 800, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Title
        title = QLabel("وضع التمرين - اختر سيناريو للتدريب")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 18, QFont.Bold))
        layout.addWidget(title)
        
        # Scenarios list
        self.scenarios_list = QListWidget()
        self.scenarios_list.itemDoubleClicked.connect(self.play_scenario)
        layout.addWidget(self.scenarios_list)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        self.play_btn = QPushButton("تشغيل السيناريو")
        self.back_btn = QPushButton("رجوع")
        
        self.play_btn.clicked.connect(self.play_selected_scenario)
        self.back_btn.clicked.connect(self.close)
        
        buttons_layout.addWidget(self.play_btn)
        buttons_layout.addWidget(self.back_btn)
        
        layout.addLayout(buttons_layout)
        
    def load_scenarios(self):
        """Load available scenarios"""
        self.scenarios_list.clear()
        if not os.path.exists(self.scenarios_dir):
            os.makedirs(self.scenarios_dir, exist_ok=True)
            QMessageBox.information(self, "Info", "No scenarios found. Please add scenarios in admin mode.")
            return
            
        scenario_files = []
        for file in os.listdir(self.scenarios_dir):
            if file.endswith('.json'):
                scenario_files.append(file)
                
        if not scenario_files:
            QMessageBox.information(self, "Info", "No scenarios found. Please add scenarios in admin mode.")
            return
            
        for file in scenario_files:
            scenario_path = os.path.join(self.scenarios_dir, file)
            scenario_data = JSONHandler.read_json(scenario_path)
            if scenario_data:
                item = QListWidgetItem(scenario_data.get('title', file))
                item.setData(Qt.UserRole, file)
                self.scenarios_list.addItem(item)
                
    def play_selected_scenario(self):
        """Play the selected scenario"""
        current_item = self.scenarios_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Error", "Please select a scenario to play")
            return
            
        self.play_scenario(current_item)
        
    def play_scenario(self, item):
        """Play the scenario"""
        scenario_file = item.data(Qt.UserRole)
        scenario_path = os.path.join(self.scenarios_dir, scenario_file)
        
        success = self.process_launcher.launch_scenario_player(scenario_path, "practice")
        if not success:
            QMessageBox.warning(self, "Error", "Failed to launch scenario player")