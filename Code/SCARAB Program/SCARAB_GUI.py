from time import sleep

from GUI_Wrappers import *
from SCARAB_Logic import *
from PySide6 import QtWidgets
import threading
from PySide6.QtCore import QMetaObject, Qt, Signal

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
        
        self.men_home.setScarabFound(False)
        self.men_home.setModule("NONE")
        self.mod_modules.setModule("NONE")
        self.ch_scanning.ui.unplug_label.setVisible(False)
        self.ch_scanning.ui.ok_button.setVisible(False)
        self.view.switchScreen(self.men_home)
        
    def configureButtons(self):
        self.view.ui.home_button.clicked.connect(lambda: self.view.switchScreen(self.men_home))
        self.view.ui.modules_button.clicked.connect(lambda: self.view.switchScreen(self.mod_modules))
        self.view.ui.check_health_button.clicked.connect(lambda: self.view.switchScreen(self.ch_check_health))
        self.view.ui.save_management_button.clicked.connect(lambda: self.view.switchScreen(self.sm_save_menu))
        self.men_home.ui.view_module_button.clicked.connect(lambda: self.view.switchScreen(self.mod_modules))
        self.mod_modules.ui.identify_module_button.clicked.connect(self.identifyModule)
        self.sm_save_menu.ui.browse_saves_button.clicked.connect(lambda: self.view.switchScreen(self.sm_select_game))
        self.sm_save_menu.ui.dump_save_button.clicked.connect(self.dumpSave)
        self.sm_save_menu.ui.restore_save_button.clicked.connect(self.switchRestore)
        self.sm_select_restore.ui.restore_save_button.clicked.connect(self.restoreSave)
        self.ch_check_health.ui.check_health_button.clicked.connect(self.checkHealth)
        self.ch_check_health.ui.custom_scan_button.clicked.connect(lambda: self.view.switchScreen(self.ch_custom_scan))
        self.ch_custom_scan.ui.custom_scan_button.clicked.connect(lambda: self.checkHealth(True))
        self.sm_select_game.ui.select_game_button.clicked.connect(self.prepSaveManager)
        self.sm_select_game.ui.use_inserted_button.clicked.connect(lambda: self.view.switchScreen(self.sm_save_browse))
        self.view.ui.options_button.clicked.connect(lambda: self.view.switchScreen(self.options))
        self.sm_save_browse.ui.back_button.clicked.connect(lambda: self.view.switchScreen(self.sm_select_game))
        self.sm_select_game.ui.console_list.selectionModel().selectionChanged.connect(self.popGamesByConsole)
        
        self.men_home.ui.re_identify_button.clicked.connect(self.identifyScarab)

    def identifyScarab(self):
        prev_screen = self.view.getScreen()
        self.view.switchScreen(self.identifying)
        result = self.scarab.identifyScarab()
        self.men_home.setScarabFound(result)
        if result:
            self.identifyModule()
            if self.scarab.currentModule is not None and result:
                self.scarab.currentModule.detectCartridge(self.scarab.scarab, self.scarab.cartridge)
                print(self.scarab.cartridge)
                self.ch_check_health.ui.name.setText(self.scarab.cartridge["name"])
                self.ch_check_health.ui.rom_size.setText(str(self.scarab.cartridge["romsize"]) + "KB")
                self.ch_check_health.ui.chipset.setText(self.scarab.cartridge["chipset"])
                self.ch_check_health.ui.checksum.setText(self.scarab.cartridge["checksum"])
            else:
                self.men_home.setModule("NONE")
                self.mod_modules.setModule("NONE")
        else:
            self.men_home.setModule("NONE")
            self.mod_modules.setModule("NONE")
        self.view.switchScreen(prev_screen)
        
    def dumpSave(self):
        location = File_Management.getNewSaveFilePath(self.scarab.currentModule.getIdString(), self.scarab.cartridge["name"])
        self.sm_dump.dumpingSetup(location)
        self.view.switchScreen(self.sm_dump)
        save_data = self.scarab.dumpSave()
        File_Management.writeSave(location, save_data)
        self.sm_dump.dumpedSetup()
        
    def switchRestore(self):
        saves = File_Management.getSavesByGame(self.scarab.currentModule.getIdString(), self.scarab.cartridge["name"])
        self.sm_select_restore.populateSaves(saves)
        self.view.switchScreen(self.sm_select_restore)
        
    def restoreSave(self):
        selected_save = self.sm_select_restore.getSelectedSave()
        location = File_Management.getExistingSaveFilePath(self.scarab.currentModule.getIdString(), self.scarab.cartridge["name"], selected_save)
        self.sm_restore.restoringSetup(location)
        self.view.switchScreen(self.sm_restore)
        save_buffer = File_Management.readSave(self.scarab.currentModule.getIdString(), self.scarab.cartridge["name"], selected_save)
        self.scarab.restoreSave(save_buffer)
        self.sm_restore.restoredSetup()
        
    def identifyModule(self):
        try:
            self.scarab.identifyModule()
            if self.scarab.currentModule is not None:
                self.men_home.setModule(self.scarab.currentModule.getIdString())
                self.mod_modules.setModule(self.scarab.currentModule.getIdString())
            else:
                self.men_home.setModule("NONE")
                self.mod_modules.setModule("NONE")
        except:
            self.men_home.setModule("NONE")
            self.mod_modules.setModule("NONE")
        
    def populateSaveLists(self):
        cons = File_Management.getConsolesList()
        self.sm_select_game.populateConsoles(cons)
        
    def popGamesByConsole(self):
        console = self.sm_select_game.getCurrentConsole()
        games = File_Management.getGamesByConsole(console)
        self.sm_select_game.populateGames(games)
        
    def prepSaveManager(self):
        console = self.sm_select_game.getCurrentConsole()
        game = self.sm_select_game.getCurrentGame()
        saves = File_Management.getSavesByGame(console, game)
        self.sm_save_browse.populateSaves(saves, console)
        self.view.switchScreen(self.sm_save_browse)
        
    def checkHealth(self, custom=False):
        if custom:
            pins = self.ch_custom_scan.isPinsChecked()
            checksum = self.ch_custom_scan.isChecksumChecked()
            retention = self.ch_custom_scan.isRetentionChecked()
            self.ch_scanning.setupCheck(pins, checksum, retention)
        else:
            pins = True
            checksum = True
            retention = True
            self.ch_scanning.setupCheck(pins, checksum, retention)
        self.view.switchScreen(self.ch_scanning)
        if pins:
            pin_result = self.scarab.testPins()
            self.ch_scanning.displayResults("pins", pin_result)
            self.view.repaint()
        if checksum:
            checksum_result = self.scarab.calcChecksum()
            self.ch_scanning.displayResults("checksum", checksum_result)
            self.view.repaint()
        if retention:
            self.ch_scanning.ui
        #results = self.scarab.checkHealth(pins, checksum, retention)
        #self.ch_scanning.displayResults(results)
        
    def deleteSave(self):
        toDelete = self.sm_save_browse.getSelectedSave()
        console = self.sm_save_browse.current_console
        File_Management.deleteSave(toDelete, console)
        