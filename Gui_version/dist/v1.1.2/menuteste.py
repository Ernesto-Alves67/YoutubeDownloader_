from pytube import YouTube
from moviepy.editor import AudioFileClip
import os
import sys

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTableWidget, QTableWidgetItem, QAction, QFileDialog, QDialog, QSpinBox
from menu import Ui_MainWindow
from PyQt5.QtCore import Qt, QEvent, pyqtSignal, QObject, QThread, QTimer, QFileInfo, QSize
from functools import partial
from YtDloader import buscar_videos
from YtDloader import exibir_arquivos_mp3
from threading import Thread

import pygame
import time
import threading

class AudioDownloader(QObject):
    progress_updated = pyqtSignal(int)
    music_updated = pyqtSignal(int)

    def __init__(self, youtube_url, output_filename):
        super().__init__()
        self.youtube_url = youtube_url
        self.output_filename = output_filename

    def download_and_convert_audio(self):
        # Baixar o vídeo do YouTube
        temp_dir = os.getcwd() 
        yt = YouTube(self.youtube_url)
        video = yt.streams.filter(only_audio=True).first()
        video.download(filename='temp.mp4')
        progress = 25
        self.progress_updated.emit(progress)
         # Converter o vídeo para MP3
        video_clip = AudioFileClip(os.path.join(temp_dir, 'temp.mp4'))
        progress = 50
        self.progress_updated.emit(progress)
        video_clip.write_audiofile(self.output_filename, codec='libmp3lame')

        progress = 100
        self.progress_updated.emit(progress)

        # Limpar o arquivo temporário
        video_clip.close()
        os.remove(os.path.join(temp_dir, 'temp.mp4'))

   
    def reproduzir_audio(self, arquivo_mp3):
        try:
            # Inicializa o pygame
            pygame.init()

            # Carrega o arquivo MP3 como um objeto Sound
            som_carregado = pygame.mixer.music.load(arquivo_mp3)
            som2 = pygame.mixer.Sound(arquivo_mp3)

            # Reproduz o arquivo MP3
            #pygame.mixer.Sound.play(som_carregado)
            pygame.mixer.music.play()    
            # Obtém a duração da música
            duracao = pygame.mixer.Sound.get_length(som2)

            # Loop de controle de reprodução
            self.inicio = time.time()
            while time.time() - self.inicio < duracao:
                # Obtém o tempo decorrido da música
                tempo_decorrido = pygame.mixer.music.get_pos()
                #print("Dentro While")
                self.music_updated.emit(tempo_decorrido)

                time.sleep(1)
                

        except KeyboardInterrupt:
            # Se uma interrupção de teclado ocorrer, encerra a reprodução de áudio e encerra o pygame
            
            pygame.quit()
			
class SobreDialog(QtWidgets.QDialog):
	def __init__(self, assunto=None, parent=None):
		super(SobreDialog, self).__init__(parent)
		
		if assunto is None:
			print("A variável é None")
			self.assunto = "sobre"
		else:
			self.assunto = assunto
			print("A variável não é None")
		layout = QtWidgets.QVBoxLayout()
		#print(self.assunto)
		
		if(self.assunto == "conf"):
			self.resize(400, 500)
			self.setWindowTitle("Configurações")
			self.numBuscas_label = QtWidgets.QLabel()
	
			self.numBuscas_label.setObjectName(u"numBuscas_label")
			self.numBuscas_label.setGeometry(QtCore.QRect(0, 5, 5, 13))
			self.numBuscas_label.setText("Numero de Resultados por busca ")
			self.sb_numBuscas = QSpinBox()
			self.sb_numBuscas.setObjectName(u"sb_numBuscas")
			self.sb_numBuscas.setGeometry(QtCore.QRect(5, 5, 5, 26))
			font = self.numBuscas_label.font()
			font.setPointSize(10)
			font.setBold(True)
			self.numBuscas_label.setFont(font)
			self.sb_numBuscas.setMaximum(50)
			self.sb_numBuscas.setMinimum(1)
			
			self.tipo_audio_download = QtWidgets.QLabel()
			self.tipo_audio_download.setObjectName(u"numBuscas_label")
			self.tipo_audio_download.setGeometry(QtCore.QRect(0, 8, 5, 13))
			self.tipo_audio_download.setText("Escolha o tipo de audio a ser baixado ")
			self.tipo_audio_download.setFont(font)
			
			self.rb_mp3 = QtWidgets.QRadioButton()
			self.rb_mp3.setObjectName(u"rb_mp3")
			self.rb_mp3.setGeometry(QtCore.QRect(100, 200, 22, 23))
			self.rb_mp3.setText(".mp3")
			self.rb_wav = QtWidgets.QRadioButton()
			self.rb_wav.setObjectName(u"rb_wav")
			self.rb_wav.setGeometry(QtCore.QRect(110, 200, 22, 23))
			self.rb_wav.setText(".wav")
			self.rb_mp4 = QtWidgets.QRadioButton()
			self.rb_mp4.setObjectName(u"rb_mp4")
			self.rb_mp4.setGeometry(QtCore.QRect(120, 200, 22, 23))
			self.rb_mp4.setText(".mp4")
			self.rb_ogg = QtWidgets.QRadioButton()
			self.rb_ogg.setObjectName(u"rb_ogg")
			self.rb_ogg.setGeometry(QtCore.QRect(120, 200, 22, 23))
			self.rb_ogg.setText(".ogg")
			
			self.button_ok = QtWidgets.QPushButton("OK")
			self.button_ok.clicked.connect(self.accept)

			spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
			
			layout.addWidget(self.numBuscas_label)
			layout.addWidget(self.sb_numBuscas)
			layout.addWidget(self.tipo_audio_download)
			layout.addWidget(self.rb_mp3)
			layout.addWidget(self.rb_wav)
			layout.addWidget(self.rb_mp4)
			layout.addWidget(self.rb_ogg)
			layout.addItem(spacer)
			layout.addWidget(self.button_ok)

			self.setLayout(layout)
			self.setStyleSheet("background-color: rgb(150,150,150)")
		else:
			self.setWindowTitle("Sobre")

			

			layout.addWidget(QtWidgets.QLabel("Este é um programa de exemplo."))
			layout.addWidget(QtWidgets.QLabel("Versão 1.0"))
			self.setLayout(layout)
			self.setStyleSheet("background-color: rgb(150,150,150)")
			
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

class MyMainWindow(QMainWindow):
	resultados = []
	selecionado = []
	historico = []
	diretorio = "nan"
	state_pause = 0
	num_results = 0
	reproducaostatus = 0
	nome_musica_reproducao = ""
	som_carregado = ''
	progresso_reproducao = pyqtSignal(int)
    

	def __init__(self):
		
		super().__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.initUI()
		self.timer = QTimer()
		self.timer.timeout.connect(self.update_music_status)
		self.timer.start(100)
		
		## ================== [Configurando Eventos] =========== ##
		self.ui.lista_musicas.selectionModel().selectionChanged.connect(self.exibir_conteudo_selecionado)
		self.ui.lineEdit.returnPressed.connect(self.realiza_busca)        
		self.ui.button_proxima.clicked.connect(self.next_button_clicked)
		self.ui.button_anterior.clicked.connect(self.previuos_button_clicked)
		self.ui.button_play.clicked.connect(self.play_button_clicked)
		self.ui.button_pause.clicked.connect(self.pause_button_clicked)
		self.ui.button_parar.clicked.connect(self.stop_button_clicked)
		self.ui.button_buscar.clicked.connect(self.realiza_busca)
		self.ui.button_historico.clicked.connect(self.historico_button_clicked)
		self.ui.button_baixar.clicked.connect(self.download_music)
		self.ui.button_bvarios.clicked.connect(self.baixar_variuos_clicked)
		self.ui.slider.sliderMoved.connect(self.set_music_position)
	
		self.ui.tabWidget.currentChanged.connect(self.aba_mudada)
		self.ui.actionAbrir_Pasta.triggered.connect(self.abrir_pasta)
		self.ui.actionAbrir_Musica.triggered.connect(self.abrir_musica)
		self.ui.actionReproducao.triggered.connect(self.tutorial_reproducao)
		self.ui.actionDownloads.triggered.connect(self.tutorial_download)
		self.ui.actionBuscas.triggered.connect(self.tutorial_buscas)
		self.ui.actionSobre.triggered.connect(self.mostrar_sobre_dialog)
		self.ui.actConf_ds.triggered.connect(self.mostrar_configuracoes)
		"""licenca_action = QAction('Informações de Licença', self)
		licenca_action.triggered.connect(self.sobre_menu_cliked)
		self.ui.menuSobre.addAction(licenca_action)"""	
# ========================================= [Fim SetupUi]
# ========================================= [InitUi]
	def initUI(self):

		self.setWindowIcon(QtGui.QIcon(self.ui.iconspath+'app-64.png'))
### ====================================== [Configuração Redimensionamneto] ============================================== ###
	def changeEvent(self, event):
		if event.type() == event.WindowStateChange and self.windowState() & Qt.WindowMaximized:
			self.resizeEvent(event)
    
	def resizeEvent(self, event):
		# Obter a largura e a altura da janela
		width = self.width()
		height = self.height()
		print(f" largura atual: {width}")
		print(f" altura atual: {height}")
		self.ui.tableWidget.resize(width - 300, height - 250)
		#self.ui.tableWidget.resizeRowsToContents()
		#self.ui.busca_scroll_area.setGeometry(QtCore.QRect(10, 40, width - 630, height - 250 ))
		#self.ui.down_scroll_area.setGeometry(QtCore.QRect(100, 30, 271, height - 251))
		self.ui.frame.setGeometry(QtCore.QRect(10, 15, width - 20, height - 65))
		self.ui.tabWidget.setGeometry(QtCore.QRect(0, 0, width - 20, height- 60))
		self.ui.frame_2.setGeometry(QtCore.QRect(width-285, 50, 255, height- 250)) 
		self.ui.frame_3.setGeometry(QtCore.QRect(10, height-185, width - 40 , 91))
		self.ui.frame_4.setGeometry(QtCore.QRect(10, 20, width - 40 , height-191))
		self.ui.frame_5.setGeometry(QtCore.QRect(10, height-200, width - 40 , 91))
		self.ui.slider.setGeometry(10, 10, 20, 10)
		
		pixmap = QtGui.QPixmap(self.ui.iconspath + 'icons8-botão- play -dentro-de-um-círculo-60.png')

		pixmap = pixmap.scaled(35, 35)
		icon = QtGui.QIcon(pixmap)


		
		self.ui.button_play.setIcon(icon)
		self.ui.button_play.setIconSize(pixmap.size())
		self.ui.button_play.setText("")

		self.ui.button_pause.setText("")
		self.ui.button_anterior.setText("")
		self.ui.button_parar.setText("")
		self.ui.button_proxima.setText("")
		
		#tirar depois, debug
		
		

		

### ======================================================= [Funcionalidades] ================================================= ###

	# Função para pegar nome da musica selecionada na linha selecionada
	def exibir_conteudo_selecionado(self, selected, deselected):
		indexes = selected.indexes()
		if indexes:
			# Recupera o índice da linha selecionada
			index = indexes[0]
			# Obtém o conteúdo da linha selecionada
			self.nome_musica_reproducao = index.data()
			# Faça o que quiser com o conteúdo (exemplo: imprimir)
			print("Conteúdo da linha selecionada:", self.nome_musica_reproducao)

	def get_selected_row_info(self):
		selected_items = self.ui.tableWidget.selectedItems()
		if len(selected_items) > 0:
			row = selected_items[0].row()  # Obtém o índice da linha do primeiro item selecionado
			column_count = self.ui.tableWidget.columnCount()
			row_info = []
			row_info.append(row)
			for column in range(column_count):
				item = self.ui.tableWidget.item(row, column)
				row_info.append(item.text())

			return row_info
		else:
			return None

	def teste_selec(self):
		if(self.ui.tableWidget.selectedItems()):

			self.get_selected_row_info()
		else:
			 QMessageBox.warning(self, "Aviso", "Selecione Uma musica dos resultados de buscas")

	def aba_mudada(self, index):
		if(index == 0):
			print("Buscando")
		else:
			if(self.diretorio == "nan"):
				self.diretorio = os.getcwd()
				arquivos_mp3 = self.ui.listar_arquivos_mp3(self.diretorio)
			else:
				arquivos_mp3 = self.ui.listar_arquivos_mp3(self.diretorio)
			

			# Adicionando nomes de arquivos ao modelo de dados
			self.ui.model.setStringList(arquivos_mp3)
			self.ui.lista_musicas.setModel(self.ui.model)
			print("Ouvindo")



### ====================================================== [Botoes Music Player] ================================================ ###        
	def pause_button_clicked(self):
		print("entrou pause")
		state_music = pygame.mixer.music.get_busy()
		if(self.state_pause == 0):
			pygame.mixer.music.pause()
			self.state_pause = 1
			self.ui.slider.valueChanged.connect(self.set_music_position)
		else:
			pygame.mixer.music.unpause()
			self.state_pause = 0
			self.ui.slider.valueChanged.disconnect(self.set_music_position)

	def stop_button_clicked(self):
		print("entrou stop")
		pygame.mixer.music.stop()

	def play_button_clicked(self):
		print("entrou play")
		if(self.reproducaostatus):
			self.stop_button_clicked()
			self.iniciar_reproducao(self.nome_musica_reproducao)
		else:
			self.iniciar_reproducao(self.nome_musica_reproducao)

	def previuos_button_clicked(self):
		print("entrou anterior")

	def next_button_clicked(self):
		print("entrou proxima")
	
	## ======================================= [Reproducao de Audio]
	def update_music_status(self):
		if pygame.mixer.music.get_busy():
			# Obter a posição atual da reprodução da música e atualizar a barra de deslize
			current_pos = pygame.mixer.music.get_pos() / 1000  # Em segundos
			self.ui.slider.setValue(int(current_pos))

	def reproduzir_musica(self, arquivo):
		self.reproducaostatus = 1
		if(self.diretorio != arquivo):
			
			print("diretor != arq")
		# Inicializa o mixer do pygame
		pygame.mixer.init()

		# Carrega a música
		nl = pygame.mixer.Sound(arquivo)
		arq = pygame.mixer.music.load(arquivo)
		tam_musica = pygame.mixer.Sound.get_length(nl)
		self.ui.slider.setRange(0, int(tam_musica))
		# Reproduz a música
		pygame.mixer.music.play()
		initial_volume = 0.5
		pygame.mixer.music.set_volume(initial_volume)
		#print(tam_musica)

		minutos = int(tam_musica // 60)
		segundos = int(tam_musica % 60)

		print("Duração:", minutos, "minutos e", segundos, "segundos")

	def iniciar_reproducao(self, arquivo):
		# Cria e inicia uma nova thread para a reprodução
		thread = threading.Thread(target=self.reproduzir_musica, args=(arquivo,))
		thread.start()
	
	def set_music_position(self, value):
		pygame.mixer.music.set_pos(value)
		
### ============================================================= [Botoes Dowsload and Search] ================================================ ### 
	def historico_button_clicked(self):

		max_width = 200
		num_rows = len(self.historico)
		num_columns = 3
		column_titles = ["Nome", "Canal", "Duração"]
		self.ui.tableWidget.setRowCount(num_rows)
		self.ui.tableWidget.setColumnCount(num_columns)
		self.ui.tableWidget.setHorizontalHeaderLabels(column_titles)
		self.ui.tableWidget.setColumnWidth(50, max_width)
		if(len(self.historico) > 0):
			for i in range(len(self.historico)):
				for j in range(4):

					if(j > 3):

						break
					
					self.ui.tableWidget.setItem(i, j, QTableWidgetItem(str(self.historico[i][j])))
					
	def baixar_variuos_clicked(self):
		print("Baixar Varios")
		self.ui.tableWidget.removeRow(0)

	def download_music(self):

		self.selecionado.append(self.get_selected_row_info())
		indice = self.selecionado[0][0]

		link = self.resultados[indice][3]
		nome_arquivo = f'{self.resultados[indice][0]}.mp3'
		print(link)
		caminho = os.getcwd() 
		try:
			self.start_download(link, nome_arquivo)
		except Exception as e:
			print("Erro ao tentar baixar o arquivo:", str(e))

	def start_download(self, youtube_url, output_filename, temp_dir=None):

		# Criar uma nova thread para download e conversão
		self.thread = QThread()
		self.audio_downloader = AudioDownloader(youtube_url, output_filename)
		self.audio_downloader.moveToThread(self.thread)
		self.thread.started.connect(self.audio_downloader.download_and_convert_audio)
		self.audio_downloader.progress_updated.connect(self.update_progress)
		self.thread.start()

	def update_progress(self, progress):
		self.ui.progress_bar.setValue(progress)
	
	def realiza_busca(self):
		
		if(self.ui.lineEdit.text() == ""):
			QMessageBox.warning(self, "Aviso", "Por favor, algo no campo de busca.")
			return
		else:
			
			if(self.num_results == 0):
				self.resultados.clear()
				print(f"Antes busca: {len(self.resultados)}")
				self.resultados = buscar_videos(self.ui.lineEdit.text())
				self.historico.extend(self.resultados)
				print(f"busca realizada: {len(self.resultados)}")
			else:
				self.resultados = []
				self.resultados = buscar_videos(self.ui.lineEdit.text(), self.num_results)
				self.historico.extend(self.resultados)


		self.ui.tableWidget.clearContents()
		self.ui.tableWidget.setRowCount(0)  # Limpa todas as linhas existentes
		self.ui.tableWidget.setColumnCount(0)

		
		num_rows = len(self.resultados)
		print(num_rows)
		num_columns = 3
		column_titles = ["Nome", "Canal", "Duração"]
		self.ui.tableWidget.setRowCount(num_rows)
		self.ui.tableWidget.setColumnCount(num_columns)
		self.ui.tableWidget.setHorizontalHeaderLabels(column_titles)
		self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
		self.ui.tableWidget.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
		
		if(len(self.resultados) > 0):
			for i in range(len(self.resultados)):
				for j in range(num_columns):
					
					self.ui.tableWidget.setItem(i, j, QTableWidgetItem(str(self.resultados[i][j])))
		else:
			print("Falha na busca")
		

		
		self.ui.tableWidget.viewport().update()
	
	### ======================================================= [Funcoes menu] ================================================= ###
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
		if pasta_selecionada:
			# Aqui você pode fazer o que quiser com a pasta selecionada,
			# por exemplo, exibir o caminho ou trabalhar com os arquivos dentro dela
			print("Pasta selecionada:", pasta_selecionada)
		else:
			print("Erro ao abrir pasta")

	def abrir_musica(self):
		arquivo_selecionado, _ = QFileDialog.getOpenFileName(self, "Selecione uma música", "", "Arquivos de Áudio (*.mp3 *.wav)")
		if arquivo_selecionado:
			self.diretorio = QFileInfo(arquivo_selecionado).absolutePath()
			self.iniciar_reproducao(arquivo_selecionado)
			self.ui.tabWidget.setCurrentIndex(1)
			
			print("Música selecionada:", self.diretorio)
		else:
			print("Erro ao abrir musica")
	
	def tutorial_download(self):
		print("ds")
		dialog = TutorialDialog(self)
		dialog.exec_()

	def tutorial_reproducao(self):
		print("rpr")
		dialog = TutorialDialog(self)
		dialog.tab_widget.setCurrentIndex(2)
		dialog.exec_()
	
	def tutorial_buscas(self):
		dialog = TutorialDialog(self)
		dialog.tab_widget.setCurrentIndex(1)
		dialog.exec_()
		print("sch")

	def mostrar_sobre_dialog(self):
		dialog = SobreDialog(self)
		dialog.exec_()

	def mostrar_configuracoes(self):
		confdialog = SobreDialog("conf", self)
		confdialog.exec_()
		print("Menu de configurações clicado")
		
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())