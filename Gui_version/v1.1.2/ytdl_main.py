import sys
import threading


from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt, QEvent, QTimer
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QFileDialog, QDialog, QMessageBox, \
    QInputDialog

from actions.audio_actions import AudioActions
from ui.dialogs import SobreDialog
from downloader.audio_downloader import *
from downloader.buscas import buscar_videos
from ui.menu import MenuMixin
from ui.ui_ytdownloader import Ui_MainWindow


class MyMainWindow(QMainWindow,
                   MenuMixin,
                   AudioActions):
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
    progresso_reproducao = Signal(int)

    def __init__(self):
        
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.initUI()
        os.chdir(self.ui.path_musicas)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_music_status)
        # self.timer.start(100)
        
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

        
    # ========================================= [InitUi]
    def initUI(self):
        self.setWindowIcon(QtGui.QIcon(self.ui.iconspath+'app-64.png'))
        sys.stdout = self

    def write(self, text):
        # Exibir progresso na barra de status
        self.statusBar().showMessage(text.strip())        
    # # # ====================================== [Configuração Redimensionamneto] ============================================== ###
    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange and self.windowState() & Qt.WindowMaximized:
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
        print(model)
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
        
        if input_dialog.exec() == QDialog.Accepted:
            novo_nome = input_dialog.textValue()
            if( ".mp3" in novo_nome):
                self.nome_arquivo_link = novo_nome
            else:
                self.nome_arquivo_link = novo_nome+'.mp3'
            return 1
        else:
            return 0


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
        print("Entrou no baixar_clicked")
        self.selecionado = []
        indice = None
        musica_selecionada = self.get_infoRow_table()
        print(musica_selecionada)
        if musica_selecionada is None:
            pass
        else:
            self.selecionado.append(musica_selecionada)
            indice = self.selecionado[0][0] if self.selecionado[0][0]!=None else None
        print(self.nome_arquivo)
        if indice is not None:
            link = self.resultados[indice][3]

            self.nome_arquivo = f'{self.resultados[indice][0]}.mp3'
            self.ui.label2.setText("Checando nome da musica")
            checa = self.checa_nome()
            if(checa):
                try:
                    print("entrou")
                    self.ui.label2.setText("Iniciando Download")
                    self.start_download(link, self.nome_arquivo, self.ui.path_musicas)
                except Exception as e:
                    QMessageBox.information(None, "Aviso", "Erro ao tentar baixar o arquivo:", str(e))
        else:
            QMessageBox.information(None, "Aviso", "Selecione uma musica.")
    
    def start_download(self, youtube_url, output_filename, temp_dir=None):
        print("entrou")
        if(temp_dir is None):
            print(youtube_url)
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
        print(self.resultados)
        if(len(self.resultados) > 0):
            for i in range(len(self.resultados)):
                for j in range(num_columns):
                    self.ui.tableWidget.setItem(i, j, QTableWidgetItem(str(self.resultados[i][j])))
            return
        else:

            return

    def bv_checa_nome(self):
        renomeacao = SobreDialog("rnv", self.varios_selec, self)
        
        if(renomeacao.exec() == QDialog.Accepted):
            return True
        else:
            return False

    def start_manydownloads(self):
        checagem = self.bv_checa_nome()
        #print(self.varios_selec)
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
        # font.setWeight(75)
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
        button_clicked = msg_box.exec()
        if button_clicked == QMessageBox.Ok:
            print("Botão 'OK' pressionado.")
            return True
        else:
            return False

    def url_link(self):
        pasta_selecionada = QFileDialog.getExistingDirectory(self, "Selecione uma pasta")
        self.diretorio = pasta_selecionada
        link_ = self.ui.urlEdit.text()
        print(link_)
        if pasta_selecionada:
            pass
        else:
            print("Erro ao abrir pasta")
        
        nomeacao = self.exibir_nomeacao_link()
        if nomeacao:
            self.start_download(link_, self.nome_arquivo_link, pasta_selecionada)
        else:
            print("ERROR  {}")


		
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

    sys.exit(app.exec())