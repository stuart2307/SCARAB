from GUI_Screens import save_management_browse_saves
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QStringListModel

class browse_saves(QWidget):
    def __init__(self):
        super().__init__()
        
        self.ui = save_management_browse_saves.Ui_browse_saves()
        self.ui.setupUi(self)
        self.ui.save_list
        self.current_console = None
        self.current_game = None
        
    def populateSaves(self, saves, console):
        self.current_console = console
        self.ui.save_list.setModel(QStringListModel(saves))
        
    def getSelectedSave(self):
        return self.ui.save_list.currentIndex().data()