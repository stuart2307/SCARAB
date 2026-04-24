#SCARAB GUI Wrapper
#Copyright (C) 2026 Stuart Rossiter
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.
from GUI_Screens import check_health_menu
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class check_health(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = check_health_menu.Ui_check_health_menu()
        self.ui.setupUi(self)
        
    def setGame(self, name, romsize, chipset, checksum):
        self.ui.name.setText(name)
        self.ui.rom_size.setText(romsize)
        self.ui.chipset.setText(chipset)
        self.ui.checksum.setText(checksum)
        
    def setImage(self, image: bytes):
        image_pixmap = QPixmap()
        image_pixmap.loadFromData(image)
        scaled = image_pixmap.scaled(self.ui.cart_image.size(),Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
        self.ui.cart_image.setPixmap(scaled)