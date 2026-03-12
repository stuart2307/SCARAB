from GUI_Wrappers import *
from Logic import *
from PySide6 import QtWidgets

class SCARABGUI:
    def __init__(self, view: base_menu):
        super().__init__()
        self.view = view
        self.setupScreens()
        self.configureButtons()
        self.scarab = SCARAB_Device.scarab_device()

    def setupScreens(self):
        self.men_home = main_menu_screen()
        self.mod_modules = module_menu()
        self.ch_check_health = check_health()
        #self.ch_custom_scan = check_health_custom_scan.Ui_check_health_custom_scan()
        #self.ch_scanning = check_health_in_progress.Ui_check_health_in_progress()
        #self.identifying = identifying.Ui_identifying()
        #self.options = options.Ui_options()
        self.sm_save_menu = save_management()
        #self.sm_save_browse = save_management_browse_saves.Ui_browse_saves()
        #self.sm_dump = save_management_dumping.Ui_dumping_save()
        #self.sm_restore = save_management_restoring.Ui_restoring_save()
        #self.sm_select_game = save_management_select_game.Ui_select_game()
        #self.sm_select_save = save_management_select_restore.Ui_select_restore()

        self.view.addScreen(self.men_home)
        self.view.addScreen(self.mod_modules)
        self.view.addScreen(self.ch_check_health)
        #self.stack.addWidget(self.ch_custom_scan)
        #self.stack.addWidget(self.ch_scanning)
        #self.stack.addWidget(self.identifying)
        #self.stack.addWidget(self.options)
        self.view.addScreen(self.sm_save_menu)
        #self.stack.addWidget(self.sm_save_browse)
        #self.stack.addWidget(self.sm_dump)
        #self.stack.addWidget(self.sm_restore)
        #self.stack.addWidget(self.sm_select_game)
        #self.stack.addWidget(self.sm_select_save)
        
        self.view.switchScreen(self.men_home)
        
    def configureButtons(self):
        self.view.ui.home_button.clicked.connect(lambda: self.view.switchScreen(self.men_home))
        self.view.ui.modules_button.clicked.connect(lambda: self.view.switchScreen(self.mod_modules))
        self.view.ui.check_health_button.clicked.connect(lambda: self.view.switchScreen(self.ch_check_health))
        self.view.ui.save_management_button.clicked.connect(lambda: self.view.switchScreen(self.sm_save_menu))

        self.men_home.ui.re_identify_button.clicked.connect(self.identifyScarab)

    def identifyScarab(self):
        result = self.scarab.identifyScarab()
        self.men_home.setScarabFound(result)