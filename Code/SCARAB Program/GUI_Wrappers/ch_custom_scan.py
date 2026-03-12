from GUI_Screens import check_health_custom_scan
from PySide6.QtWidgets import QWidget

class ch_custom_scan(QWidget):
    def __init__(self):
        super().__init__()
        
        self.ui = check_health_custom_scan.Ui_check_health_custom_scan()
        self.ui.setupUi(self)