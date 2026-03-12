from GUI_Screens import save_management_select_restore
from PySide6.QtWidgets import QWidget

class select_restore(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = save_management_select_restore.Ui_select_restore()
        self.ui.setupUi(self)