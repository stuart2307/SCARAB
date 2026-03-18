from GUI_Screens import save_management_select_restore
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QStringListModel

class select_restore(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = save_management_select_restore.Ui_select_restore()
        self.ui.setupUi(self)
        
    def populateSaves(self, saves):
        self.ui.save_list.setModel(QStringListModel(saves))
        
    def getSelectedSave(self):
        return self.ui.save_list.currentIndex().data()