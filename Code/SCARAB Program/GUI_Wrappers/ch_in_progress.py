from GUI_Screens import check_health_in_progress
from PySide6.QtWidgets import QWidget

from SCARAB_Logic.Test_Results import test_result

class ch_in_progress(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = check_health_in_progress.Ui_check_health_in_progress()
        self.ui.setupUi(self)
        
    def setupCheck(self, pins, checksum, retention):
        self.ui.test_pins.setText("In Progress..." if pins else "Not Selected.")
        self.ui.verify_checksum.setText("In Progress..." if checksum else "Not Selected.")
        self.ui.test_save_retention.setText("In Progress..." if retention else "Not Selected.")
        self.ui.identify_corruption.setText("Not Selected")
        
    def displayResults(self, results: test_result):
        self.ui.test_pins.setText("Not Selected" if results.pins_ok is None else "PASS" if results.pins_ok else "FAIL")
        self.ui.verify_checksum.setText("Not Selected" if results.checksum_ok is None else "PASS" if results.checksum_ok else "FAIL")
        self.ui.test_save_retention.setText("Not Selected" if results.retention_ok is None else "PASS" if results.retention_ok else "FAIL")
        self.ui.identify_corruption.setText("Not Selected")