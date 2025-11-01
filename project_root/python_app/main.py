import sys
import os
from PyQt5.QtWidgets import QApplication
from windows.main_window import MainWindow

def ensure_directories_and_background():
    """Ensure all required directories and background exist"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Required directories
    directories = [
        os.path.join(current_dir, "data"),
        os.path.join(current_dir, "data", "scenarios"),
        os.path.join(current_dir, "assets"),
        os.path.join(current_dir, "assets", "backgrounds"),
        os.path.join(current_dir, "utils"),
        os.path.join(current_dir, "windows")
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    # Check if background exists
    background_path = os.path.join(current_dir, "assets", "backgrounds", "military_background.jpg")
    
def main():
    # Ensure directories and background exist
    ensure_directories_and_background()
    
    # Add the project root to Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    if project_root not in sys.path:
        sys.path.append(project_root)
    
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Interactive Tactical Training System")
    app.setApplicationVersion("1.0")
    
    # Create and show main window
    window = MainWindow()
    window.showMaximized()  # Fullscreen
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()