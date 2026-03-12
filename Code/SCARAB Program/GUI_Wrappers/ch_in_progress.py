from GUI_Screens import check_health_in_progress
from PySide6.QtWidgets import QWidget

class ch_in_progress(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = check_health_in_progress.Ui_check_health_in_progress()
        self.ui.setupUi(self)