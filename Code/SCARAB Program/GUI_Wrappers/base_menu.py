#SCARAB GUI Wrapper
#Copyright (C) 2026 Stuart Rossiter
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.
from GUI_Screens import base
from PySide6.QtWidgets import QMainWindow, QWidget, QStackedWidget
from PySide6.QtCore import QTimer

class base_menu(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = base.Ui_SCARAB_MENU()
        self.ui.setupUi(self)
        self.ui.message_banner.setVisible(False)

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
        
    def disableButtons(self):
        self.disableCheckHealthButton()
        self.disableHomeButton()
        self.disableModulesButton()
        self.disableOptionsButton()
        self.disableSaveManagementButton()
        
    def enableButtons(self):
        self.enableCheckHealthButton()
        self.enableHomeButton()
        self.enableModulesButton()
        self.enableOptionsButton()
        self.enableSaveManagementButton() 
        
    def displayMessage(self, message: str, is_error: bool = False):
        self.ui.message.setText(("ERROR: " if is_error else "") + message)
        self.ui.message_banner.setVisible(True)
        QTimer.singleShot(5000, lambda: self.ui.message_banner.setVisible(False))