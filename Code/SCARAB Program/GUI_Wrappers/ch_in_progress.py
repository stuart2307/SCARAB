from GUI_Screens import check_health_in_progress
from PySide6.QtWidgets import QWidget

class ch_in_progress(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = check_health_in_progress.Ui_check_health_in_progress()
        self.ui.setupUi(self)
        
    def setupCheck(self, pins, checksum, retention):
        self.ui.complete_label.setVisible(False)
        self.ui.ok_button_done.setVisible(False)
        self.ui.unplug_label.setVisible(False)
        self.ui.ok_button_pre.setVisible(False)
        self.ui.ok_button_post.setVisible(False)
        self.ui.replug_label.setVisible(False)
        self.ui.unplug_label.setVisible(False)
        self.ui.warning_label.setVisible(True)
        self.ui.dyk_label.setVisible(True)
        self.ui.didyouknow.setVisible(True)
        
        self.ui.test_pins.setText("In Progress..." if pins else "Not Selected.")
        self.ui.verify_checksum.setText("In Progress..." if checksum else "Not Selected.")
        self.ui.test_save_retention.setText("In Progress..." if retention else "Not Selected.")
        self.ui.identify_corruption.setText("Not Selected")
        
    def popFact(self, fact: str):
        self.ui.didyouknow.setText(fact)
        
    def preRetentionNoticeSetup(self):
        self.ui.ok_button_pre.setVisible(True)
        self.ui.unplug_label.setVisible(True)
        self.ui.warning_label.setVisible(False)
        self.ui.dyk_label.setVisible(False)
        self.ui.didyouknow.setVisible(False)
        
    def preRetentionNoticeAcknowledged(self):
        self.ui.test_save_retention.setText("Power Cycling...")
        self.ui.ok_button_pre.setVisible(False)
        self.ui.unplug_label.setVisible(False)
        self.ui.warning_label.setVisible(True)
        self.ui.dyk_label.setVisible(True)
        self.ui.didyouknow.setVisible(True)
        
    def postRetentionNoticeSetup(self):
        self.ui.ok_button_post.setVisible(True)
        self.ui.replug_label.setVisible(True)
        self.ui.warning_label.setVisible(False)
        self.ui.dyk_label.setVisible(False)
        self.ui.didyouknow.setVisible(False)
    
    def postRetentionNoticeAcknowledged(self):
        self.ui.test_save_retention.setText("Testing Save...")
        self.ui.ok_button_post.setVisible(False)
        self.ui.replug_label.setVisible(False)
        self.ui.warning_label.setVisible(True)
        self.ui.dyk_label.setVisible(True)
        self.ui.didyouknow.setVisible(True)
        
    def checksDone(self):
        self.ui.warning_label.setVisible(False)
        self.ui.dyk_label.setVisible(False)
        self.ui.didyouknow.setVisible(False)
        self.ui.complete_label.setVisible(True)
        self.ui.ok_button_done.setVisible(True)
        pass
        
    def displayResults(self, type, result, comment=None):
        if type == "pins":
            self.ui.test_pins.setText("Not Selected" if result is None else "PASS" if result else "FAIL")
        elif type == "checksum":
            self.ui.verify_checksum.setText("Not Selected" if result is None else "PASS" if result else "FAIL")
        elif type == "retention":
            self.ui.test_save_retention.setText("Not Selected" if result is None else comment)
        else:
            self.ui.identify_corruption.setText("Not Selected")