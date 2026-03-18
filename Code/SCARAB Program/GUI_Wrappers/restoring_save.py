from GUI_Screens import save_management_restoring
from PySide6.QtWidgets import QWidget

class restoring_save(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = save_management_restoring.Ui_restoring_save()
        self.ui.setupUi(self)
        
    def restoringSetup(self, save_path: str):
        self.ui.details.setText("Please Wait...")
        self.ui.save_path.setText(save_path)
    
    def restoredSetup(self):
        self.ui.details.setText("Save Restored!")