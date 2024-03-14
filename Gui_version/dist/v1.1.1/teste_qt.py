import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTableWidget, QTableWidgetItem, QAction
from PyQt5 import QtCore
from ytgui import Ui_MainWindow
from PyQt5.QtCore import Qt, QEvent
from YtDloader import buscar_videos
from YtDloader import reproduzir_audio
from YtDloader import exibir_arquivos_mp3
from YtDloader import download_youtube_audio


class LicenseWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Informações de Licença")
        self.setGeometry(100, 100, 400, 200)

        # Exibir informações da licença
        license_text = "Texto da licença..."
        self.label = QLabel(license_text, self)
        self.label.setGeometry(10, 10, 380, 180)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)




class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.lineEdit.setFocus()
        
        # =========== Configurando Eventos ================ #
        self.ui.lineEdit.mousePressEvent = self.clear_text
        self.ui.lineEdit.returnPressed.connect(self.realiza_busca)        
        self.ui.button_proxima.clicked.connect(self.next_button_clicked)
        self.ui.button_anterior.clicked.connect(self.previuos_button_clicked)
        self.ui.button_play.clicked.connect(self.play_button_clicked)
        self.ui.button_pause.clicked.connect(self.pause_button_clicked)
        self.ui.button_parar.clicked.connect(self.stop_button_clicked)
        """licenca_action = QAction('Informações de Licença', self)
        licenca_action.triggered.connect(self.sobre_menu_cliked)
        self.ui.menuSobre.addAction(licenca_action)"""
 ### ============================================ [Funcionalidades] ====================================================================== ###
 
 
    def realiza_busca(self):
        resultados = buscar_videos(self.ui.lineEdit.text())
        #print(resultados)
        num_rows = len(resultados)
        num_columns = 3
        column_titles = ["Nome", "Canal", "Duração"]
        self.ui.table_widget.setRowCount(num_rows)
        self.ui.table_widget.setColumnCount(num_columns)
        self.ui.table_widget.setHorizontalHeaderLabels(column_titles)
        if(len(resultados) > 0):
            for i in range(len(resultados)):
                print(i)
                for j in range(4):

                    if(j == 3):
                        break
                    self.ui.table_widget.setItem(i, j, QTableWidgetItem(str(resultados[i][j])))

            """for item in resultados:
                item_string = ', '.join(str(elem) for elem in item[:-1])
                #print(item)
                label = QLabel(item_string)
                self.ui.scroll_layout.addWidget(label)"""
                
    def download_music(self, link_):
        try:
            download_youtube_audio(link_)
        except Exception as e:
            print("Erro ao tentar baixar o arquivo:", str(e))
    
    def abre_pasta(self):
        pass
    
    def abre_musica(self):
        pass 
 

 ### ============================================ Definição dos eventos ================================================================== ###
    
    def changeEvent(self, event):
        print("Entrou event no inicio")
        if event.type() == event.WindowStateChange and self.windowState() & Qt.WindowMaximized:
            # Se a janela foi maximizada, execute a função
            self.resizeEvent(event)
    
    def resizeEvent(self, event):
        # Obter a largura e a altura da janela
        width = self.width()
        height = self.height()
        print(f" largura atual: {width}")
        print(f" altura atual: {height}")
        """
        # Redimensionar o botão proporcionalmente à largura e à altura da janela
        button_width = width // 5
        button_height = height // 10
        self.ui.table_widget.resize(width - 250, height - 250)
        self.ui.table_widget.resizeRowsToContents()
        #self.ui.busca_scroll_area.setGeometry(QtCore.QRect(10, 40, width - 630, height - 250 ))
        #self.ui.down_scroll_area.setGeometry(QtCore.QRect(100, 30, 271, height - 251))
        self.ui.main_frame.setGeometry(QtCore.QRect(10, 35, width - 20, height - 145))
        self.ui.tab_main.setGeometry(QtCore.QRect(0, 0, width - 20, height- 130)) 
        self.ui.button_frame.setGeometry(QtCore.QRect(10, height - 110, width - 20 , 91))
        self.ui.menubar.setNativeMenuBar(True)
        self.ui.menubar.setVisible(True)
       
        #self.ui.button_frame_2.setGeometry(QtCore.QRect(0, 0, 711, 100))
        """    
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

    def clear_text(self, event):
        # Limpa o texto quando o QLineEdit é clicado
        self.ui.lineEdit.clear()
    
    def sobre_menu_cliked(self):
        license_window = LicenseWindow()
        license_window.show()
        
    # ====================================== [ Eventos MENU] ======================================== # 
        
    
    
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())