#SCARAB GUI Wrapper
#Copyright (C) 2026 Stuart Rossiter
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.
from pathlib import Path
import sys

from GUI_Screens import modules_menu
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPixmap

class module_menu(QWidget):
    IMAGES_PATH = (Path(sys.executable).parent if hasattr(sys, '_MEIPASS') else Path(__file__).parent.parent) / "Images"
    
    def __init__(self):
        super().__init__()

        self.ui = modules_menu.Ui_modules_menu()
        self.ui.setupUi(self)
        
    def setModule(self, moduleName):
        self.ui.inserted_module.setText(moduleName)
        filepath = self.IMAGES_PATH / "Modules" / (moduleName + ".png")
        self.ui.mod_image.setPixmap(QPixmap(filepath))
        
    def setGame(self, gameName):
        self.ui.inserted_game.setText(gameName)