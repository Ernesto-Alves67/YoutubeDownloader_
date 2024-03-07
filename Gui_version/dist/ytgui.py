# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'guiyt.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
##from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHBoxLayout, QVBoxLayout, QGridLayout, QMenu, QAction
from PyQt5.QtWidgets import*

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        
        # ========================= [Estilos] ========================= #
        style_button = "QPushButton {" \
                       "background-color: rgb(0, 0, 0);" \
                       "color: rgb(255, 255, 255);" \
                       "border-radius: 10px;" \
                       "}" \
                       "QPushButton::pressed {" \
                       "background-color: rgb(100, 100, 100);" \
                       "}"
        
        style_frmbutton = "background-color: rgb(0, 170, 127);\n"\
                            "border-radius: 15px;\n"
        
        style_tab_main = "color: rgb(255, 255, 255);\n"\
                        "background: rgb(0,0,0)"
                                          
#### ========================================= [ Inicio ] =================================================================================== ####
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(741, 576)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../../Downloads/download-da-nuvem.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("background-color: rgb(255, 255, 255);")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # ========================= [Frame Botoes] ========================= #
        self.button_frame = QtWidgets.QFrame(self.centralwidget)
        self.button_frame.setGeometry(QtCore.QRect(10, 400, 721, 100))
        self.button_frame.setAutoFillBackground(False)
        self.button_frame.setStyleSheet(style_frmbutton)
        self.button_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.button_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.button_frame.setObjectName("button_frame")
        self.button_frame_2 = QtWidgets.QFrame(self.button_frame)
        self.button_frame_2.setGeometry(QtCore.QRect(0, 0, 711, 100))
        self.button_frame_2.setAutoFillBackground(False)
        self.button_frame_2.setStyleSheet(style_frmbutton)
        self.button_frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.button_frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.button_frame_2.setObjectName("button_frame_2")
        
        # ========================= [botao play] ========================= #
        self.button_play = QtWidgets.QPushButton(self.button_frame_2)
        self.button_play.setGeometry(QtCore.QRect(300, 50, 75, 23))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.button_play.setFont(font)
        self.button_play.setStyleSheet(style_button)
        self.button_play.setProperty("play_click_event", True)
        self.button_play.setObjectName("button_play")
        
        # ========================= [botao anterior] ========================= #
        self.button_anterior = QtWidgets.QPushButton(self.button_frame_2)
        self.button_anterior.setGeometry(QtCore.QRect(40, 50, 75, 23))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.button_anterior.setFont(font)
        self.button_anterior.setStyleSheet(style_button)
        self.button_anterior.setProperty("anterior_click_event", True)
        self.button_anterior.setObjectName("button_anterior")
        
        # ========================= [botao proxima] ========================= #
        self.button_proxima = QtWidgets.QPushButton(self.button_frame_2)
        self.button_proxima.setGeometry(QtCore.QRect(590, 50, 75, 23))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.button_proxima.setFont(font)
        self.button_proxima.setStyleSheet(style_button)
        self.button_proxima.setProperty("proxima_click_event", False)
        self.button_proxima.setObjectName("button_proxima")
        
        # ========================= [botao parar] ========================= #
        self.button_parar = QtWidgets.QPushButton(self.button_frame_2)
        self.button_parar.setGeometry(QtCore.QRect(380, 50, 75, 23))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.button_parar.setFont(font)
        self.button_parar.setStyleSheet(style_button)
        self.button_parar.setProperty("parar_click_event", True)
        self.button_parar.setObjectName("button_parar")
        
        # ========================= [botao pausar] ========================= #
        self.button_pause = QtWidgets.QPushButton(self.button_frame_2)
        self.button_pause.setGeometry(QtCore.QRect(220, 50, 75, 23))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.button_pause.setFont(font)
        self.button_pause.setStyleSheet(style_button)
        self.button_pause.setProperty("pause_click_event", True)
        self.button_pause.setObjectName("button_pause")
        
        # ========================= [Player de musica] ========================= #
        self.music_pgbar = QtWidgets.QProgressBar(self.button_frame_2)
        self.music_pgbar.setGeometry(QtCore.QRect(20, 30, 671, 16))
        self.music_pgbar.setStyleSheet("background-color: rgb(85, 170, 255);\n"
"border-radius: 10px;\n"
"")
        self.music_pgbar.setProperty("value", 0)
        self.music_pgbar.setObjectName("music_pgbar")
        self.music_tittle = QtWidgets.QLabel(self.button_frame_2)
        self.music_tittle.setGeometry(QtCore.QRect(40, 10, 471, 16))
        self.music_tittle.setStyleSheet("background: rgb(170, 255, 204)")
        self.music_tittle.setText("")
        self.music_tittle.setObjectName("music_tittle")
        
        # ========================= [Frame Principal] ========================= #
        self.main_frame = QtWidgets.QFrame(self.centralwidget)
        self.main_frame.setGeometry(QtCore.QRect(10, 100, 721, 421))
        self.main_frame.setStyleSheet("background-color: rgb(0, 0, 0);\n")
        self.main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.main_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.main_frame.setObjectName("main_frame")
        
        # ========================= [ABAS] ========================= #
        self.tab_main = QtWidgets.QTabWidget(self.main_frame)
        self.tab_main.setGeometry(QtCore.QRect(0, 0, 721, 401))
        #self.tab_main.setStyleSheet(style_tab_main)
        self.tab_main.setStyleSheet("background-color: rgb(0, 0, 0);\n")
        self.tab_main.setObjectName("tab_main")
        
        # ========================= [Aba Busca/Download] ========================= #
        self.ds_tab = QtWidgets.QWidget()
        self.ds_tab.setStyleSheet("background-color: rgb(0, 170, 127);")
        self.ds_tab.setObjectName("ds_tab")
        
        # ========================= [Buscas] ========================= #
        self.busca_scroll_area = QtWidgets.QScrollArea(self.ds_tab)
        self.busca_scroll_area.setGeometry(QtCore.QRect(10, 30, 421, 361))
        self.busca_scroll_area.setStyleSheet("background-color: rgb(100, 149, 237);\n"
"border-radius: 12px;")
        self.busca_scroll_area.setWidgetResizable(True)
        self.busca_scroll_area.setObjectName("busca_scroll_area")
        self.table_widget = QTableWidget()
        self.table_widget.setStyleSheet("QTableView { border-radius: 10px; border: 2px solid gray; }")

        
        #self.table_widget.horizontalHeader().setVisible(False)
        self.busca_scroll_area.setWidget(self.table_widget)
       
        
        """self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 421, 321))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.busca_scroll_area.setWidget(self.scrollAreaWidgetContents)
        self.busca_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        
        self.busca_scroll_area.setWidget(self.scrollAreaWidgetContents)
        
        self.scroll_layout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)"""
        
        # ========================= [Download log] ========================= #
        self.down_scroll_area = QtWidgets.QScrollArea(self.ds_tab)
        self.down_scroll_area.setGeometry(QtCore.QRect(100, 30, 271, 200))
        self.down_scroll_area.setStyleSheet("background-color: rgb(49, 34, 255);\n"
"border-radius: 12px;")
        self.down_scroll_area.setWidgetResizable(True)
        self.down_scroll_area.setObjectName("down_scroll_area")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 271, 221))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.down_scroll_area.setWidget(self.scrollAreaWidgetContents_2)
            # Criar um layout vertical para o ds_tab
        

        # Adicionar o down_scroll_area ao layout vertical
        
        
        # Definir o alinhamento do down_scroll_area para o lado direito
        
        
        # ========================= [Campo de busca ========================= #
        self.lineEdit = QtWidgets.QLineEdit(self.ds_tab)
        self.lineEdit.setGeometry(QtCore.QRect(10, 10, 361, 20))
        self.lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);\n"
"border-radius: 10px;")
        self.lineEdit.setProperty("busca_clickfocus_event", True)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setAlignment(Qt.AlignCenter)
        self.lineEdit.setToolTip("Entre com ")

        self.label = QtWidgets.QLabel(self.ds_tab)
        self.label.setGeometry(QtCore.QRect(440, 10, 151, 16))
       
        font = QtGui.QFont()
        font.setFamily("Source Serif Pro")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(0, 0, 0); border-radius: 10px")
        self.label.setObjectName("label")
        self.tab_main.addTab(self.ds_tab, "")
        
        # Criar um layout grid para o ds_tab
        ds_tab_layout = QGridLayout(self.ds_tab)

        # Adicionar o QLineEdit e o QLabel na parte superior do grid
        ds_tab_layout.addWidget(self.lineEdit, 0, 0, 1, 1)
        ds_tab_layout.addWidget(self.label, 0, 1)
        

        
        # Adicionar o segundo QScrollArea abaixo do primeiro
        ds_tab_layout.addWidget(self.busca_scroll_area, 1, 0, 1, 1)  # Ocupa uma coluna
        ds_tab_layout.addWidget(self.down_scroll_area, 1, 1, 1, 1)   # Ocupa três colunas


        
        
        ds_tab_layout.setAlignment(Qt.AlignTop) 
        
        
        # ========================= [Aba Reprodução e Vizualização] ========================= #
        self.tab_rep = QtWidgets.QWidget()
        self.tab_rep.setStyleSheet("background-color: rgb(85, 85, 255);")
        
        # ========================= [lista de musicas] ========================= #
        self.lista_music_frame = QtWidgets.QFrame(self.tab_rep)
        self.lista_music_frame.setObjectName(u"lista_music_frame")
        self.lista_music_frame.setGeometry(QtCore.QRect(489, 30, 221, 281))
        self.lista_music_frame.setStyleSheet(u"background-color: rgb(170, 170, 255); border-radius: 10px;")
        self.lista_music_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.lista_music_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.tab_rep.setObjectName("tab_rep")
        self.tab_main.addTab(self.tab_rep, "")
        MainWindow.setCentralWidget(self.centralwidget)
               
        
        # ========================== [status bar] ========================== #
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.statusbar.setStyleSheet("background-color: rgb(255, 0, 255)")
        MainWindow.setStatusBar(self.statusbar)
        

        # ================================================================= [menu bar] ========================================================== #
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 741, 20))
        self.menubar.setObjectName("menubar")
        self.menubar.setStyleSheet("background-color: rgb(255, 255, 255);")
        
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuAjuda = QMenu(self.menubar)
        self.menuAjuda.setObjectName(u"menuAjuda")
        self.menuAjuda.setProperty("exibe_licenca", True)
        self.menuSobre = QMenu(self.menubar)
        self.menuSobre.setObjectName(u"menuSobre")
        """self.actionAbrir_Pasta = QAction(MainWindow)
        self.actionAbrir_Pasta.setObjectName(u"actionAbrir_Pasta")
        self.actionAbrir_Musica = QAction(MainWindow)
        self.actionAbrir_Musica.setObjectName(u"actionAbrir_Musica")
        self.actionConfigura_es = QAction(MainWindow)
        self.actionConfigura_es.setObjectName(u"actionConfigura_es")
        """
        
        self.menubar.setNativeMenuBar(True)
        self.menubar.setVisible(True)
        MainWindow.setMenuBar(self.menubar)
        
        
        """self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAjuda.menuAction())
        self.menubar.addAction(self.menuSobre.menuAction())
        self.menuFile.addAction(self.actionAbrir_Pasta)
        self.menuFile.addAction(self.actionAbrir_Musica)
        self.menuFile.addAction(self.actionConfigura_es)
        """
        self.retranslateUi(MainWindow)
        self.tab_main.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        









    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Youtube Downloader"))
        self.button_play.setText(_translate("MainWindow", "Play"))
        self.button_anterior.setText(_translate("MainWindow", "Anterior"))
        self.button_proxima.setText(_translate("MainWindow", "Proxima"))
        self.button_parar.setText(_translate("MainWindow", "Parar"))
        self.button_pause.setText(_translate("MainWindow", "Pause"))
        self.lineEdit.setText(_translate("MainWindow", "Buscar"))
        self.label.setText(_translate("MainWindow", "Downloads"))
        self.tab_main.setTabText(self.tab_main.indexOf(self.ds_tab), _translate("MainWindow", "D.S"))
        self.tab_main.setTabText(self.tab_main.indexOf(self.tab_rep), _translate("MainWindow", "Listen and View"))
