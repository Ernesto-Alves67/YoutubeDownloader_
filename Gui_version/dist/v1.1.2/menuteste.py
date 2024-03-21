from pytube import YouTube
from moviepy.editor import AudioFileClip
import os
import sys

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTableWidget, QTableWidgetItem, QAction, QFileDialog, QDialog, QSpinBox, QMessageBox, QInputDialog
from PyQt5.QtCore import Qt, QEvent, pyqtSignal, QObject, QThread, QTimer, QFileInfo, QSize

from menu import Ui_MainWindow
from functools import partial
from YtDloader import buscar_videos

from threading import Thread
import pygame
import time
import threading

class AudioDownloader(QObject):
    progress_updated = pyqtSignal(int)
    

    def __init__(self, youtube_url, output_filename, label, temp_dire=None, parent=None):
        super(AudioDownloader, self).__init__(parent)
        self.youtube_url = youtube_url
        self.output_filename = output_filename
        self.label2 = label
        self.temp_dir = temp_dire if temp_dire!=None else os.getcwd()
       
    def download_and_convert_audio(self):
        # Baixar o vídeo do YouTube
       
        yt = YouTube(self.youtube_url)
        video = yt.streams.filter(only_audio=True).first()
        video.download(filename='temp.mp4', output_path=self.temp_dir)
        progress = 25
        self.progress_updated.emit(progress)
         # Converter o vídeo para MP3
        self.label2.setText("Convertendo")
        video_clip = AudioFileClip(os.path.join(self.temp_dir, 'temp.mp4'))
        progress = 50
        self.progress_updated.emit(progress)
        caminho = self.temp_dir+"\\"+self.output_filename
        print(caminho)
        video_clip.write_audiofile(caminho, codec='libmp3lame')

        progress = 100
        self.label2.setText("Concluido")
        self.progress_updated.emit(progress)
        # Limpar o arquivo temporário
        video_clip.close()
        os.remove(os.path.join(self.temp_dir, 'temp.mp4'))
			
class SobreDialog(QtWidgets.QDialog):
    def __init__(self, assunto=None,nomes=None,n_results=None, parent=None):
        super(SobreDialog, self).__init__(parent)
        
        ok_button = QtWidgets.QPushButton("OK")
        cancel_button = QtWidgets.QPushButton("Cancelar")
        
        self.assunto = "sobre" if assunto is None else assunto
        self.nomes = nomes if nomes is not None else None
        self.n_results = n_results if n_results is not None else None
        spacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            
        layout = QtWidgets.QVBoxLayout()
		   
        if(self.assunto == "rnv"):
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
        
        elif(self.assunto == "ytd"):
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
            text = "O YouTube Downloader foi desenvolvido para os amantes da música.\n"\
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

        #print(self.widgets_list[0][0])
        if(self.assunto == "rnv"):
            for k in range(self.num_widgets):
                if( ".mp3" in self.widgets_list[k].text()):
                    self.nomes[k][1] = self.widgets_list[k].text()
                else:
                    self.nomes[k][1] = self.widgets_list[k].text()+'.mp3'
            self.accept()
        elif(self.assunto == "conf"):
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

class MyMainWindow(QMainWindow):
    max_threads = 5  # Por exemplo, vamos permitir até 5 threads simultâneas
    semaphore = threading.Semaphore(max_threads)
    nome_arquivo = ""
    nome_arquivo_link = ""
    nome_proxima = ""
    nome_anterior = ""
    resultados = []
    varios_selec = []
    selecionado = []
    historico = []
    diretorio = "nan"
    state_pause = 0
    state_listaclick = 0
    num_results = 0
    num_resultsB = 0
    reproducaostatus = 0
    nome_musica_reproducao = ""
    som_carregado = ''
    progresso_reproducao = pyqtSignal(int)

    def __init__(self):
        
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.initUI()
        os.chdir(self.ui.path_musicas)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_music_status)
        self.timer.start(100)
        
        # # ================== [Configurando Eventos] =========== ##
        self.ui.lista_musicas.selectionModel().selectionChanged.connect(self.selection_changed_listaMusicas)
        self.ui.lineEdit.returnPressed.connect(self.realiza_busca)        
        self.ui.urlEdit.returnPressed.connect(self.url_link)        
        

        self.ui.button_proxima.clicked.connect(self.next_button_clicked)
        self.ui.button_anterior.clicked.connect(self.previuos_button_clicked)
        self.ui.button_play.clicked.connect(self.play_button_clicked)
        self.ui.button_pause.clicked.connect(self.pause_button_clicked)
        self.ui.button_parar.clicked.connect(self.stop_button_clicked)
        self.ui.button_buscar.clicked.connect(self.realiza_busca)
        self.ui.button_historico.clicked.connect(self.historico_button_clicked)
        self.ui.button_baixar.clicked.connect(self.baixar_clicked)
        self.ui.button_bvarios.clicked.connect(self.baixar_variuos_clicked)
        self.ui.slider.sliderPressed.connect(self.set_music_position)
        self.ui.volume_slider.sliderReleased.connect(self.set_music_volume)
        self.ui.volume_slider.valueChanged.connect(self.set_music_volume)
        self.ui.button_listaMusicas.clicked.connect(self.listaMusicas_click)
        

        self.ui.tabWidget.currentChanged.connect(self.aba_mudada)
        self.ui.actionAbrir_Pasta.triggered.connect(self.abrir_pasta)
        self.ui.actionAbrir_Musica.triggered.connect(self.abrir_musica)
        self.ui.actionReproducao.triggered.connect(self.tutorial_reproducao)
        self.ui.actionDownloads.triggered.connect(self.tutorial_download)
        self.ui.actionBuscas.triggered.connect(self.tutorial_buscas)
        self.ui.actionSobre.triggered.connect(self.mostrar_sobre_dialog)
        self.ui.actConf_ds.triggered.connect(self.mostrar_configuracoes)
        self.ui.actAboutApp.triggered.connect(self.mostrar_sobre_ytd_dialog)

        #self.ui.tabWidget.setCurrentIndex(1)
    # ========================================= [InitUi]
    def initUI(self):
        self.setWindowIcon(QtGui.QIcon(self.ui.iconspath+'app-64.png'))
        sys.stdout = self

    def write(self, text):
        # Exibir progresso na barra de status
        self.statusBar().showMessage(text.strip())        
    # # # ====================================== [Configuração Redimensionamneto] ============================================== ###
    def changeEvent(self, event):
        if event.type() == event.WindowStateChange and self.windowState() & Qt.WindowMaximized:
            self.resizeEvent(event)

    def resizeEvent(self, event):
        # Obter a largura e a altura da janela
        width = self.width()
        height = self.height()
        #print(f" largura atual: {width}")
        #print(f" altura atual: {height}")
        self.ui.tableWidget.resize(width - 300, height - 250)
        self.ui.frame.setGeometry(QtCore.QRect(10, 15, width - 20, height - 65))
        self.ui.tabWidget.setGeometry(QtCore.QRect(0, 0, width - 20, height- 60))
        self.ui.frame_2.setGeometry(QtCore.QRect(width-285, 50, 255, height- 250))
        
        self.ui.frame_3.setGeometry(QtCore.QRect(10, height-185, width - 40 , 91))
        self.ui.frVizualize_music.setGeometry(QtCore.QRect(10, 20, width - 40 , height-211))
        self.ui.listaM_widget.setGeometry(QtCore.QRect(width-385, 0, 511, 40))
        self.ui.frMusic_controls.setGeometry(QtCore.QRect(10, height-185, width - 40 , 91))
        
        #self.ui.slider.setGeometry(100, 10, 590, 10)
        #self.ui.volume_slider.setGeometry(10, 18, 30, 70)
        #self.ui.volume_slider.setStyleSheet("border-radius: 10px;")
        self.ui.urlEdit.setGeometry(QtCore.QRect(width-285, 20, 201, 20))
        self.ui.lineEdit.setGeometry(QtCore.QRect(30, 15, width - 400, 25))

        self.ui.button_play.setText("")
        self.ui.button_historico.setText("Histórico")
        self.ui.button_pause.setText("")
        self.ui.button_anterior.setText("")
        self.ui.button_parar.setText("")
        self.ui.button_proxima.setText("")
        self.ui.lineEdit.setText("")
    
    # # # ======================================================= [Func Utils] ================================================= ###
    
    def get_various_table_selec(self):
        selected_items = self.ui.tableWidget.selectedItems()
        self.varios_selec = []
        if selected_items:
            for item in selected_items:
                #print(item)
                row = item.row()
                column = item.column()
                value = item.text()
                if(column == 0):
                    musica_selec = []
                    musica_selec = [row, value,self.resultados[row][3]]
                    self.varios_selec.append(musica_selec)
                    continue
            
            return True
        else:
            
            return
    
    def get_infoRow_table(self):
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

    def selection_changed_listaMusicas(self, selected, deselected):
        
        indexes2 = selected.indexes()
        if indexes2:
            # Recupera o índice da linha selecionada
            index2 = indexes2[0]
            # Obtém o conteúdo da linha selecionada
            self.nome_musica_reproducao = index2.data()
        
        # Obtenha o modelo associado à lista
        model = self.ui.lista_musicas.model()

        # Obtenha o índice da linha selecionada
        index = selected.indexes()[0] if selected.indexes() else QtCore.QModelIndex()

        # Obtenha o número total de itens
        total_items = model.rowCount()

        # Obtenha o índice da linha anterior e da próxima linha
        previous_row = index.row() - 1
        next_row = index.row() + 1

        # Verifique se a linha anterior é válida e obtenha seu conteúdo
        if previous_row >= 0:
            previous_item = model.data(model.index(previous_row, 0), QtCore.Qt.DisplayRole)
            #print("Item anterior:", previous_item)
            self.nome_anterior = previous_item

        # Verifique se a próxima linha é válida e obtenha seu conteúdo
        if next_row < total_items:
            next_item = model.data(model.index(next_row, 0), QtCore.Qt.DisplayRole)
            #print("Próximo item:", next_item)
            self.nome_proxima = next_item            
 
    def aba_mudada(self, index):
        if(index == 0):
            pass
        else:
            
            """if(self.diretorio == "nan"):
                self.diretorio = os.getcwd()
                arquivos_mp3 = self.ui.listar_arquivos_mp3(self.diretorio)
            else:
                arquivos_mp3 = self.ui.listar_arquivos_mp3(self.diretorio)
            """
            self.arquivos_mp3 = self.ui.listar_arquivos_mp3(self.ui.path_musicas)
            # Adicionando nomes de arquivos ao modelo de dados
            self.ui.model.setStringList(self.arquivos_mp3)
            self.ui.lista_musicas.setModel(self.ui.model)
            
    def exibir_nomeacao_link(self):
        input_dialog = QInputDialog(self)
        input_dialog.setWindowTitle("Nomear Arquivo")
        input_dialog.setLabelText("Nome do arquivo:")
        input_dialog.setMinimumWidth(700)  # Defina o tamanho mínimo da largura
        input_dialog.setMinimumHeight(600)  # Defina o tamanho mínimo da altura
        input_dialog.setStyleSheet("background-color: rgb(150,150,150);color: rgb(255,255,255);")
        
        input_dialog.exec()
        
        if input_dialog.exec() == QDialog.Accepted:
            novo_nome = input_dialog.textValue()
            if( ".mp3" in novo_nome):
                self.nome_arquivo_link = novo_nome
            else:
                self.nome_arquivo_link = novo_nome+'.mp3'
            return 1
        else:
            return 0

  
    # # # ====================================================== [Botoes Music Player] ================================================ ###        
    def pause_button_clicked(self):
        if(self.state_pause == 0):
            pygame.mixer.music.pause()
            self.state_pause = 1
            self.ui.slider.valueChanged.connect(self.set_music_position)
        else:
            pygame.mixer.music.unpause()
            self.state_pause = 0
            self.ui.slider.valueChanged.disconnect(self.set_music_position)

    def stop_button_clicked(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            self.reproducaostatus = False
        else:
            pass

    def play_button_clicked(self):
        if(self.nome_musica_reproducao == ""):
            self.ui.statusbar.showMessage(" ========= Escola uma musica da lista de Músicas =========== ")
        else:
            if(self.reproducaostatus):
                self.stop_button_clicked()
                self.iniciar_reproducao(self.nome_musica_reproducao)
            else:
                self.iniciar_reproducao(self.nome_musica_reproducao)
            
            selection_model = self.ui.lista_musicas.selectionModel()
            selection_model.clearSelection()
            self.set_prox_ant(self.nome_musica_reproducao)
         
    def previuos_button_clicked(self):
        if pygame.mixer.music.get_busy():
            if(self.reproducaostatus):
                self.stop_button_clicked()
                self.iniciar_reproducao(self.nome_anterior)
                self.set_prox_ant(self.nome_anterior)
            else:
                self.iniciar_reproducao(self.nome_anterior)
                self.set_prox_ant(self.nome_anterior)
        else:
            pass
              
    def next_button_clicked(self):
        if pygame.mixer.music.get_busy():
            if(self.reproducaostatus):
                self.stop_button_clicked()
                self.iniciar_reproducao(self.nome_proxima)
                self.set_prox_ant(self.nome_proxima)
            else:
                self.iniciar_reproducao(self.nome_proxima)
                self.set_prox_ant(self.nome_proxima)
        else:
            pass

    def set_prox_ant(self, nome):
        if(self.ui.arquivos_mp3 != None):
            playing_index = self.ui.arquivos_mp3.index(nome)
            if(len(self.ui.arquivos_mp3) > 1):
                if(playing_index == 0):
                    prev_index = (-1)
                    next_index = 1
                elif((playing_index+1) == len(self.ui.arquivos_mp3)):
                    prev_index = playing_index - 1
                    next_index = 0
                else:                
                    prev_index = playing_index - 1
                    next_index = playing_index + 1
                    
                self.nome_proxima = self.ui.arquivos_mp3[next_index]
                self.nome_anterior = self.ui.arquivos_mp3[prev_index]
                return
            else:
                prev_index = 0
                next_index = 0
            return

    def set_music_volume(self):
        value = self.ui.volume_slider.value()
        value = value/100
        pygame.mixer.music.set_volume(value)
        
                          
    # # ================================================================= [Reproducao de Audio]
    def update_music_status(self):
        if pygame.mixer.music.get_busy():
            # Obter a posição atual da reprodução da música e atualizar a barra de deslize
            current_pos = pygame.mixer.music.get_pos() / 1000  # Em segundos
            self.ui.slider.setValue(int(current_pos))

    def reproduzir_musica(self, arquivo):
        self.reproducaostatus = 1
        #if(self.diretorio != arquivo):
        if arquivo.startswith('C:\\'):
            nome_abs = arquivo.split('\\')
            parte_diferente = nome_abs[-1]
            parte_diferente = parte_diferente.rstrip('.mp3')
            self.ui.lbl_nome_musica.setText("Playing: "+parte_diferente)
        elif arquivo.startswith('C://'):
            nome_abs = arquivo.split('//')
            parte_diferente = nome_abs[-1]
            parte_diferente = parte_diferente.rstrip('.mp3')
            self.ui.lbl_nome_musica.setText("Playing: "+parte_diferente)
        else:
            nome_sem_extensao = arquivo.rstrip('.mp3')
            self.ui.lbl_nome_musica.setText("Playing: "+nome_sem_extensao)
        # Inicializa o mixer do pygame
        pygame.mixer.init()

        # Carrega a música
        nl = pygame.mixer.Sound(arquivo)
        arq = pygame.mixer.music.load(arquivo)
        tam_musica = pygame.mixer.Sound.get_length(nl)
        self.ui.slider.setRange(0, int(tam_musica))
        # Reproduz a música
        pygame.mixer.music.play()
        initial_volume = 0.25
        pygame.mixer.music.set_volume(initial_volume)
        minutos = int(tam_musica // 60)
        segundos = int(tam_musica % 60)

    def reproduzir_musica2(self, arquivo):
        self.reproducaostatus = 1
        #if(self.diretorio != arquivo):
        nome_arquivo = os.path.basename(arquivo)   
        if ('C://' in arquivo):
            nome_abs = arquivo.split('//')
            parte_diferente = nome_abs[-1]
            parte_diferente = parte_diferente.rstrip('.mp3')
            self.ui.lbl_nome_musica.setText("Playing: "+parte_diferente)
        elif ('C:\\' in arquivo):
            nome_abs = arquivo.split('\\')
            parte_diferente = nome_abs[-1]
            parte_diferente = parte_diferente.rstrip('.mp3')
            self.ui.lbl_nome_musica.setText("Playing: "+parte_diferente)
        else:
            nome_sem_extensao = nome_arquivo.rstrip('.mp3')
            self.ui.lbl_nome_musica.setText("Playing: "+nome_sem_extensao)
        
        pygame.mixer.init()

        # Carrega a música
        nl = pygame.mixer.Sound(arquivo)
        arq = pygame.mixer.music.load(arquivo)
        tam_musica = pygame.mixer.Sound.get_length(nl)
        self.ui.slider.setRange(0, int(tam_musica))
        # Reproduz a música
        pygame.mixer.music.play()
        initial_volume = 0.25
        pygame.mixer.music.set_volume(initial_volume)
        minutos = int(tam_musica // 60)
        segundos = int(tam_musica % 60)

    def iniciar_reproducao(self, arquivo):
            
        # Cria e inicia uma nova thread para a reprodução
        if self.diretorio == "nan":
            thread = threading.Thread(target=self.reproduzir_musica, args=(arquivo,))
        else:    
            thread = threading.Thread(target=self.reproduzir_musica2, args=(arquivo,))

        thread.start()
      
    def iniciar_proxima_musica(self):
        # Verificar se há uma próxima música na lista e iniciar reprodução
          # Substitua com a lógica real para obter a próxima música
        if self.nome_proxima:
            self.iniciar_reproducao(self.nome_proxima)
        else:
            return

    def set_music_position(self):
        value = self.ui.slider.value()
        pygame.mixer.music.set_pos(value)

        
    # # # ============================================================= [Botoes Download and Search] ================================================ ### 
    def listaMusicas_click(self):
        style_btlm = "QPushButton {background-color: rgb(26,31,49); color: white;"\
                       "text-align: center; padding: 0px; border-radius: 50px; border-width: 15px;}"\
                       "QPushButton:pressed {background-color: rgb(126, 31, 49);}"
        self.ui.button_listaMusicas.setStyleSheet(style_btlm)
        x_pos = self.ui.listaM_widget.pos().x()
        
        if(self.state_listaclick == 0):
            
            self.state_listaclick += 1
            self.ui.listaM_widget.setGeometry(QtCore.QRect(x_pos, 0, 511, 241))
            return 0
        else:
            self.ui.button_listaMusicas.setStyleSheet(self.ui.style_btlista_musica)
            self.ui.listaM_widget.setGeometry(QtCore.QRect(x_pos, 0, 511, 40))
            self.state_listaclick = 0
           
            return 0

    def historico_button_clicked(self):
        if len(self.historico) != 0:
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
                        
                        self.ui.tableWidget.setItem(i, j, QTableWidgetItem(str(self.historico[i][j])))
        else:
            QMessageBox.information(None, "Aviso", "Histórico Vazio.")
    
    def baixar_variuos_clicked(self):

        if self.get_various_table_selec():

            self.start_manydownloads()
        else:
            QMessageBox.information(None, "Aviso", "Selecione linhas na tabela de buscas")
        return

    def baixar_clicked(self): 
        self.selecionado = []
        indice = None
        musica_selecionada = self.get_infoRow_table()
        if musica_selecionada is None:
            pass
        else:
            self.selecionado.append(musica_selecionada)
            indice = self.selecionado[0][0] if self.selecionado[0][0]!=None else None

        if indice is not None:
            link = self.resultados[indice][3]
            
            self.nome_arquivo = f'{self.resultados[indice][0]}.mp3'
            self.ui.label2.setText("Checando nome da musica")
            checa = self.checa_nome()
            if(checa):
                try:
                    self.ui.label2.setText("Iniciando Download")
                    self.start_download(link, self.nome_arquivo, self.ui.path_musicas)
                except Exception as e:
                    QMessageBox.information(None, "Aviso", "Erro ao tentar baixar o arquivo:", str(e))
        else:
            QMessageBox.information(None, "Aviso", "Selecione uma musica.")
    
    def start_download(self, youtube_url, output_filename, temp_dir=None):
        if(temp_dir is None):
            
            self.audio_downloader = AudioDownloader(youtube_url, output_filename, self.ui.label2)
            self.audio_downloader.progress_updated.connect(self.update_progress)
        else:
            self.audio_downloader = AudioDownloader(youtube_url, output_filename, self.ui.label2, temp_dir)
            self.audio_downloader.progress_updated.connect(self.update_progress)
        
        def download_and_release_semaphore():
            # Critical Section
            self.semaphore.acquire()

            # Executa o download e conversão de áudio
            self.audio_downloader.download_and_convert_audio()

            # Libera o semáforo
            self.semaphore.release()

        thread2 = threading.Thread(target=download_and_release_semaphore)
        thread2.start()
        

        return thread2
    
    def update_progress(self, progress):
        self.ui.progress_bar.setValue(progress)
        self.ui.statusbar.showMessage(str(progress))

    def realiza_busca(self):	
        if(self.ui.lineEdit.text() == ""):
            QMessageBox.information(None, "Aviso", "Por favor, Digite algo no campo de busca.")
            return
        else:
            
            if(self.num_results == 0):
                self.resultados.clear()
                self.resultados = buscar_videos(self.ui.lineEdit.text())
                self.historico.extend(self.resultados)
            else:
                self.resultados.clear()
                self.resultados = buscar_videos(self.ui.lineEdit.text(), self.num_results)
                self.historico.extend(self.resultados)

        self.ui.tableWidget.clearContents()
        self.ui.tableWidget.setRowCount(0)  # Limpa todas as linhas existentes
        self.ui.tableWidget.setColumnCount(0)

        num_rows = len(self.resultados)
        
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
            return
        else:

            return

    def bv_checa_nome(self):
        renomeacao = SobreDialog("rnv", self.varios_selec, self)
        
        if(renomeacao.exec_() == QDialog.Accepted):
            return True
        else:
            return False

    def start_manydownloads(self):
        checagem = self.bv_checa_nome()
        print(self.varios_selec)
        if checagem:
            for musica in self.varios_selec:
                print(musica)
                self.nome_arquivo = musica[1]
                link_ = musica[2]
                try:
                    download_variousThread = self.start_download(link_, self.nome_arquivo, self.ui.path_musicas)
                    download_variousThread.join()
                except Exception as e:
                    #print("Erro ao tentar baixar o arquivo:", str(e))
                    continue
            return True     
        else:
            QMessageBox.information(None, "Aviso", f"Download em lotes cancelado.")
            return False

    def checa_nome(self):
        
        while True :
            chars = ["|", "┃", "("]
            char = next((c for c in chars if c in self.nome_arquivo), None)
            if char is not None:
                response = self.aviso_nomeIrregular(f'O Nome do arquivo contem o caractere "{char}"')
                if response:
                    if (self.exibir_dialogo_renomeacao()):
                        continue
                    else:
                        return False
                else:
                    return False

            elif len(self.nome_arquivo) == 4 and '.mp3' == self.nome_arquivo:
                response = self.aviso_nomeIrregular("Nome Invalido para nomeação de arquivo.")
                if response:
                    self.exibir_dialogo_renomeacao()
                    continue
                else:
                    return False
            elif(len(self.nome_arquivo) > 60):
                response = self.aviso_nomeIrregular("Nome Exede tamanho válido.")
                if response:
                    self.exibir_dialogo_renomeacao()
                    continue
                else:
                    return False
            else:
                # QMessageBox.information(None, "Sucesso", "O nome do arquivo é um nome válido.")
                return 1
        return 0

    def exibir_dialogo_renomeacao(self):
        input_dialog = QInputDialog(self)
        input_dialog.setWindowTitle("Renomear Arquivo")
        input_dialog.setLabelText("Novo nome:")
        input_dialog.setFixedSize(700, 600)
        input_dialog.setStyleSheet("background-color: rgb(150,150,150);color: rgb(0,0,0);")
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        input_dialog.setFont(font)
        
        # Define o texto padrão na caixa de entrada
        input_dialog.setTextValue(self.nome_arquivo)

        
        if input_dialog.exec() == QDialog.Accepted:
            # Botão "OK" foi pressionado
            print("inicio if Ok pressionado")
            novo_nome = input_dialog.textValue()
            self.nome_arquivo = novo_nome
            print("Botão OK pressionado. Novo nome:", novo_nome)
            return True
        else:
            # Botão "Cancelar" ou tecla Esc foi pressionada
            print("Botão Cancelar pressionado.")
            return
    
    def aviso_nomeIrregular(self, char):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Aviso")
        msg_box.setText(f"{char}.\nClique em 'Ok' para renomear. ")
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        button_clicked = msg_box.exec_()
        if button_clicked == QMessageBox.Ok:
            print("Botão 'OK' pressionado.")
            return True
        else:
            return False

    def url_link(self):
        pasta_selecionada = QFileDialog.getExistingDirectory(self, "Selecione uma pasta")
        self.diretorio = pasta_selecionada
        link_ = self.ui.urlEdit.text()
        if pasta_selecionada:
            pass
        else:
            print("Erro ao abrir pasta")
        
        nomeacao = self.exibir_nomeacao_link()
        if(nomeacao):
            self.start_download(link_, self.nome_arquivo_link, pasta_selecionada)
        else:
            print("ERROR  {}")

   
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
        arquivo_selecionado, _ = QFileDialog.getOpenFileName(self, "Selecione uma música", "", "Arquivos de Áudio (*.mp3 *.wav)")
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
    
    def mostrar_sobre_ytd_dialog(self):
        ytd = SobreDialog("ytd", self)
        ytd.exec_()

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
        
        ok = input_dialog.exec_()
        if ok:
            # Botão "OK" foi pressionado
            self.num_results = sb_numBuscas.value()
            return 1
        else:
            # Botão "Cancelar" ou tecla Esc foi pressionada
            return 0

		
if __name__ == '__main__':
    app = QApplication(sys.argv)
    icon_path = os.path.join(os.getcwd(), "icons", "app-64.png")
    window = MyMainWindow()
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(icon_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    app.setWindowIcon(icon)
    # Obtenha o caminho absoluto para o ícone
    
    """# Verifique se o arquivo de ícone existe
    if os.path.exists(icon_path):
        app_icon = QtGui.QIcon(icon_path)
        app.setWindowIcon(app_icon)
    else:
        print("Arquivo de ícone não encontrado:", icon_path)
    """
    window.show()

    sys.exit(app.exec_())