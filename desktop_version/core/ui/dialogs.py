from PySide6 import QtWidgets, QtGui, QtCore


class SobreDialog(QtWidgets.QDialog):
    def __init__(self, assunto=None, nomes=None, n_results=None, parent=None):
        super(SobreDialog, self).__init__(parent)

        ok_button = QtWidgets.QPushButton("OK")
        cancel_button = QtWidgets.QPushButton("Cancelar")

        self.assunto = "sobre" if assunto is None else assunto
        self.nomes = nomes if nomes is not None else None
        self.n_results = n_results if n_results is not None else None
        spacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        layout = QtWidgets.QVBoxLayout()

        if (self.assunto == "rnv"):
            self.resize(600, 400)
            self.setWindowTitle("Renomeação")
            self.num_widgets = len(self.nomes)
            y_widget = 15
            self.widgets_list = []
            for j in range(self.num_widgets):
                line_edit = QtWidgets.QLineEdit()  # Criar um novo QLineEdit
                line_edit.setGeometry(QtCore.QRect(10, y_widget, 401, 20))
                line_edit.setText(self.nomes[j][1])
                musicaN = QtWidgets.QLabel()
                musicaN.setObjectName(u"musicaN")
                musicaN.setGeometry(QtCore.QRect(0, 5, 5, 13))
                musicaN.setText(f"Nome Musica {j} ")

                layout.addWidget(musicaN)
                layout.addWidget(line_edit)
                self.widgets_list.append(line_edit)
                y_widget += 20

            self.setLayout(layout)
            self.setStyleSheet("background-color: rgb(150,150,150)")
            layout.addItem(spacer)
            layout.addWidget(cancel_button)

        elif (self.assunto == "ytd"):
            self.setWindowTitle("YT Downloader")
            self.resize(400, 300)
            text_edit = QtWidgets.QTextEdit()
            text_edit.setReadOnly(True)
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            text_edit.setFont(font)

            # Definir o texto a ser exibido no QTextEdit
            text = "O YouTube Downloader foi desenvolvido para os amantes da música.\n" \
                   "Aproveite e escute muita música."
            text_edit.setPlainText(text)
            layout.addWidget(text_edit)

            self.setStyleSheet("background-color: rgb(150,150,150)")

        else:
            # Assunto= sobre
            self.setWindowTitle("Sobre")

            layout.addWidget(QtWidgets.QLabel("Este programa é opensource friendly.\nThe Piracy Never Ends"))
            layout.addWidget(QtWidgets.QLabel("Versão 1.1.2"))
            self.setLayout(layout)
            self.setStyleSheet("background-color: rgb(150,150,150)")

        self.setLayout(layout)
        layout.addWidget(ok_button)
        ok_button.clicked.connect(self.on_ok_clicked)

    def on_ok_clicked(self):

        # print(self.widgets_list[0][0])
        if (self.assunto == "rnv"):
            for k in range(self.num_widgets):
                if (".mp3" in self.widgets_list[k].text()):
                    self.nomes[k][1] = self.widgets_list[k].text()
                else:
                    self.nomes[k][1] = self.widgets_list[k].text() + '.mp3'
            self.accept()
        elif (self.assunto == "conf"):
            self.n_results = self.sb_numBuscas.value()
            print(self.n_results)

        else:
            self.accept()


class TutorialDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(TutorialDialog, self).__init__(parent)

        self.setWindowTitle("Instruções de Uso")

        self.tab_widget = QtWidgets.QTabWidget()
        self.tab_widget.setStyleSheet("background-color: rgb(150,150,150)")
        self.resize(600, 400)
        # Tab para download
        download_tab = QtWidgets.QWidget()
        download_layout = QtWidgets.QVBoxLayout()

        self.text_edit = QtWidgets.QTextEdit()
        self.text_edit.setReadOnly(True)  # Para tornar o QTextEdit somente leitura

        # Instruções ou tutorial sobre o download
        tutorial_text = """<h2>Instruções para Download:</h2>
		<p>1. Selecione uma musica nos resultados de busca</p>
		<p>2. Escolha a pasta onde deseja salvar o arquivo.</p>
		<p>3. Clique em "Baixar" e aguarde o download ser concluído.</p>
		"""
        self.text_edit.setHtml(tutorial_text)

        download_layout.addWidget(self.text_edit)

        download_tab.setLayout(download_layout)
        self.tab_widget.addTab(download_tab, "Download")

        # ================================================== Tab para buscas
        buscas_tab = QtWidgets.QWidget()
        buscas_layout = QtWidgets.QVBoxLayout()
        self.text_edit2 = QtWidgets.QTextEdit()
        self.text_edit2.setReadOnly(True)  # Para tornar o QTextEdit somente leitura

        # ==== Instruções sobre as Buscas
        tutorial_text2 = """<h2>Instruções para Buscas:</h2>
		<p>1. Digite o nome de algum artista, ou musica que queira buscar.</p>
		<p>2. Selecione uma linha nos resultados de busca, clicando no indice lateral da musica desejada.</p>
		<p>3. Aguarde até que o download seja concluído.</p>
		<p>3. Utilize o botão "Historico de buscas" para acessar seu historico de buscas.</p>
		"""
        self.text_edit2.setHtml(tutorial_text2)
        buscas_layout.addWidget(self.text_edit2)
        buscas_tab.setLayout(buscas_layout)
        self.tab_widget.addTab(buscas_tab, "Buscas")

        # Tab para reprodução
        reproducao_tab = QtWidgets.QWidget()
        reproducao_layout = QtWidgets.QVBoxLayout()
        self.text_edit3 = QtWidgets.QTextEdit()
        self.text_edit3.setReadOnly(True)  # Para tornar o QTextEdit somente leitura

        # ==== Instruções sobre a Reprodução de audio
        tutorial_text3 = """<h2>Instruções para Reprodução de Audio:</h2>
		<p>1. Na aba "Listen and View" selecione uma musica da lista de musica e aperte o "play" ou apenas a tecla "Enter".</p>
		<p>2. Na opção "File", da barra de menu, na opção "Abrir Pasta" você pode escolher uma pasta que deseje abrir.</p>
		<p>3. Na opção "File", da barra de menu, na opção "Abrir Musica" você pode escolher de um local especifico uma musica que deseje escutar.</p>
		<p>3. Os formatos de audio suportados são: .mp3 /.mp4 / .wav / .ogg </p>
		"""
        self.text_edit3.setHtml(tutorial_text3)
        reproducao_layout.addWidget(self.text_edit3)
        reproducao_tab.setLayout(reproducao_layout)
        self.tab_widget.addTab(reproducao_tab, "Reprodução")

        self.button_ok = QtWidgets.QPushButton("OK")
        self.button_ok.clicked.connect(self.accept)
        self.button_ok.setStyleSheet("background-color: rgb(150,150,150)")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.tab_widget)
        layout.addWidget(self.button_ok)
        self.setLayout(layout)