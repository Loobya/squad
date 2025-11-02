"""
Assets Manager Tab for Admin Dashboard
Manages logos and squad markers
"""

import os
import shutil
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QListWidget, QListWidgetItem, QMessageBox,
                             QFileDialog, QTabWidget, QFrame, QGridLayout)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon

class AssetsManagerTab(QWidget):
    """Tab for managing logos and squad markers"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.assets_dir = os.path.join(self.current_dir, "..", "assets")
        self.logos_dir = os.path.join(self.assets_dir, "logos")
        self.markers_dir = os.path.join(self.assets_dir, "squad_markers")
        
        # Ensure directories exist
        os.makedirs(self.logos_dir, exist_ok=True)
        os.makedirs(self.markers_dir, exist_ok=True)
        
        self.init_ui()
        self.load_assets()
    
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Assets Manager - إدارة الأصول")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
                background: rgba(58, 107, 52, 0.8);
                border-radius: 5px;
            }
        """)
        layout.addWidget(title)
        
        # Create tabs for logos and markers
        tabs = QTabWidget()
        
        # Logos tab
        self.logos_tab = self.create_asset_tab("logos")
        tabs.addTab(self.logos_tab, "🖼️ Logos")
        
        # Squad markers tab
        self.markers_tab = self.create_asset_tab("markers")
        tabs.addTab(self.markers_tab, "📍 Squad Markers")
        
        layout.addWidget(tabs)
        self.setLayout(layout)
    
    def create_asset_tab(self, asset_type):
        """Create a tab for managing assets (logos or markers)"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Instructions
        if asset_type == "logos":
            instructions = QLabel(
                "📌 Logos are decorative icons that can be placed on the map.\n"
                "Supported formats: PNG, JPG, JPEG\n"
                "Recommended size: 64x64 to 256x256 pixels"
            )
            folder = self.logos_dir
        else:
            instructions = QLabel(
                "📌 Squad markers represent military units on the map.\n"
                "Supported format: PNG (with transparency)\n"
                "Recommended size: 32x32 to 64x64 pixels"
            )
            folder = self.markers_dir
        
        instructions.setStyleSheet("color: #c8e6c9; padding: 10px; font-size: 12px;")
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        upload_btn = QPushButton(f"📤 Upload {asset_type.title()}")
        delete_btn = QPushButton(f"🗑️ Delete Selected")
        open_folder_btn = QPushButton(f"📁 Open Folder")
        
        upload_btn.clicked.connect(lambda: self.upload_asset(asset_type))
        delete_btn.clicked.connect(lambda: self.delete_asset(asset_type))
        open_folder_btn.clicked.connect(lambda: self.open_folder(folder))
        
        buttons_layout.addWidget(upload_btn)
        buttons_layout.addWidget(delete_btn)
        buttons_layout.addWidget(open_folder_btn)
        
        layout.addLayout(buttons_layout)
        
        # Asset grid view
        grid_container = QFrame()
        grid_container.setStyleSheet("""
            QFrame {
                background: rgba(58, 107, 52, 0.9);
                border: 2px solid #2d5429;
                border-radius: 5px;
            }
        """)
        
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)
        grid_container.setLayout(grid_layout)
        
        # Store reference to grid
        grid_container.setObjectName(f"{asset_type}_grid")
        widget.setProperty(f"{asset_type}_grid", grid_layout)
        
        from PyQt5.QtWidgets import QScrollArea
        scroll = QScrollArea()
        scroll.setWidget(grid_container)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
        
        # Asset count label
        count_label = QLabel("0 assets")
        count_label.setStyleSheet("color: #90EE90; padding: 5px;")
        count_label.setObjectName(f"{asset_type}_count")
        layout.addWidget(count_label)
        
        widget.setLayout(layout)
        return widget
    
    def upload_asset(self, asset_type):
        """Upload a new asset (logo or marker)"""
        folder = self.logos_dir if asset_type == "logos" else self.markers_dir
        
        file_dialog = QFileDialog()
        if asset_type == "logos":
            file_filter = "Images (*.png *.jpg *.jpeg);;All Files (*)"
        else:
            file_filter = "PNG Images (*.png);;All Files (*)"
        
        file_paths, _ = file_dialog.getOpenFileNames(
            self,
            f"Select {asset_type.title()} to Upload",
            "",
            file_filter
        )
        
        if not file_paths:
            return
        
        uploaded = 0
        for file_path in file_paths:
            try:
                filename = os.path.basename(file_path)
                destination = os.path.join(folder, filename)
                
                # Check if file already exists
                if os.path.exists(destination):
                    reply = QMessageBox.question(
                        self,
                        "File Exists",
                        f"{filename} already exists. Overwrite?",
                        QMessageBox.Yes | QMessageBox.No
                    )
                    if reply == QMessageBox.No:
                        continue
                
                # Copy file
                shutil.copy2(file_path, destination)
                uploaded += 1
                
            except Exception as e:
                QMessageBox.warning(
                    self,
                    "Error",
                    f"Failed to upload {filename}: {str(e)}"
                )
        
        if uploaded > 0:
            QMessageBox.information(
                self,
                "Success",
                f"Successfully uploaded {uploaded} file(s)!"
            )
            self.load_assets()
    
    def delete_asset(self, asset_type):
        """Delete selected asset"""
        # Get selected items from grid
        # This is a simplified version - you'd track selection in practice
        QMessageBox.information(
            self,
            "Info",
            "Click on an asset thumbnail and confirm deletion.\n"
            "Feature will be enhanced in next update."
        )
    
    def open_folder(self, folder_path):
        """Open the assets folder in file explorer"""
        try:
            if os.name == 'nt':  # Windows
                os.startfile(folder_path)
            elif os.name == 'posix':  # macOS and Linux
                import subprocess
                if os.uname().sysname == 'Darwin':  # macOS
                    subprocess.call(['open', folder_path])
                else:  # Linux
                    subprocess.call(['xdg-open', folder_path])
        except Exception as e:
            QMessageBox.warning(
                self,
                "Error",
                f"Could not open folder: {str(e)}"
            )
    
    def load_assets(self):
        """Load and display all assets"""
        self.load_asset_grid("logos", self.logos_dir)
        self.load_asset_grid("markers", self.markers_dir)
    
    def load_asset_grid(self, asset_type, folder):
        """Load assets into grid view"""
        # Get the grid layout
        tab = self.logos_tab if asset_type == "logos" else self.markers_tab
        grid_container = tab.findChild(QFrame, f"{asset_type}_grid")
        if not grid_container:
            return
        
        grid_layout = grid_container.layout()
        
        # Clear existing items
        while grid_layout.count():
            child = grid_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Get all image files
        image_files = []
        if os.path.exists(folder):
            for file in os.listdir(folder):
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    image_files.append(file)
        
        # Update count
        count_label = tab.findChild(QLabel, f"{asset_type}_count")
        if count_label:
            count_label.setText(f"{len(image_files)} asset(s)")
        
        # Add thumbnails to grid
        row = 0
        col = 0
        max_cols = 4
        
        for file in image_files:
            file_path = os.path.join(folder, file)
            
            # Create thumbnail widget
            thumbnail = self.create_thumbnail(file_path, file, asset_type)
            grid_layout.addWidget(thumbnail, row, col)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        # Add stretch to push items to top
        grid_layout.setRowStretch(row + 1, 1)
    
    def create_thumbnail(self, file_path, filename, asset_type):
        """Create a thumbnail widget for an asset"""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background: white;
                border: 2px solid #3a6635;
                border-radius: 5px;
                padding: 5px;
            }
            QFrame:hover {
                border: 2px solid #5d9557;
                background: #f0f0f0;
            }
        """)
        frame.setCursor(Qt.PointingHandCursor)
        
        layout = QVBoxLayout()
        layout.setSpacing(5)
        
        # Image
        pixmap = QPixmap(file_path)
        if not pixmap.isNull():
            pixmap = pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            image_label = QLabel()
            image_label.setPixmap(pixmap)
            image_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(image_label)
        
        # Filename
        name_label = QLabel(filename)
        name_label.setStyleSheet("color: black; font-size: 10px;")
        name_label.setWordWrap(True)
        name_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(name_label)
        
        # Delete button
        delete_btn = QPushButton("🗑️")
        delete_btn.setMaximumSize(30, 30)
        delete_btn.clicked.connect(lambda: self.confirm_delete(file_path, filename, asset_type))
        layout.addWidget(delete_btn)
        
        frame.setLayout(layout)
        frame.setMaximumSize(120, 150)
        
        return frame
    
    def confirm_delete(self, file_path, filename, asset_type):
        """Confirm and delete an asset"""
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Delete {filename}?\n\nThis cannot be undone!",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                os.remove(file_path)
                QMessageBox.information(
                    self,
                    "Success",
                    f"{filename} deleted successfully!"
                )
                self.load_assets()
            except Exception as e:
                QMessageBox.warning(
                    self,
                    "Error",
                    f"Failed to delete {filename}:\n{str(e)}"
                )


# Integration code to add to existing admin_dashboard.py
def add_assets_tab_to_admin_dashboard(admin_dashboard_instance):
    """
    Add this function call in admin_dashboard.py's init_ui method:
    
    # After creating other tabs, add:
    self.assets_tab = AssetsManagerTab(self)
    self.tabs.addTab(self.assets_tab, "🖼️ Assets - الأصول")
    """
    pass