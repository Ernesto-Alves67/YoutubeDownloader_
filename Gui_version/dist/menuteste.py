from pytube import YouTube
from moviepy.editor import AudioFileClip
import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTableWidget, QTableWidgetItem, QAction
from PyQt5 import QtCore
from menu import Ui_MainWindow
from PyQt5.QtCore import Qt, QEvent, pyqtSignal, QObject, QThread

from functools import partial
from YtDloader import buscar_videos
from threading import Thread
#from YtDloader import download_youtube_audio



class AudioDownloader(QObject):
    progress_updated = pyqtSignal(int)

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

        
       


class MyMainWindow(QMainWindow):
    resultados = []
    selecionado = []
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.lineEdit.setFocus()
        
        self.connect_menu_signals()
        self.ui.menubar.setStyleSheet(
            "QMenuBar:hover {  }\n"
            "QMenuBar::item:selected { background-color: rgb(125, 0, 0); }\n"
            "QMenuBar::item:hover { background-color: rgb(125, 0, 0); }\n"
            "QMenuBar {color: rgb(0, 0, 0); background-color: rgb(63, 200, 106);}"
        )
        
        self.ui.menuFile.setStyleSheet(
            "QMenu {background-color: rgb(150, 150, 150); }\n"
            "QMenu:hover {  }\n"
          
        )
        
        self.ui.lineEdit.returnPressed.connect(self.realiza_busca)        
        self.ui.button_proxima.clicked.connect(self.next_button_clicked)
        self.ui.button_anterior.clicked.connect(self.previuos_button_clicked)
        self.ui.button_play.clicked.connect(self.play_button_clicked)
        self.ui.button_pause.clicked.connect(self.pause_button_clicked)
        self.ui.button_parar.clicked.connect(self.stop_button_clicked)
        self.ui.button_buscar.clicked.connect(self.realiza_busca)
        self.ui.button_historico.clicked.connect(self.teste_selec)
        self.ui.button_baixar.clicked.connect(self.download_music)
        """licenca_action = QAction('Informações de Licença', self)
        licenca_action.triggered.connect(self.sobre_menu_cliked)
        self.ui.menuSobre.addAction(licenca_action)"""
 
 
 ### ============================================ [Funcionalidades] ====================================================================== ###
    
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
    
    
    def realiza_busca(self):
        
        if(self.ui.lineEdit.text() == ""):
            QMessageBox.warning(self, "Aviso", "Por favor, algo no campo de busca.")
            return
        self.resultados = buscar_videos(self.ui.lineEdit.text())
        
        num_rows = len(self.resultados)
        num_columns = 3
        column_titles = ["Nome", "Canal", "Duração"]
        self.ui.tableWidget.setRowCount(num_rows)
        self.ui.tableWidget.setColumnCount(num_columns)
        self.ui.tableWidget.setHorizontalHeaderLabels(column_titles)
        
        if(len(self.resultados) > 0):
            for i in range(len(self.resultados)):
                for j in range(4):
                    
                    if(j > 3):
                        
                        break
                    self.ui.tableWidget.setItem(i, j, QTableWidgetItem(str(self.resultados[i][j])))
      
    
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
        
    def download_youtube_audio(self, youtube_url, output_filename, temp_dir=None):
        if temp_dir is None:
            temp_dir = os.getcwd()  # Define o diretório atual como padrão
        print(temp_dir)
        
        def update_progress(progress):
            self.ui.progress_bar.setValue(progress)
        try:
            # Baixar o vídeo do YouTube
            yt = YouTube(youtube_url)
            video = yt.streams.filter(only_audio=True).first()
            video.download(output_path=temp_dir, filename='temp.mp4')  # Salva o arquivo temporário no diretório especificado
            
            
            
            # Converter o vídeo para MP3
            video_clip = AudioFileClip(os.path.join(temp_dir, 'temp.mp4'))
            
            total_frames = sum(1 for _ in video_clip.iter_frames())
            
            for i, frame in enumerate(video_clip.iter_frames(), start=1):
                # Calcula a porcentagem de progresso e atualiza a barra de progresso
                progress = int(i / total_frames * 100)
                update_progress(progress)
            
            
            video_clip.write_audiofile(output_filename, codec='libmp3lame')

            # Limpar o arquivo temporário
            video_clip.close()
            os.remove(os.path.join(temp_dir, 'temp.mp4'))

            

        except Exception as e:
            print("Erro ao baixar e converter o áudio:", e)

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
        

### ================================== [Botoes Music Player] ================================================ ###        
    def pause_button_clicked(self,a):
        print("entrou pause")
    
    def stop_button_clicked(self, b):
        print("entrou stop")
        
    def play_button_clicked(self, c):
        print("entrou play")
            
            
    def previuos_button_clicked(self,c ):
        print("entrou anterior")
        
    def next_button_clicked(self):
        print("entrou proxima")



    def connect_menu_signals(self):
        for action in self.ui.menubar.actions():
            action.hovered.connect(partial(self.menu_hovered, action))
            action.triggered.connect(partial(self.menu_triggered, action))

        # ============= [Funcoes menu] ===================#
    def menu_hovered(self, action):
        print("Menu hovered:", action.text())

    def menu_triggered(self, action):
        print("opcao clicada:", action.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())