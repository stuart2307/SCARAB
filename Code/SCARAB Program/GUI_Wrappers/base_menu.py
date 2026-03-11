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