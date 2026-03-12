from GUI_Screens import save_management_select_game
from PySide6.QtWidgets import QWidget

class select_game(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = save_management_select_game.Ui_select_game()
        self.ui.setupUi(self)