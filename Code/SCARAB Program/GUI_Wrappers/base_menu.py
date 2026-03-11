from ..GUI_Screens import base
from PySide6.QtWidgets import QWidget, QStackedWidget

class base_menu(QWidget):
    def __init__(self):
        super.__init__()

        self.ui = base.Ui_SCARAB_MENU()
        self.ui.setupUi(self)

        self.stack = QStackedWidget(self.ui.content_frame)
        self.stack.setGeometry(self.ui.content_frame.rect())
    
    def add_screen(self, screen):
        self.stack.addWidget(screen)

    def switch_screen(self, screen):
        self.stack.setCurrentWidget(screen)

    def disable_home_button(self):
        self.ui.home_button.setDisabled(True)

    def enable_home_button(self):
        self.ui.home_button.setDisabled(False)

    def disable_modules_button(self):
        self.ui.modules_button.setDisabled(True)

    def enable_modules_button(self):
        self.ui.modules_button.setDisabled(False)

    def disable_check_health_button(self):
        self.ui.check_health_button.setDisabled(True)

    def enable_check_health_button(self):
        self.ui.check_health_button.setDisabled(False)

    def disable_save_management_button(self):
        self.ui.save_management_button.setDisabled(True)

    def enable_save_management_button(self):
        self.ui.save_management_button.setDisabled(False)

    def disable_options_button(self):
        self.ui.options_button.setDisabled(True)

    def enable_options_button(self):
        self.ui.options_button.setDisabled(False)