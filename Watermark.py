import sys
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QFileDialog, QMessageBox)
from PyQt5.QtGui import QPixmap, QFont, QImage
from PyQt5.QtCore import Qt
from PIL import Image, ImageDraw, ImageFont

#python -m PyInstaller --additional-hooks-dir=. --onefile --windowed app.py

dir_marca_daagua = ("marca_d_agua.png")

class Watermark(QWidget):
    def __init__(self):
        super().__init__()
        
        # Color Palette
        self.colors = {
            'black': '#000000',
            'deep_mauve': '#753A53',
            'soft_mauve': '#926176',
            'warm_peach': '#D6A26F',
            'light_gray': '#DEE0E3'
        }
        
        self.selected_image_path = None
        self.initUI()
        
    def initUI(self):
        # Main window setup
        self.setWindowTitle('Watermark')
        self.setGeometry(300, 300, 600, 500)
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {self.colors['light_gray']};
                font-family: Helvetica, Arial, sans-serif;
            }}
        """)
        
        # Main layout
        main_layout = QVBoxLayout()
        
        # Image Preview Label
        self.preview_label = QLabel('Select an image')
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setStyleSheet(f"""
            background-color: {self.colors['soft_mauve']};
            color: {self.colors['light_gray']};
            font-size: 16px;
            font-weight: bold;
            border-radius: 15px;
            min-height: 300px;
            margin: 20px;
        """)
        main_layout.addWidget(self.preview_label)
        
        # Button Layout
        button_layout = QHBoxLayout()
        
        # Select Image Button
        self.select_button = QPushButton('Choose Image')
        self.select_button.setStyleSheet(self.get_button_style(self.colors['deep_mauve']))
        self.select_button.clicked.connect(self.select_image)
        button_layout.addWidget(self.select_button)
        
        # Add Watermark Button
        self.watermark_button = QPushButton('Add Watermark')
        self.watermark_button.setStyleSheet(self.get_button_style(self.colors['warm_peach']))
        self.watermark_button.clicked.connect(self.add_watermark)
        self.watermark_button.setEnabled(False)  # Disabled until image is selected
        button_layout.addWidget(self.watermark_button)
        
        # Path Display
        self.path_label = QLabel('No image selected')
        self.path_label.setStyleSheet(f"""
            background-color: {self.colors['soft_mauve']};
            color: {self.colors['light_gray']};
            border-radius: 10px;
            padding: 10px;
            margin: 10px;
        """)
        self.path_label.setWordWrap(True)
        
        # Add layouts to main layout
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.path_label)
        
        # Set main layout
        self.setLayout(main_layout)
        
    def get_button_style(self, bg_color):
        """
        Generate button style dynamically
        
        Args:
        bg_color (str): Background color for the button
        
        Returns:
        str: Stylesheet for the button
        """
        return f"""
            QPushButton {{
                background-color: {bg_color};
                color: {self.colors['light_gray']};
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 10px;
                padding: 10px 20px;
            }}
            QPushButton:hover {{
                background-color: {self.colors['black']};
            }}
            QPushButton:pressed {{
                background-color: {self.colors['soft_mauve']};
            }}
            QPushButton:disabled {{
                background-color: #888888;
                color: #cccccc;
            }}
        """
        
    def select_image(self):
        """
        Open file dialog to select an image and display its preview
        
        Returns:
        str: Full path of the selected image
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select an image", 
            "", 
            "Image Files (*.png *.jpg *.jpeg *.gif *.bmp)"
        )
        
        if file_path:
            # Store the full path
            self.selected_image_path = file_path
            
            # Update path label
            self.path_label.setText(f"Selected: {file_path}")
            
            # Display image preview
            self.display_image_preview(file_path)
            
            # Enable watermark button
            self.watermark_button.setEnabled(True)
        
        return file_path
    
    def display_image_preview(self, file_path):
        """
        Display a preview of the selected image
        
        Args:
        file_path (str): Path to the image file
        """
        try:
            # Load pixmap and scale
            pixmap = QPixmap(file_path)
            scaled_pixmap = pixmap.scaled(
                400, 300, 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            
            # Update preview label
            self.preview_label.setPixmap(scaled_pixmap)
            self.preview_label.setStyleSheet(f"""
                background-color: {self.colors['deep_mauve']};
                color: {self.colors['light_gray']};
                border-radius: 15px;
                min-height: 300px;
                margin: 20px;
            """)
        
        except Exception as e:
            self.preview_label.setText(f"Error loading image: {str(e)}")
            self.preview_label.setStyleSheet(f"""
                background-color: {self.colors['black']};
                color: {self.colors['light_gray']};
                border-radius: 15px;
                min-height: 300px;
                margin: 20px;
            """)
    
    def add_watermark(self):
        """
        Add watermark to the selected image and save in a dedicated folder
        """
        if not self.selected_image_path:
            QMessageBox.warning(self, "Error", "Please select an image first.")
            return
        
        try:
            # Create 'Images with Watermark' folder in Pictures directory
            pictures_dir = os.path.join(os.path.expanduser('~'),"OneDrive", "Pictures")
            watermark_dir = os.path.join(pictures_dir, 'Images with Watermark')
            print(os.path.expanduser('~'))
            print(pictures_dir)
            print(watermark_dir)
            os.makedirs(watermark_dir, exist_ok=True)
            
            # Open the image
            image = Image.open(self.selected_image_path)
            
            image_marca_dagua = Image.open(dir_marca_daagua)

            size_total = image.size
            image_marca_dagua = image_marca_dagua.resize(size_total)

            image_com_marca = image.copy()

            image_com_marca.paste(image_marca_dagua,(0,0),image_marca_dagua)
            
            
            # Generate filename
            filename = os.path.basename(self.selected_image_path)
            name, ext = os.path.splitext(filename)
            watermarked_filename = f"{name}_watermarked{ext}"
            watermarked_path = os.path.join(watermark_dir, watermarked_filename)
            
            # Save the watermarked image
            image_com_marca.save(watermarked_path)
            
            # Show success message
            QMessageBox.information(
                self, 
                "Success", 
                f"Watermarked image saved to:\n{watermarked_path}"
            )
        
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Error", 
                f"Failed to add watermark: {str(e)}"
            )

def main():
    app = QApplication(sys.argv)
    watermark = Watermark()
    watermark.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()