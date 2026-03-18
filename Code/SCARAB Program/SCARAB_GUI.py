from time import sleep

from GUI_Wrappers import *
from SCARAB_Logic import *
from PySide6 import QtWidgets

class SCARABGUI:
    def __init__(self, view: base_menu):
        super().__init__()
        self.view = view
        self.setupScreens()
        self.populateSaveLists()
        self.configureButtons()
        self.scarab = SCARAB_Device.scarab_device()
        

    def setupScreens(self):
        self.men_home = main_menu_screen()
        self.mod_modules = module_menu()
        self.ch_check_health = check_health()
        self.ch_custom_scan = ch_custom_scan()
        self.ch_scanning = ch_in_progress()
        self.identifying = identifying_screen()
        self.options = options_menu()
        self.sm_save_menu = save_management()
        self.sm_save_browse = browse_saves()
        self.sm_dump = dumping_save()
        self.sm_restore = restoring_save()
        self.sm_select_game = select_game()
        self.sm_select_restore = select_restore()

        self.view.addScreen(self.men_home)
        self.view.addScreen(self.mod_modules)
        self.view.addScreen(self.ch_check_health)
        self.view.addScreen(self.ch_custom_scan)
        self.view.addScreen(self.ch_scanning)
        self.view.addScreen(self.identifying)
        self.view.addScreen(self.options)
        self.view.addScreen(self.sm_save_menu)
        self.view.addScreen(self.sm_save_browse)
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
        self.sm_save_menu.ui.dump_save_button.clicked.connect(self.dumpSave)
        self.sm_save_menu.ui.restore_save_button.clicked.connect(lambda: self.view.switchScreen(self.sm_select_restore))
        self.sm_select_restore.ui.restore_save_button.clicked.connect(self.restoreSave)
        self.ch_check_health.ui.check_health_button.clicked.connect(lambda: self.view.switchScreen(self.ch_scanning))
        self.ch_check_health.ui.custom_scan_button.clicked.connect(lambda: self.view.switchScreen(self.ch_custom_scan))
        self.ch_custom_scan.ui.custom_scan_button.clicked.connect(lambda: self.view.switchScreen(self.ch_scanning))
        self.sm_select_game.ui.select_game_button.clicked.connect(lambda: self.view.switchScreen(self.sm_save_browse))
        self.sm_select_game.ui.use_inserted_button.clicked.connect(lambda: self.view.switchScreen(self.sm_save_browse))
        self.view.ui.options_button.clicked.connect(lambda: self.view.switchScreen(self.options))
        self.sm_save_browse.ui.back_button.clicked.connect(lambda: self.view.switchScreen(self.sm_select_game))
        self.sm_select_game.ui.console_list.selectionModel().selectionChanged.connect(self.popGamesByConsole)
        
        self.men_home.ui.re_identify_button.clicked.connect(self.identifyScarab)

    def identifyScarab(self):
        result = self.scarab.identifyScarab()
        self.men_home.setScarabFound(result)
        #FIX THIS, HARDCODE BAD
        self.scarab.currentModule = self.scarab.modules["SNES"]
        if self.scarab.currentModule is not None:
            self.scarab.currentModule.detectCartridge(self.scarab.scarab, self.scarab.cartridge)
        self.ch_check_health.ui.name.setText(self.scarab.cartridge["name"])
        self.ch_check_health.ui.rom_size.setText(str(self.scarab.cartridge["romsize"]) + "KB")
        self.ch_check_health.ui.chipset.setText(self.scarab.cartridge["chipset"])
        self.ch_check_health.ui.checksum.setText(self.scarab.cartridge["checksum"])
        
    def dumpSave(self):
        print("A")
        location = File_Management.getNewSaveFilePath(self.scarab.currentModule.getIdString(), self.scarab.cartridge["name"])
        print("A")
        self.sm_dump.dumpingSetup(location)
        print("A")
        self.view.switchScreen(self.sm_dump)
        print("A")
        save_data = self.scarab.dumpSave()
        print("A")
        File_Management.writeSave(location, save_data)
        print("A")
        self.sm_dump.dumpedSetup()
        print("A")
        
    def restoreSave(self):
        self.sm_restore.restoringSetup()
        self.view.switchScreen(self.sm_restore)
        selected_save = self.sm_select_restore.getSelectedSave()
        save_buffer = File_Management.readSave(self.scarab.currentModule.getIdString(), self.scarab.cartridge["name"], selected_save)
        self.scarab.restoreSave(save_buffer)
        self.sm_restore.restoredSetup()
        
    def identifyModule(self):
        self.scarab.identifyModule()
        self.men_home.setModule(self.scarab.currentModule.getIdString())
        self.mod_modules.setModule(self.scarab.currentModule.getIdString())
        
    def populateSaveLists(self):
        cons = File_Management.getConsolesList()
        self.sm_select_game.populateConsoles(cons)
        
    def popGamesByConsole(self):
        console = self.sm_select_game.getCurrentConsole()
        games = File_Management.getGamesByConsole(console)
        self.sm_select_game.populateGames(games)