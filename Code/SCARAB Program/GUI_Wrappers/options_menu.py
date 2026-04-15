from GUI_Screens import options
from PySide6.QtWidgets import QWidget

class options_menu(QWidget):
    def __init__(self):
        super().__init__()
        
        self.ui = options.Ui_options()
        self.ui.setupUi(self)
        
    def populateSettings(self, settings: dict):
        self.ui.api_key.setText(settings["API"]["gamesdbapikey"])
        self.ui.auto_id_box.setChecked(settings["SCARAB"]["autoid"] == 'yes')
        
    def getSettings(self):
        settings = {"API": {"gamesdbapikey": self.ui.api_key.text()}, "SCARAB": {"autoid": 'yes' if self.ui.auto_id_box.isChecked() else 'no'}}
        return settings