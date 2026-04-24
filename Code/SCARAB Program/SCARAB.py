#SCARAB Main
#Copyright (C) 2026 Stuart Rossiter
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.


import sys

from PySide6.QtWidgets import QApplication
import SCARAB_GUI
from GUI_Wrappers import base_menu

app = QApplication()
app.setStyle("Fusion")

window = base_menu()
controller = SCARAB_GUI.SCARABGUI(window)
window.show()

sys.exit(app.exec())