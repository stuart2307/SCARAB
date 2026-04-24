#SCARAB GUI Wrapper
#Copyright (C) 2026 Stuart Rossiter
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.
from GUI_Screens import save_management_browse_saves
from PySide6.QtWidgets import QInputDialog, QWidget
from PySide6.QtCore import QStringListModel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class browse_saves(QWidget):
    def __init__(self):
        super().__init__()
        
        self.ui = save_management_browse_saves.Ui_browse_saves()
        self.ui.setupUi(self)
        self.ui.save_list
        self.current_console = None
        self.current_game = None
        
    def populateSaves(self, saves, console, game):
        self.current_console = console
        self.current_game = game
        self.ui.save_list.setModel(QStringListModel(saves))
        
    def getSelectedSave(self):
        return self.ui.save_list.currentIndex().data()
    
    def setImage(self, image: bytes):
        image_pixmap = QPixmap()
        image_pixmap.loadFromData(image)
        scaled = image_pixmap.scaled(self.ui.cart_image.size(),Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
        self.ui.cart_image.setPixmap(scaled)
        
    def allowRename(self):
        self.ui.save_list.edit(self.ui.save_list.currentIndex())