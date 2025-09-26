import os
from functools import partial
from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import QFileInfo
from PySide6.QtWidgets import QSpinBox, QDialog, QFileDialog

from ui.dialogs import SobreDialog, TutorialDialog


class MenuMixin:

    # # # ======================================================= [Funcoes menu] ================================================= ###
    def connect_menu_signals(self):
        for action in self.ui.menubar.actions():
            action.hovered.connect(partial(self.menu_hovered, action))
            action.triggered.connect(partial(self.menu_triggered, action))

    def menu_hovered(self, action):
        print("Menu hovered:", action.text())

    def menu_triggered(self, action):
        print("opcao clicada:", action.text())

    def abrir_pasta(self):
        pasta_selecionada = QFileDialog.getExistingDirectory(self, "Selecione uma pasta")
        self.diretorio = pasta_selecionada

        self.ui.arquivos_mp3 = self.ui.listar_arquivos_mp3(self.diretorio)
        if pasta_selecionada:
            os.chdir(self.diretorio)
            self.ui.model.setStringList(self.ui.arquivos_mp3)
            self.ui.lista_musicas.setModel(self.ui.model)

            self.ui.tabWidget.setCurrentIndex(1)
        else:
            pass

    def abrir_musica(self):
        arquivo_selecionado, _ = QFileDialog.getOpenFileName(self, "Selecione uma música", "",
                                                             "Arquivos de Áudio (*.mp3 *.wav *.mp4)")
        if arquivo_selecionado:
            self.diretorio = QFileInfo(arquivo_selecionado).absolutePath()
            os.chdir(self.diretorio)
            self.ui.arquivos_mp3 = self.ui.listar_arquivos_mp3(self.diretorio)
            self.ui.model.setStringList(self.ui.arquivos_mp3)
            self.ui.lista_musicas.setModel(self.ui.model)
            self.iniciar_reproducao(arquivo_selecionado)
            self.ui.tabWidget.setCurrentIndex(1)

            print("Música selecionada:", self.diretorio)
        else:
            print("Erro ao abrir musica")

    def tutorial_download(self):
        print("ds")
        dialog = TutorialDialog(self)
        dialog.exec()

    def tutorial_reproducao(self):
        print("rpr")
        dialog = TutorialDialog(self)
        dialog.tab_widget.setCurrentIndex(2)
        dialog.exec()

    def tutorial_buscas(self):
        dialog = TutorialDialog(self)
        dialog.tab_widget.setCurrentIndex(1)
        dialog.exec()
        print("sch")

    def mostrar_sobre_dialog(self):
        dialog = SobreDialog(self)
        dialog.exec()

    def mostrar_sobre_ytd_dialog(self):
        ytd = SobreDialog("ytd", self)
        ytd.exec()

    def mostrar_configuracoes(self):
        self.exibir_conf_dialog()

    def exibir_conf_dialog(self):
        input_dialog = QDialog(self)
        input_dialog.setWindowTitle("Configurações | D.S")

        input_dialog.setMinimumWidth(400)  # Defina o tamanho mínimo da largura
        input_dialog.setMinimumHeight(500)  # Defina o tamanho mínimo da altura
        input_dialog.setStyleSheet("background-color: rgb(150,150,150);color: rgb(0,0,0);")
        layout = QtWidgets.QVBoxLayout()
        numBuscas_label = QtWidgets.QLabel()

        numBuscas_label.setObjectName(u"numBuscas_label")
        numBuscas_label.setGeometry(QtCore.QRect(0, 5, 5, 13))
        numBuscas_label.setText("Numero de Resultados por busca ")
        sb_numBuscas = QSpinBox()
        sb_numBuscas.setObjectName(u"sb_numBuscas")
        sb_numBuscas.setGeometry(QtCore.QRect(5, 5, 5, 26))
        font = numBuscas_label.font()
        font.setPointSize(10)
        font.setBold(True)
        numBuscas_label.setFont(font)
        sb_numBuscas.setMaximum(20)
        sb_numBuscas.setMinimum(1)
        sb_numBuscas.setSingleStep(5)

        limite_historico_label = QtWidgets.QLabel()
        limite_historico_label.setObjectName(u"limite_historico_label")
        limite_historico_label.setText("Defina um limite para a limpeza do historico de buscas. ")
        limite_historico_label.setFont(font)
        sb_limHistorico = QSpinBox()
        sb_limHistorico.setObjectName(u"sb_limHistorico")
        sb_limHistorico.setGeometry(QtCore.QRect(5, 5, 5, 26))
        sb_limHistorico.setMaximum(100)
        sb_limHistorico.setMinimum(40)
        sb_limHistorico.setSingleStep(10)

        tipo_audio_download = QtWidgets.QLabel()
        tipo_audio_download.setObjectName(u"numBuscas_label")
        tipo_audio_download.setGeometry(QtCore.QRect(0, 8, 5, 13))
        tipo_audio_download.setText("Escolha o tipo de audio a ser baixado ")
        tipo_audio_download.setFont(font)

        rb_mp3 = QtWidgets.QRadioButton()
        rb_mp3.setObjectName(u"rb_mp3")
        rb_mp3.setGeometry(QtCore.QRect(100, 200, 22, 23))
        rb_mp3.setText(".mp3")
        rb_wav = QtWidgets.QRadioButton()
        rb_wav.setObjectName(u"rb_wav")
        rb_wav.setGeometry(QtCore.QRect(110, 200, 22, 23))
        rb_wav.setText(".wav")
        rb_mp4 = QtWidgets.QRadioButton()
        rb_mp4.setObjectName(u"rb_mp4")
        rb_mp4.setGeometry(QtCore.QRect(120, 200, 22, 23))
        rb_mp4.setText(".mp4")
        rb_ogg = QtWidgets.QRadioButton()
        rb_ogg.setObjectName(u"rb_ogg")
        rb_ogg.setGeometry(QtCore.QRect(120, 200, 22, 23))
        rb_ogg.setText(".ogg")

        button_ok = QtWidgets.QPushButton("OK")
        button_ok.clicked.connect(input_dialog.accept)
        button_cancel = QtWidgets.QPushButton("Cancelar")
        button_cancel.clicked.connect(input_dialog.close)

        spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        layout.addWidget(numBuscas_label)
        layout.addWidget(sb_numBuscas)
        layout.addWidget(tipo_audio_download)
        layout.addWidget(rb_mp3)
        layout.addWidget(rb_wav)
        layout.addWidget(rb_mp4)
        layout.addWidget(rb_ogg)
        layout.addItem(spacer)
        layout.addWidget(button_ok)
        layout.addWidget(button_cancel)
        input_dialog.setLayout(layout)

        ok = input_dialog.exec()
        if ok:
            # Botão "OK" foi pressionado
            self.num_results = sb_numBuscas.value()
            return 1
        else:
            # Botão "Cancelar" ou tecla Esc foi pressionada
            return 0