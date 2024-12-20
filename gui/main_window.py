from PySide6 import QtCore, QtWidgets, QtGui
from spoiler_file import SpoilerFile
from gui.game_layout import GameLayout

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, file = None):
        super().__init__()
        self.dark_mode = True
        
        self.setWindowTitle("Spoiler Log Parser")
        
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setGeometry(QtCore.QRect(0, 0, 800, 600))
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("scrollArea")
        self.scroll_area.setEnabled(True)
        self.setCentralWidget(self.scroll_area)
        self.SetDarkMode()
        
        menu = self.menuBar()
        file_menu = menu.addMenu("File")
        preferences_menu = menu.addMenu("Preferences")
        
        load_action = QtGui.QAction("Load", self)
        load_action.setStatusTip("")
        load_action.triggered.connect(self.LoadFileDialog)
        file_menu.addAction(load_action)
        
        dark_mode_action = QtGui.QAction("Dark Mode", self)
        dark_mode_action.setStatusTip("")
        dark_mode_action.setCheckable(True)
        dark_mode_action.setChecked(True)
        dark_mode_action.triggered.connect(self.ToggleMode)
        preferences_menu.addAction(dark_mode_action)
        
        if file != None:
            self.LoadFile(file)
        
    def LoadFileDialog(self):
        file = QtWidgets.QFileDialog.getOpenFileName(self, "Load file...", filter="Randovania Game (*.rdvgame)")
        if file[0] == '':
            return
        self.LoadFile(file[0])
        
    def LoadFile(self, file):
        spoiler = SpoilerFile()
        spoiler.Read(file)
        seed_details = spoiler.GetSeedDetails()
        print(seed_details)
        
        worlds = spoiler.GetWorlds()
        self.scroll_area.setWidget(GameLayout(worlds[0]))
        
    def ToggleMode(self):
        if self.dark_mode:
            self.SetLightMode()
            return
        self.SetDarkMode()
    
    def SetLightMode(self):
        self.scroll_area.setStyleSheet("background:#DDDDDD;color:black;")
        self.dark_mode = False
        
    def SetDarkMode(self):
        self.scroll_area.setStyleSheet("background:#333333;color:white;")
        self.dark_mode = True
