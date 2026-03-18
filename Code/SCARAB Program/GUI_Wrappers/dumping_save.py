from GUI_Screens import save_management_dumping
from PySide6.QtWidgets import QWidget

class dumping_save(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = save_management_dumping.Ui_dumping_save()
        self.ui.setupUi(self)
        
    def dumpingSetup(self, save_path: str):
        self.ui.details.setText("Please Wait...")
        self.ui.save_path.setText(save_path)
        
    def dumpedSetup(self):
        self.ui.details.setText("Save Dumped!")