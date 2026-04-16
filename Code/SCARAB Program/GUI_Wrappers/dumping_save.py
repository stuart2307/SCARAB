from GUI_Screens import save_management_dumping
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class dumping_save(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = save_management_dumping.Ui_dumping_save()
        self.ui.setupUi(self)
        
    def dumpingSetup(self, save_path: str):
        self.ui.details.setText("Please Wait...")
        self.ui.save_path.setText(save_path)
        
    def dumpedSetup(self):
        self.ui.details.setText("Save Dumped!")
        
    def setImage(self, image: bytes):
        image_pixmap = QPixmap()
        image_pixmap.loadFromData(image)
        scaled = image_pixmap.scaled(self.ui.cart_image.size(),Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
        self.ui.cart_image.setPixmap(scaled)