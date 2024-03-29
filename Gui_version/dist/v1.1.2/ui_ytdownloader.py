# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'menu.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QProgressBar, QHBoxLayout,QVBoxLayout, QLabel, QSlider, QGridLayout
from PyQt5.QtCore import QDir, QStringListModel, QTimer, Qt



class Ui_MainWindow(object):
    path = os.getcwd()
    
    iconspath = "_internal\\"+ "\\icons" + "\\"
    arquivos_mp3 = []
    path_musicas = path + "\\Musicas"
    
    if not os.path.exists(path_musicas):
        os.mkdir(path_musicas)
        #print("Pasta criada com sucesso!")
    else:
        pass
    
	## =========================================================== [Estilos]
    style_padrao_1 = "background-color: rgb(26,31,49);"\
                    ""\
                    "border-radius: 10px;"

    style_padrao_2 = "background-color: rgb(150,150,150);"\
                    "color:(0,0,0)"\
                    "border-radius: 10px;"

    stylebuttons = "QPushButton {background-color: rgb(150,150,150); "\
                    "color: rgb(255, 255, 255); "\
                    "border-radius:10px;} "\
                    "QPushButton:pressed {background-color: rgb(134, 53, 181); "\
                    "color: rgb(255, 255, 255); "\
                    "border-radius:10px;}"

    stylebuttons2 = "QPushButton {background-color: rgb(0, 0, 0); "\
                    "color: rgb(255, 255, 255); "\
                    "border-radius:10px;} "\
                    "QPushButton:pressed {background-color: rgb(121, 181, 181); "\
                    "color: rgb(255, 255, 255); "\
                    "border-radius:10px;}"

    stylebutton3 = "QPushButton {background-color: rgb(10, 100, 100); "\
                    "text-align: center; padding: 0px; border-radius: 50px;}"    
    
    style_btlista_musica = "QPushButton {background-color: rgb(150, 150, 150);"\
                       "text-align: center; padding: 0px; border-radius: 50px;}"\
                       "QPushButton:pressed {background-color: rgb(126, 31, 49);}"

                    
    stylemenu = "QMenuBar { background-color: rgb(150, 150, 150);color: rgb(0, 0, 0);  border-radius: 10px;}"\
                "QMenuBar::item:selected { background-color: rgb(26,31,49); color: rgb(255,255,255); border-radius: 10px; }"\
                "QMenu QMenu { }"

    stylemenuItem = "QMenu {background-color: rgb(150, 150, 150); border-radius: 10px; }\n"\
            "QMenu::item:selected { color: rgb(255,255,255); background-color: rgb(26,31,49); }\n"\
			
    styleEdit = "border-radius:10px;\n"\
        "background-color: rgb(255, 255, 255);"\
        "color: rgb(0,0,0)"
# ====================================================== [SetupUi]
    def setupUi(self, MainWindow):
    
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 630)
        MainWindow.setStyleSheet("background-color: rgb(36, 31, 49);")
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        # ============================================= [Frame que contem tabwiget(Abas)]
        self.frame.setGeometry(QtCore.QRect(9, 19, 781, 591))
        self.frame.setStyleSheet("background-color: rgb(150, 150, 150);\n border-radius: 10px;")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.tabWidget = QtWidgets.QTabWidget(self.frame)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 781, 591))
        self.tabWidget.setStyleSheet(self.style_padrao_1)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        
        # ======================================= [resultadoBuscas|Progresso downloads|Entre com URL]
        self.lineEdit = QtWidgets.QLineEdit(self.tab)
        self.lineEdit.setGeometry(QtCore.QRect(30, 20, 401, 20))
        self.lineEdit.setStyleSheet(self.styleEdit)
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setPlaceholderText("Buscar")
        
        self.urlEdit = QtWidgets.QLineEdit(self.tab)
        self.urlEdit.setGeometry(QtCore.QRect(500, 20, 201, 20))
        self.urlEdit.setStyleSheet(self.styleEdit)
        self.urlEdit.setPlaceholderText("Url")
        self.urlEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.urlEdit.setObjectName("urlEdit")
        

        self.frame_2 = QtWidgets.QFrame(self.tab)
        self.frame_2.setGeometry(QtCore.QRect(469, 59, 241, 331))
        self.frame_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")

        self.progress_bar = QProgressBar(self.frame_2)
        self.progress_bar.setObjectName(u"progressBar")
        self.progress_bar.setGeometry(QtCore.QRect(25, 30, 181, 18))
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet("background-color: rgb(255, 255, 255);"
        "color: rgb(0,0,0)")
        
        self.label = QLabel(self.frame_2)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QtCore.QRect(10, 15, 80, 15))
        self.label.setText("Status:")
        self.label.setStyleSheet("background-color: rgb(255, 255, 255);"
        "color: rgb(0,0,0)")
        self.label2 = QLabel(self.frame_2)
        self.label2.setObjectName(u"label2")
        self.label2.setGeometry(QtCore.QRect(80, 15, 90, 13))
        self.label2.setText("")
        self.label2.setStyleSheet("background-color: rgb(255, 255, 255);"
        "color: rgb(0,0,0)")
        
        self.tableWidget = QtWidgets.QTableWidget(self.tab)
        self.tableWidget.setGeometry(QtCore.QRect(10, 50, 400, 451))
        style = "background-color: rgb(150,150,150 ); color: rgb(0,0,0);"
        
        self.tableWidget.setStyleSheet(style)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        horizontal_header = self.tableWidget.horizontalHeader()
        horizontal_header.setStyleSheet("background-color: rbg(36, 31, 49); color: rbg(36, 31, 49)")

        # Mudar a cor do texto dos índices das linhas
        vertical_header = self.tableWidget.verticalHeader()
        vertical_header.setStyleSheet("color: rbg(255, 255, 255); background-color: rbg(36, 31, 49); ")
        
        self.tableWidget.viewport().update()
        self.tabWidget.addTab(self.tab,"")
        # # =================================================== [ FRAME BOTOES UTEIS ] ========================== # #
        
        self.frame_3 = QtWidgets.QFrame(self.tab)
        self.frame_3.setGeometry(QtCore.QRect(10, 380, 711, 80))
        self.frame_3.setStyleSheet("background-color: rgb(121, 181, 181);")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        
        self.botoes_frame_3_lay = QVBoxLayout(self.frame_3)
        
        
        self.frbotoes_uteis = QtWidgets.QFrame()
        self.frbotoes_uteis.setGeometry(QtCore.QRect(100, 15, 611, 45))
        #self.frbotoes_uteis.setStyleSheet("background-color: rgb(255,255,255);")
        self.frbotoes_uteis.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frbotoes_uteis.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frbotoes_uteis.setObjectName("frbotoes_uteis")        

        self.botoes_uteis_lay = QHBoxLayout(self.frbotoes_uteis)
        self.botoes_uteis_lay.setSpacing(10)
        self.botoes_uteis_lay.setObjectName(u"botoes_uteis_lay")        
        
        self.button_baixar = QtWidgets.QPushButton(self.frbotoes_uteis)
        self.button_baixar.setGeometry(QtCore.QRect(490, 30, 75, 40))
        self.button_baixar.setMaximumSize(QtCore.QSize(100, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.button_baixar.setFont(font)
        self.button_baixar.setStyleSheet(self.stylebuttons2)
        self.button_baixar.setObjectName("button_baixar")
        
        self.button_buscar = QtWidgets.QPushButton(self.frbotoes_uteis)
        self.button_buscar.setGeometry(QtCore.QRect(20, 30, 75, 40))
        self.button_buscar.setMaximumSize(QtCore.QSize(100, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.button_buscar.setFont(font)
        self.button_buscar.setStyleSheet(self.stylebuttons2)
        self.button_buscar.setObjectName("button_buscar")
        
        self.button_historico = QtWidgets.QPushButton(self.frbotoes_uteis)
        self.button_historico.setGeometry(QtCore.QRect(120, 30, 141, 40))
        self.button_historico.setMaximumSize(QtCore.QSize(100, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.button_historico.setFont(font)
        
        self.button_historico.setStyleSheet(self.stylebuttons2)
        self.button_historico.setObjectName("button_historico")
        
        self.button_bvarios = QtWidgets.QPushButton(self.frbotoes_uteis)
        self.button_bvarios.setGeometry(QtCore.QRect(574, 30, 101, 40))
        self.button_bvarios.setMaximumSize(QtCore.QSize(100, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.button_bvarios.setFont(font)
        self.button_bvarios.setStyleSheet(self.stylebuttons2)
        self.button_bvarios.setObjectName("button_bvarios")

        self.botoes_uteis_lay.addWidget(self.button_buscar)
        self.botoes_uteis_lay.addWidget(self.button_historico)
        self.botoes_uteis_lay.addWidget(self.button_baixar)
        self.botoes_uteis_lay.addWidget(self.button_bvarios)
        self.botoes_frame_3_lay.addWidget(self.frbotoes_uteis)
        
        # # ============================== [ABA 2: "Listen and view" ] =================================================== ##

        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.frVizualize_music = QtWidgets.QFrame(self.tab_2)
        self.frVizualize_music.setGeometry(QtCore.QRect(20, 20, 311, 431))
        self.frVizualize_music.setStyleSheet("background-color: rgb(194, 194, 194);")
        self.frVizualize_music.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frVizualize_music.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frVizualize_music.setObjectName("frVizualize_music")

        self.model = QStringListModel()
        self.listaM_widget = QtWidgets.QWidget(self.frVizualize_music)
        self.listaM_widget.setGeometry(QtCore.QRect(350, 0, 511, 40))
        self.listaM_widget.setStyleSheet(self.styleEdit)
        # Adicionando nomes de arquivos ao modelo de dados
        diretorio = os.getcwd()
        self.arquivos_mp3 = self.listar_arquivos_mp3(diretorio)
        # Adicionando nomes de arquivos ao modelo de dados
        self.model.setStringList(self.arquivos_mp3)
        # Criação da QListView
        self.scroll_listaMusicas = QtWidgets.QScrollArea(self.listaM_widget)
        self.scroll_listaMusicas.setGeometry(QtCore.QRect(0, 40, 347, 201))
        self.scroll_listaMusicas.setWidgetResizable(True)
        self.lista_musicas = QtWidgets.QListView()
        self.lista_musicas.setGeometry(QtCore.QRect(0, 0, 511, 300))
        self.lista_musicas.setStyleSheet(self.style_padrao_2)
         # Define o modelo para a QListView
        self.lista_musicas.setModel(self.model)
        self.scroll_listaMusicas.setWidget(self.lista_musicas)
        
        self.button_listaMusicas = QtWidgets.QPushButton(self.listaM_widget)
        self.button_listaMusicas.setGeometry(QtCore.QRect(0, 0, 347, 40))
        self.button_listaMusicas.setStyleSheet(self.style_btlista_musica)
        self.button_listaMusicas.setObjectName("button_play")
        self.button_listaMusicas.setText("Musicas")
        self.button_listaMusicas.setFont(font)
        
        
        # # ============================== [ FRAME BOTOES MUSIC PLAYER ] ========================== ##
        self.frMusic_controls = QtWidgets.QFrame(self.tab_2)
        self.frMusic_controls.setGeometry(QtCore.QRect(10, 475, 731, 71))
        self.frMusic_controls.setStyleSheet("background-color: rgb(150, 150, 150);")
        self.frMusic_controls.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frMusic_controls.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frMusic_controls.setObjectName("frMusic_controls")
        
        ## ================================ [layout botoes music play]
        self.verticalLayout_6 = QVBoxLayout(self.frMusic_controls)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")

        self.mPlayer_layout = QVBoxLayout()
        self.mPlayer_layout.setObjectName(u"mPlayer_layout")
        self.widget = QtWidgets.QWidget(self.frMusic_controls)
        self.widget.setObjectName(u"widget")
        self.widget.setStyleSheet(u"background-color: rgb(150, 150, 150);\n"
        "border-radius: 10px;")
        
        self.mPlayer_gridLayout = QGridLayout(self.widget)
        self.mPlayer_gridLayout.setObjectName(u"mPlayer_gridLayout")
        self.mPlayer_gridLayout.setVerticalSpacing(0)
        self.mPlayer_gridLayout.setContentsMargins(5, 5, 5, 5)
        self.btPlayer_layout = QHBoxLayout()
        self.btPlayer_layout.setObjectName(u"btPlayer_layout")
        
        self.frame_botoes = QtWidgets.QFrame(self.widget)
        self.frame_botoes.setObjectName(u"frame_botoes")
        self.frame_botoes.setMaximumSize(QtCore.QSize(16777215, 100))
        self.frame_botoes.setStyleSheet(u"background-color: rgb(150, 150, 150);")
        self.frame_botoes.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_botoes.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_botoes.setLineWidth(5)

        self.btPlayer_layout2_2 = QHBoxLayout(self.frame_botoes)
        self.btPlayer_layout2_2.setObjectName(u"btPlayer_layout2_2")
        self.btPlayer_layout2_2.setContentsMargins(0, 0, 0, 0)
        self.btPlayer_layout2 = QHBoxLayout()
        self.btPlayer_layout2.setObjectName(u"btPlayer_layout2")
        
        # ========================================================== [Criação dos botoes music player]
        self.button_anterior = QtWidgets.QPushButton(self.frame_botoes)
        self.button_anterior.setGeometry(QtCore.QRect(20, 42, 45, 40))
        self.button_anterior.setStyleSheet(self.stylebuttons)
        self.button_anterior.setObjectName("button_anterior")
        pixmap2 = QtGui.QPixmap(self.iconspath + 'anterior-50.png')
        pixmap2 = pixmap2.scaled(30, 30)
        iconAnterior = QtGui.QIcon(pixmap2)
        self.button_anterior.setIcon(iconAnterior)
        self.button_anterior.setIconSize(pixmap2.size())
        self.button_anterior.setText("")

        self.button_play = QtWidgets.QPushButton(self.frame_botoes)
        self.button_play.setGeometry(QtCore.QRect(330, 42, 45, 40))
        self.button_play.setStyleSheet(self.stylebuttons)
        self.button_play.setObjectName("button_play")
        pixmap = QtGui.QPixmap(self.iconspath + 'play-50.png')
        pixmap = pixmap.scaled(30, 30)
        icon = QtGui.QIcon(pixmap)
        self.button_play.setIcon(icon)
        self.button_play.setIconSize(pixmap.size())

        self.button_pause = QtWidgets.QPushButton(self.frame_botoes)
        self.button_pause.setGeometry(QtCore.QRect(410, 42, 45, 40))
        self.button_pause.setStyleSheet(self.stylebuttons)
        self.button_pause.setObjectName("button_pause")
        pixmap3 = QtGui.QPixmap(self.iconspath + 'pause-50.png')
        pixmap3 = pixmap3.scaled(30, 30)
        iconPause = QtGui.QIcon(pixmap3)
        self.button_pause.setIcon(iconPause)
        self.button_pause.setIconSize(pixmap3.size())
        self.button_pause.setText("")

        self.button_parar = QtWidgets.QPushButton(self.frame_botoes)
        self.button_parar.setGeometry(QtCore.QRect(250, 42, 45, 40))
        self.button_parar.setStyleSheet(self.stylebuttons)
        self.button_parar.setObjectName("button_parar")
        pixmap4 = QtGui.QPixmap(self.iconspath + 'stop-50.png')
        pixmap4 = pixmap4.scaled(30, 30)
        iconStop = QtGui.QIcon(pixmap4)
        self.button_parar.setIcon(iconStop)
        self.button_parar.setIconSize(pixmap4.size())
        self.button_parar.setText("")

        self.button_proxima = QtWidgets.QPushButton(self.frame_botoes)
        self.button_proxima.setGeometry(QtCore.QRect(670, 42, 45, 40))
        self.button_proxima.setStyleSheet(self.stylebuttons)
        self.button_proxima.setObjectName("button_proxima")
        pixmap5 = QtGui.QPixmap(self.iconspath + 'proxima-50.png')
        pixmap5 = pixmap5.scaled(30, 30)
        iconStop = QtGui.QIcon(pixmap5)
        self.button_proxima.setIcon(iconStop)
        self.button_proxima.setIconSize(pixmap5.size())


        self.btPlayer_layout2.addWidget(self.button_anterior)
        self.btPlayer_layout2.addWidget(self.button_parar)
        self.btPlayer_layout2.addWidget(self.button_play)
        self.btPlayer_layout2.addWidget(self.button_pause)
        self.btPlayer_layout2.addWidget(self.button_proxima)
        self.btPlayer_layout2_2.addLayout(self.btPlayer_layout2)
        self.btPlayer_layout.addWidget(self.frame_botoes)
        self.btPlayer_layout.setStretch(0, 1)
        self.btPlayer_layout.setSpacing(10)
        self.mPlayer_gridLayout.addLayout(self.btPlayer_layout, 2, 1, 1, 1)

        ## ===================================== [nome musica reproduzindo | volume slider | music tocando progress]
        self.slider = QSlider(self.widget)
        self.slider.setObjectName(u"slider")
        self.slider.setMaximumSize(QtCore.QSize(16777215, 20))
        self.slider.setOrientation(Qt.Horizontal)
        self.mPlayer_gridLayout.addWidget(self.slider, 1, 1, 1, 1)
        
        self.volume_slider = QSlider(self.widget)
        self.volume_slider.setObjectName(u"volume_slider")
        self.volume_slider.setOrientation(Qt.Vertical)

        self.lbl_nome_musica = QLabel(self.widget)
        self.lbl_nome_musica.setObjectName(u"lbl_nome_musica")
        self.lbl_nome_musica.setMinimumSize(QtCore.QSize(100, 0))
        self.lbl_nome_musica.setMaximumSize(QtCore.QSize(350, 20))
        font = QtGui.QFont()
        font.setFamily(u"Leelawadee UI")
        font.setBold(True)
        font.setWeight(75)
        self.lbl_nome_musica.setFont(font)

        self.mPlayer_gridLayout.addWidget(self.lbl_nome_musica, 0, 1, 1, 1)
        self.mPlayer_gridLayout.addWidget(self.volume_slider, 0, 0, 3, 1)
        self.mPlayer_layout.addWidget(self.widget)
        self.verticalLayout_6.addLayout(self.mPlayer_layout)
 
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        
        # # # =============================================== [MENU BAR and STATUSBAR] ===================================== ##
        
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setStyleSheet("background-color: rgb(150,150,150);")

        MainWindow.setStatusBar(self.statusbar)
        
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuTutorial = QtWidgets.QMenu(self.menubar)
        self.menuTutorial.setObjectName("menuTutorial")
        self.menuConfiguracoes = QtWidgets.QMenu(self.menubar)
        self.menuConfiguracoes.setObjectName("menuConfiguracoes")
        self.menuSobre = QtWidgets.QMenu(self.menubar)
        self.menuSobre.setObjectName("menuSobre")
        
        MainWindow.setMenuBar(self.menubar)
        # # ============================================================ [Açoes Menu]
        self.actionSobre = QtWidgets.QAction("Versão",MainWindow)
        self.actionSobre.setObjectName("actionSobre")
        self.actAboutApp = QtWidgets.QAction("Sobre Yt Downloader",MainWindow)
        self.actAboutApp.setObjectName("actAboutApp")
        self.actionAbrir_Pasta = QtWidgets.QAction(MainWindow)
        self.actionAbrir_Pasta.setObjectName("actionAbrir_Pasta")
        self.actionAbrir_Musica = QtWidgets.QAction(MainWindow)
        self.actionAbrir_Musica.setObjectName("actionAbrir_Musica")
        self.actionBuscas = QtWidgets.QAction(MainWindow)
        self.actionBuscas.setObjectName("actionBuscas")
        self.actionDownloads = QtWidgets.QAction(MainWindow)
        self.actionDownloads.setObjectName("actionDownloads")
        self.actionReproducao = QtWidgets.QAction(MainWindow)
        self.actionReproducao.setObjectName("actionReproducao")
        self.actConf_ds = QtWidgets.QAction("Download/Buscas", MainWindow)
        self.actConf_ds.setObjectName("actConf_ds")
        self.actConf_rpr = QtWidgets.QAction("Reprodução", MainWindow)
        self.actConf_rpr.setObjectName("actConf_rpr")
        self.actConf_rpr.setEnabled(False)

        self.menuConfiguracoes.addAction(self.actConf_ds)
        self.menuConfiguracoes.addAction(self.actConf_rpr)
        self.menuSobre.addAction(self.actionSobre)
        self.menuSobre.addAction(self.actAboutApp)
        self.menuFile.addAction(self.actionAbrir_Pasta)
        self.menuFile.addAction(self.actionAbrir_Musica)
        self.menuTutorial.addAction(self.actionDownloads)
        self.menuTutorial.addAction(self.actionBuscas)
        self.menuTutorial.addAction(self.actionReproducao)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTutorial.menuAction())
        self.menubar.addAction(self.menuConfiguracoes.menuAction())
        self.menubar.addAction(self.menuSobre.menuAction())

        
      
        self.menubar.setStyleSheet(self.stylemenu)
        self.menuSobre.setStyleSheet(self.stylemenuItem)
        self.menuFile.setStyleSheet(self.stylemenuItem)
        self.menuTutorial.setStyleSheet(self.stylemenuItem)
        self.menuConfiguracoes.setStyleSheet(self.stylemenuItem)
        
        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
    #[fim SetupUI]

    # ===================================================================[Funcionalidades]
    def listar_arquivos_mp3(self, diretorio):
        arquivos_mp3 = []
        for nome_arquivo in os.listdir(diretorio):
            
            if nome_arquivo.endswith('.mp3'):
                caminho_completo = nome_arquivo
                
                arquivos_mp3.append(caminho_completo)
        self.arquivos_mp3.extend(arquivos_mp3)
        return arquivos_mp3

    # ================================================================ [Traduz a aplicação caso necessario]
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "YouTube Downloader"))
        self.button_baixar.setToolTip(_translate("MainWindow", "Selecione uma linha da tabela de buscas"))
        self.button_baixar.setText(_translate("MainWindow", "Baixar"))
        self.button_buscar.setText(_translate("MainWindow", "Buscar"))
        self.button_historico.setText(_translate("MainWindow", "Historico de Buscas"))
        self.button_bvarios.setToolTip(_translate("MainWindow", "Selecione uma linha da tabela de buscas"))
        self.button_bvarios.setText(_translate("MainWindow", "Baixar Vários"))
        self.lineEdit.setText(_translate("MainWindow", "Buscar"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "D.S"))
        self.button_anterior.setText(_translate("MainWindow", "Anterior"))
        self.button_play.setText(_translate("MainWindow", "Play"))
        self.button_pause.setText(_translate("MainWindow", "Pause"))
        self.button_parar.setText(_translate("MainWindow", "Stop"))
        self.button_proxima.setText(_translate("MainWindow", "Proxima"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Listen and View"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuTutorial.setTitle(_translate("MainWindow", "Tutorial"))
        self.menuConfiguracoes.setTitle(_translate("MainWindow", "Configurações"))
        self.menuSobre.setTitle(_translate("MainWindow", "Sobre"))
        self.actionAbrir_Pasta.setText(_translate("MainWindow", "Abrir Pasta"))
        self.actionAbrir_Musica.setText(_translate("MainWindow", "Abrir Música"))
        self.actionBuscas.setText(_translate("MainWindow", "Buscas"))
        self.actionDownloads.setText(_translate("MainWindow", "Downloads"))
        self.actionReproducao.setText(_translate("MainWindow", "Reprodução"))

