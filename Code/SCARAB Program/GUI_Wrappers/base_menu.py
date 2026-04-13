from GUI_Screens import base
from PySide6.QtWidgets import QMainWindow, QWidget, QStackedWidget

class base_menu(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = base.Ui_SCARAB_MENU()
        self.ui.setupUi(self)

        self.stack = QStackedWidget(self.ui.content_frame)
        self.stack.setGeometry(self.ui.content_frame.rect())
    
    def addScreen(self, screen):
        self.stack.addWidget(screen)
        
    def getScreen(self):
        return self.stack.currentWidget()

    def switchScreen(self, screen):
        self.stack.setCurrentWidget(screen)
        self.repaint()

    def disableHomeButton(self):
        self.ui.home_button.setDisabled(True)

    def enableHomeButton(self):
        self.ui.home_button.setDisabled(False)

    def disableModulesButton(self):
        self.ui.modules_button.setDisabled(True)

    def enableModulesButton(self):
        self.ui.modules_button.setDisabled(False)

    def disableCheckHealthButton(self):
        self.ui.check_health_button.setDisabled(True)

    def enableCheckHealthButton(self):
        self.ui.check_health_button.setDisabled(False)

    def disableSaveManagementButton(self):
        self.ui.save_management_button.setDisabled(True)

    def enableSaveManagementButton(self):
        self.ui.save_management_button.setDisabled(False)

    def disableOptionsButton(self):
        self.ui.options_button.setDisabled(True)

    def enableOptionsButton(self):
        self.ui.options_button.setDisabled(False)