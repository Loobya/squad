import os
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap, QPainter, QColor, QLinearGradient

def create_simple_background():
    """Create a simple military background image"""
    try:
        current_dir = os.path.dirname(__file__)
        assets_dir = os.path.join(current_dir, "..", "assets")
        backgrounds_dir = os.path.join(assets_dir, "backgrounds")
        
        # Create directories if they don't exist
        os.makedirs(backgrounds_dir, exist_ok=True)
        
        background_path = os.path.join(backgrounds_dir, "military_background.jpg")
        
        # Create a simple app instance (required for QPixmap)
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # Create a pixmap
        pixmap = QPixmap(1920, 1080)
        pixmap.fill(QColor(30, 63, 26))  # Fill with dark green
        
        # Create painter
        painter = QPainter(pixmap)
        
        # Draw gradient overlay
        gradient = QLinearGradient(0, 0, 1920, 1080)
        gradient.setColorAt(0.0, QColor(45, 90, 39, 200))
        gradient.setColorAt(0.5, QColor(58, 107, 52, 150))
        gradient.setColorAt(1.0, QColor(30, 63, 26, 200))
        
        painter.fillRect(0, 0, 1920, 1080, gradient)
        
        # Add grid pattern
        painter.setPen(QColor(45, 90, 39, 80))
        for x in range(0, 1920, 50):
            painter.drawLine(x, 0, x, 1080)
        for y in range(0, 1080, 50):
            painter.drawLine(0, y, 1920, y)
        
        painter.end()
        
        # Save the image
        success = pixmap.save(background_path, "JPG", 90)
        if success:
            print(f"✓ Background image created: {background_path}")
            print("You can replace this with your own military-themed image.")
        else:
            print("✗ Failed to create background image")
            
        return success
        
    except Exception as e:
        print(f"Error creating background: {e}")
        return False

if __name__ == "__main__":
    create_simple_background()