from ..GUI_Screens import identifying
from PySide6.QtWidgets import QWidget

class identifying_screen(QWidget):
    def __init__(self):
        super.__init__()

        self.ui = identifying.Ui_identifying()
        self.ui.setupUi(self)