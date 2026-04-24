#SCARAB GUI Wrapper
#Copyright (C) 2026 Stuart Rossiter
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.
from GUI_Screens import identifying
from PySide6.QtWidgets import QWidget

class identifying_screen(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = identifying.Ui_identifying()
        self.ui.setupUi(self)