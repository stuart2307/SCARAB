import random

from GUI_Wrappers import *
from SCARAB_Logic import *
from PySide6.QtCore import QTimer, Qt

class SCARABGUI:
    def __init__(self, view: base_menu):
        super().__init__()
        self.view = view
        self.game_image_manager = Game_Imagery()
        self.setupScreens()
        self.populateSaveLists()
        self.configureButtons()
        self.getSettings()
        self.scarab = SCARAB_Device.scarab_device()
        if self.settings["SCARAB"]["autoid"] == 'yes':
            QTimer.singleShot(100, self.identifyScarab)

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
        self.view.switchScreen(self.men_home)
        
    def configureButtons(self):
        self.view.ui.home_button.clicked.connect(lambda: self.view.switchScreen(self.men_home))
        self.view.ui.modules_button.clicked.connect(lambda: self.view.switchScreen(self.mod_modules))
        self.view.ui.check_health_button.clicked.connect(lambda: self.view.switchScreen(self.ch_check_health))
        self.view.ui.save_management_button.clicked.connect(lambda: self.view.switchScreen(self.sm_save_menu))
        self.men_home.ui.view_module_button.clicked.connect(lambda: self.view.switchScreen(self.mod_modules))
        self.mod_modules.ui.identify_module_button.clicked.connect(self.identifyModule)
        self.mod_modules.ui.identify_cart_button.clicked.connect(self.detectCartridge)
        self.sm_save_menu.ui.browse_saves_button.clicked.connect(lambda: self.view.switchScreen(self.sm_select_game))
        self.sm_save_menu.ui.dump_save_button.clicked.connect(self.dumpSave)
        self.sm_save_menu.ui.restore_save_button.clicked.connect(self.switchRestore)
        self.sm_select_restore.ui.restore_save_button.clicked.connect(self.restoreSave)
        self.ch_check_health.ui.check_health_button.clicked.connect(self.checkHealth)
        self.ch_check_health.ui.custom_scan_button.clicked.connect(lambda: self.view.switchScreen(self.ch_custom_scan))
        self.ch_custom_scan.ui.custom_scan_button.clicked.connect(lambda: self.checkHealth(True))
        self.sm_select_game.ui.select_game_button.clicked.connect(self.prepSaveManager)
        self.sm_select_game.ui.use_inserted_button.clicked.connect(lambda: self.prepSaveManager(True))
        self.view.ui.options_button.clicked.connect(lambda: self.view.switchScreen(self.options))
        self.sm_save_browse.ui.back_button.clicked.connect(lambda: self.view.switchScreen(self.sm_select_game))
        self.sm_select_game.ui.console_list.selectionModel().selectionChanged.connect(self.popGamesByConsole)
        self.ch_scanning.ui.ok_button_pre.clicked.connect(self.saveRetentionPreWait)
        self.ch_scanning.ui.ok_button_post.clicked.connect(self.saveRetentionFinal)
        self.ch_scanning.ui.ok_button_done.clicked.connect(lambda: self.view.switchScreen(self.ch_check_health))
        self.sm_save_browse.ui.delete_button.clicked.connect(self.deleteSave)
        self.men_home.ui.re_identify_button.clicked.connect(self.identifyScarab)
        self.options.ui.save_settings.clicked.connect(self.saveSettings)
        self.options.ui.cancel_changes.clicked.connect(self.getSettings)
        self.options.ui.write_to_eeprom.clicked.connect(self.writeEEPROM)
        self.sm_save_browse.ui.rename_button.clicked.connect(self.allowRename)
        self.sm_save_browse.ui.save_list.itemDelegate().commitData.connect(self.renameSave)

    def identifyScarab(self):
        prev_screen = self.view.getScreen()
        self.view.switchScreen(self.identifying)
        result = self.scarab.identifyScarab()
        self.men_home.setScarabFound(result)
        if result:
            self.identifyModule()
        else:
            self.view.displayMessage("SCARAB not found.", is_error=True)
            self.men_home.setModule("NONE")
            self.mod_modules.setModule("NONE")
            self.mod_modules.setGame("NONE")
            self.ch_check_health.setGame("N/A", "0KB", "N/A", "N/A")
        self.view.switchScreen(prev_screen)
        
    def detectCartridge(self):
        self.scarab.cartridge.clear()
        if self.scarab.currentModule is not None:
            if self.scarab.currentModule.detectCartridge(self.scarab.scarab, self.scarab.cartridge):
                print(self.scarab.cartridge)
                name = self.scarab.cartridge.get("name", "N/A")
                romsize = self.scarab.cartridge.get("romsize", 0)
                chipset = self.scarab.cartridge.get("chipset", "N/A")
                checksum = self.scarab.cartridge.get("checksum", "N/A")
                image = self.game_image_manager.getImageByName(self.scarab.cartridge.get("name", "N/A"), self.scarab.currentModule.getIdString())
                if image is not None:
                    self.setImages(image)
                self.mod_modules.setGame(name)
                self.ch_check_health.setGame(name, romsize, chipset, checksum)
                self.sm_select_game.setDetectedGame(name)
        else:
            self.view.displayMessage("Cannot identify Cartridge with no Module inserted.", is_error=True)
            self.ch_check_health.ui.cart_image.setPixmap(None)
            self.mod_modules.setGame("NONE")
            self.ch_check_health.setGame("N/A", "0KB", "N/A", "N/A")
    
    def setImages(self, image):
        self.ch_custom_scan.setImage(image)
        self.ch_check_health.setImage(image)
        self.ch_scanning.setImage(image)
        self.sm_dump.setImage(image)
        self.sm_restore.setImage(image)
        self.sm_save_menu.setImage(image)
        self.sm_select_restore.setImage(image)
        
    def writeEEPROM(self):
        string = self.options.getEEPROMValue()
        self.scarab.writeEeprom(string)
        self.view.displayMessage("EEPROM Written.")
    
    def dumpSave(self):
        if not self.cartSafetyCheck():
            return
        if self.scarab.cartridge.get("saveexp", 0) == 0:
            self.view.displayMessage("Cartridge does not support save files.", is_error=True)
            return
        self.view.disableButtons()
        location = File_Management.getNewSaveFilePath(self.scarab.currentModule.getIdString(), self.scarab.cartridge.get("name", "N/A"))
        self.sm_dump.dumpingSetup(location)
        self.view.switchScreen(self.sm_dump)
        save_data = self.scarab.dumpSave()
        File_Management.writeSave(location, save_data)
        self.sm_dump.dumpedSetup()
        self.view.enableButtons()
        
    def switchRestore(self):
        if not self.cartSafetyCheck():
            return
        if self.scarab.cartridge.get("saveexp", 0) == 0:
            self.view.displayMessage("Cartridge does not support save files.", is_error=True)
            return
        saves = File_Management.getSavesByGame(self.scarab.currentModule.getIdString(), self.scarab.cartridge.get("name", "N/A"))
        self.sm_select_restore.populateSaves(saves)
        self.view.switchScreen(self.sm_select_restore)
        
    def restoreSave(self):
        self.view.disableButtons()
        selected_save = self.sm_select_restore.getSelectedSave()
        location = File_Management.getExistingSaveFilePath(self.scarab.currentModule.getIdString(), self.scarab.cartridge.get("name", "N/A"), selected_save)
        self.sm_restore.restoringSetup(location)
        self.view.switchScreen(self.sm_restore)
        save_buffer = File_Management.readSave(self.scarab.currentModule.getIdString(), self.scarab.cartridge.get("name", "N/A"), selected_save)
        self.scarab.restoreSave(save_buffer)
        self.sm_restore.restoredSetup()
        self.view.enableButtons()
        
    def allowRename(self):
        self.old_save = self.sm_save_browse.getSelectedSave()
        self.sm_save_browse.allowRename()
        
    def renameSave(self):
        save = self.sm_save_browse.getSelectedSave()
        File_Management.renameSave(self.sm_save_browse.current_console, self.sm_save_browse.current_game, self.old_save, save)
        self.view.displayMessage("Save Renamed.")
        console = self.sm_save_browse.current_console
        game = self.sm_save_browse.current_game
        saves = File_Management.getSavesByGame(console, game)
        self.sm_save_browse.populateSaves(saves, console, game)
        
    def identifyModule(self):
        try:
            self.scarab.identifyModule()
            if self.scarab.currentModule is not None:
                self.men_home.setModule(self.scarab.currentModule.getIdString())
                self.mod_modules.setModule(self.scarab.currentModule.getIdString())
                self.view.repaint()
            else:
                self.men_home.setModule("NONE")
                self.mod_modules.setModule("NONE")
        except:
            self.men_home.setModule("NONE")
            self.mod_modules.setModule("NONE")
            self.view.repaint()
        try:
            self.detectCartridge()
        except Exception as e:
            print(e.args)
            pass
        
    def populateSaveLists(self):
        cons = File_Management.getConsolesList()
        self.sm_select_game.populateConsoles(cons)
        
    def popGamesByConsole(self):
        console = self.sm_select_game.getCurrentConsole()
        games = File_Management.getGamesByConsole(console)
        self.sm_select_game.populateGames(games)
        
    def prepSaveManager(self, inserted: bool = False):
        if not inserted:
            console = self.sm_select_game.getCurrentConsole()
            game = self.sm_select_game.getCurrentGame()
            if game is None or console is None:
                self.view.displayMessage("Game not selected.", is_error=True)
                return
            saves = File_Management.getSavesByGame(console, game)
            self.sm_save_browse.populateSaves(saves, console, game)
            self.sm_save_browse.current_console = console
            self.sm_save_browse.current_game = game
        else:
            if not self.cartSafetyCheck():
                return
            if self.scarab.cartridge.get("saveexp", 0) == 0:
                self.view.displayMessage("Cartridge does not support save files.", is_error=True)
                return
            console = self.scarab.currentModule.getIdString()
            game = self.scarab.cartridge.get("name", "N/A")
            saves = File_Management.getSavesByGame(console, game)
            self.sm_save_browse.populateSaves(saves, console, game)
        img = self.game_image_manager.getImageByName(game, console)
        self.sm_save_browse.setImage(img)
        self.view.switchScreen(self.sm_save_browse)
        
    def checkHealth(self, custom=False):
        if "name" not in self.scarab.cartridge.keys():
            self.view.displayMessage("Cannot run Health Check with no Cartridge.", is_error=True)
            return
        fact_file = open("didyouknow.txt")
        self.view.disableButtons()
        random_fact = random.choice(fact_file.read().splitlines())
        fact_file.close()
        self.ch_scanning.popFact(random_fact)
        if custom:
            pins = self.ch_custom_scan.isPinsChecked()
            checksum = self.ch_custom_scan.isChecksumChecked()
            retention = self.ch_custom_scan.isRetentionChecked() and self.scarab.cartridge.get("saveexp", 0) != 0
            self.ch_scanning.setupCheck(pins, checksum, retention)
        else:
            pins = True
            checksum = True
            retention = True and self.scarab.cartridge["saveexp"] != 0
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
            temp_save = self.scarab.dumpSave()
            File_Management.retentionWriteTempSave(temp_save, self.scarab.cartridge["name"])
            self.dummy = File_Management.generateDummySave(self.scarab.cartridge["savesize"])
            self.scarab.restoreSave(self.dummy)
            self.ch_scanning.preRetentionNoticeSetup()
            self.view.repaint()
        else:
            self.ch_scanning.checksDone()
            self.view.enableButtons()
            self.view.repaint()
            
        #results = self.scarab.checkHealth(pins, checksum, retention)
        #self.ch_scanning.displayResults(results)
        
    def saveRetentionPreWait(self):
        self.ch_scanning.preRetentionNoticeAcknowledged()
        self.view.repaint()
        QTimer.singleShot(30000, self.saveRetentionPostWait)
        
    def saveRetentionPostWait(self):
        self.ch_scanning.postRetentionNoticeSetup()
        self.view.repaint()
        
    def saveRetentionFinal(self):
        self.ch_scanning.postRetentionNoticeAcknowledged()
        self.view.repaint()
        test_save = self.scarab.dumpSave()
        mismatches = 0
        total = self.scarab.cartridge.get("savesize", 0)
        for i in range(total):
            if test_save[i] != self.dummy[i]:
                mismatches += 1
        percent = round(((total - mismatches) / total) * 100, 2)
        self.ch_scanning.displayResults("retention", True, str(percent) + "% Match")
        temp = File_Management.retentionReadTempSave(self.scarab.cartridge["name"])
        self.scarab.restoreSave(temp)
        File_Management.deleteSave(self.scarab.cartridge["name"], "TEMP", "")
        self.ch_scanning.checksDone()
        self.view.enableButtons()
    
    def deleteSave(self):
        if self.sm_save_browse.getSelectedSave() is None:
            self.view.displayMessage("Save not selected.", is_error=True)
            return
        toDelete = self.sm_save_browse.getSelectedSave()
        console = self.sm_save_browse.current_console
        game = self.sm_save_browse.current_game
        File_Management.deleteSave(toDelete, console, game)
        saves = File_Management.getSavesByGame(console, game)
        self.sm_save_browse.populateSaves(saves, console, game)
        
    def cartSafetyCheck(self) -> bool:
        if self.scarab.scarab is None:
            self.view.displayMessage("SCARAB not found.", is_error=True)
            return False
        if self.scarab.currentModule is None:
            self.view.displayMessage("Module not found.", is_error=True)
            return False
        if "name" not in self.scarab.cartridge.keys():
            self.view.displayMessage("No game inserted.", is_error=True)
            return False
        return True
    
    def getSettings(self):
        self.settings = File_Management.getSettings()
        self.options.populateSettings(self.settings)
        
    def saveSettings(self):
        self.settings = self.options.getSettings()
        File_Management.saveSettings(self.settings)
        self.view.displayMessage("Settings saved.")