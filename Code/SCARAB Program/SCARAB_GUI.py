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
        self.ch_scanning = ch_in_progress()
        #self.identifying = identifying.Ui_identifying()
        #self.options = options.Ui_options()
        self.sm_save_menu = save_management()
        #self.sm_save_browse = save_management_browse_saves.Ui_browse_saves()
        self.sm_dump = dumping_save()
        self.sm_restore = restoring_save()
        self.sm_select_game = select_game()
        self.sm_select_restore = select_restore()

        self.view.addScreen(self.men_home)
        self.view.addScreen(self.mod_modules)
        self.view.addScreen(self.ch_check_health)
        #self.stack.addWidget(self.ch_custom_scan)
        self.view.addScreen(self.ch_scanning)
        #self.stack.addWidget(self.identifying)
        #self.stack.addWidget(self.options)
        self.view.addScreen(self.sm_save_menu)
        #self.stack.addWidget(self.sm_save_browse)
        self.view.addScreen(self.sm_dump)
        self.view.addScreen(self.sm_restore)
        self.view.addScreen(self.sm_select_game)
        self.view.addScreen(self.sm_select_restore)
        
        self.view.switchScreen(self.men_home)
        
    def configureButtons(self):
        self.view.ui.home_button.clicked.connect(lambda: self.view.switchScreen(self.men_home))
        self.view.ui.modules_button.clicked.connect(lambda: self.view.switchScreen(self.mod_modules))
        self.view.ui.check_health_button.clicked.connect(lambda: self.view.switchScreen(self.ch_check_health))
        self.view.ui.save_management_button.clicked.connect(lambda: self.view.switchScreen(self.sm_save_menu))
        self.sm_save_menu.ui.browse_saves_button.clicked.connect(lambda: self.view.switchScreen(self.sm_select_game))
        self.sm_save_menu.ui.dump_save_button.clicked.connect(lambda: self.view.switchScreen(self.sm_dump))
        self.sm_save_menu.ui.restore_save_button.clicked.connect(lambda: self.view.switchScreen(self.sm_select_restore))
        self.sm_select_restore.ui.restore_save_button.clicked.connect(lambda: self.view.switchScreen(self.sm_restore))
        self.ch_check_health.ui.check_health_button.clicked.connect(lambda: self.view.switchScreen(self.ch_scanning))

        self.men_home.ui.re_identify_button.clicked.connect(self.identifyScarab)

    def identifyScarab(self):
        result = self.scarab.identifyScarab()
        self.men_home.setScarabFound(result)