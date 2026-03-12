from GUI_Screens import check_health_menu
from PySide6.QtWidgets import QWidget

class check_health(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = check_health_menu.Ui_check_health_menu()
        self.ui.setupUi(self)
