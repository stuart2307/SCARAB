from GUI_Screens import check_health_custom_scan
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class ch_custom_scan(QWidget):
    def __init__(self):
        super().__init__()
        
        self.ui = check_health_custom_scan.Ui_check_health_custom_scan()
        self.ui.setupUi(self)
        
    def isPinsChecked(self):
        return self.ui.test_pins_box.isChecked()
    
    def isChecksumChecked(self):
        return self.ui.checksum_box.isChecked()
    
    def isRetentionChecked(self):
        return self.ui.test_save_box.isChecked()
    
    def setImage(self, image: bytes):
        image_pixmap = QPixmap()
        image_pixmap.loadFromData(image)
        scaled = image_pixmap.scaled(self.ui.cart_image.size(),Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
        self.ui.cart_image.setPixmap(scaled)