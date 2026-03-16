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