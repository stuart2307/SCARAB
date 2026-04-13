from GUI_Screens import save_management_select_game
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QStringListModel

class select_game(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = save_management_select_game.Ui_select_game()
        self.ui.setupUi(self)
        
    def populateConsoles(self, consoles: list):
        self.ui.console_list.setModel(QStringListModel(consoles))
        
    def populateGames(self, games: list):
        self.ui.save_list.setModel(QStringListModel(games))
        
    def getCurrentConsole(self):
        return self.ui.console_list.currentIndex().data()
    
    def getCurrentGame(self):
        return self.ui.save_list.currentIndex().data()