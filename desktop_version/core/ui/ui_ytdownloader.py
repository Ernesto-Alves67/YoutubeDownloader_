"""
Main UI class for YouTube Downloader application
"""

import os
from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, 
                               QTableWidget, QLineEdit, QPushButton, QLabel, 
                               QSlider, QProgressBar, QListView, QFrame,
                               QMenuBar, QStatusBar, QStringListModel)
from PySide6.QtCore import Qt


class Ui_MainWindow:
    """Main UI class for the YouTube Downloader"""
    
    def __init__(self):
        # Default paths
        self.path_musicas = os.path.join(os.path.expanduser("~"), "Music", "YouTubeDownloads")
        self.iconspath = os.path.join(os.path.dirname(__file__), "..", "icons", "")
        
        # Create music directory if it doesn't exist
        os.makedirs(self.path_musicas, exist_ok=True)
        
        # Model for music list
        self.model = QStringListModel()
        
    def setupUi(self, MainWindow):
        """Setup the main UI"""
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setWindowTitle("YouTube Downloader v1.1.2")
        
        # Central widget
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        
        # Main layout
        main_layout = QVBoxLayout(self.centralwidget)
        
        # Create main frame
        self.frame = QFrame()
        self.frame.setFrameStyle(QFrame.StyledPanel)
        main_layout.addWidget(self.frame)
        
        # Tab widget
        self.tabWidget = QTabWidget(self.frame)
        tab_layout = QVBoxLayout(self.frame)
        tab_layout.addWidget(self.tabWidget)
        
        # Search tab
        self.setup_search_tab()
        
        # Music player tab
        self.setup_player_tab()
        
        # Create additional UI components
        self.setup_additional_components()
        
        # Menu bar
        self.setup_menubar(MainWindow)
        
        # Status bar
        self.statusbar = QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)
        
        # Style
        self.apply_styles()
        
    def setup_search_tab(self):
        """Setup the search tab"""
        search_tab = QWidget()
        search_layout = QVBoxLayout(search_tab)
        
        # Search input layout
        search_input_layout = QHBoxLayout()
        
        self.lineEdit = QLineEdit()
        self.lineEdit.setPlaceholderText("Digite sua busca aqui...")
        search_input_layout.addWidget(self.lineEdit)
        
        self.button_buscar = QPushButton("Buscar")
        search_input_layout.addWidget(self.button_buscar)
        
        search_layout.addLayout(search_input_layout)
        
        # URL input layout
        url_layout = QHBoxLayout()
        url_label = QLabel("URL:")
        self.urlEdit = QLineEdit()
        self.urlEdit.setPlaceholderText("Cole a URL do YouTube aqui...")
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.urlEdit)
        search_layout.addLayout(url_layout)
        
        # Results table
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["Nome", "Canal", "Duração"])
        search_layout.addWidget(self.tableWidget)
        
        # Download buttons layout
        download_layout = QHBoxLayout()
        
        self.button_baixar = QPushButton("Baixar")
        self.button_bvarios = QPushButton("Baixar Vários")
        self.button_historico = QPushButton("Histórico")
        
        download_layout.addWidget(self.button_baixar)
        download_layout.addWidget(self.button_bvarios)
        download_layout.addWidget(self.button_historico)
        download_layout.addStretch()
        
        search_layout.addLayout(download_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        search_layout.addWidget(self.progress_bar)
        
        # Status label
        self.label2 = QLabel("Pronto")
        search_layout.addWidget(self.label2)
        
        self.tabWidget.addTab(search_tab, "Busca e Download")
    
    def setup_player_tab(self):
        """Setup the music player tab"""
        player_tab = QWidget()
        player_layout = QVBoxLayout(player_tab)
        
        # Music visualization frame
        self.frVizualize_music = QFrame()
        self.frVizualize_music.setFrameStyle(QFrame.StyledPanel)
        viz_layout = QVBoxLayout(self.frVizualize_music)
        
        # Music list widget container
        self.listaM_widget = QWidget()
        listaM_layout = QVBoxLayout(self.listaM_widget)
        
        # List music button
        self.button_listaMusicas = QPushButton("Lista de Músicas")
        listaM_layout.addWidget(self.button_listaMusicas)
        
        # Music list
        self.lista_musicas = QListView()
        self.lista_musicas.setModel(self.model)
        listaM_layout.addWidget(self.lista_musicas)
        
        viz_layout.addWidget(self.listaM_widget)
        player_layout.addWidget(self.frVizualize_music)
        
        # Music controls frame
        self.frMusic_controls = QFrame()
        self.frMusic_controls.setFrameStyle(QFrame.StyledPanel)
        controls_layout = QVBoxLayout(self.frMusic_controls)
        
        # Progress slider
        self.slider = QSlider(Qt.Horizontal)
        controls_layout.addWidget(self.slider)
        
        # Control buttons layout
        buttons_layout = QHBoxLayout()
        
        self.button_anterior = QPushButton("⏮")
        self.button_play = QPushButton("▶")
        self.button_pause = QPushButton("⏸")
        self.button_parar = QPushButton("⏹")
        self.button_proxima = QPushButton("⏭")
        
        buttons_layout.addWidget(self.button_anterior)
        buttons_layout.addWidget(self.button_play)
        buttons_layout.addWidget(self.button_pause)
        buttons_layout.addWidget(self.button_parar)
        buttons_layout.addWidget(self.button_proxima)
        
        # Volume control
        volume_layout = QHBoxLayout()
        volume_label = QLabel("Volume:")
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(70)
        volume_layout.addWidget(volume_label)
        volume_layout.addWidget(self.volume_slider)
        
        controls_layout.addLayout(buttons_layout)
        controls_layout.addLayout(volume_layout)
        
        player_layout.addWidget(self.frMusic_controls)
        
        self.tabWidget.addTab(player_tab, "Reprodução")
    
    def setup_additional_components(self):
        """Setup additional UI components"""
        # Additional frames that might be referenced
        self.frame_2 = QFrame()
        self.frame_3 = QFrame()
        
        # Styles for buttons
        self.style_btlista_musica = """
            QPushButton {
                background-color: rgb(64, 64, 64);
                color: white;
                border: 1px solid rgb(100, 100, 100);
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: rgb(80, 80, 80);
            }
            QPushButton:pressed {
                background-color: rgb(120, 120, 120);
            }
        """
        
    def setup_menubar(self, MainWindow):
        """Setup the menu bar"""
        menubar = MainWindow.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("Arquivo")
        
        self.actionAbrir_Pasta = file_menu.addAction("Abrir Pasta de Músicas")
        self.actionAbrir_Musica = file_menu.addAction("Abrir Música")
        
        # Tutorial menu
        tutorial_menu = menubar.addMenu("Tutorial")
        
        self.actionReproducao = tutorial_menu.addAction("Reprodução")
        self.actionDownloads = tutorial_menu.addAction("Downloads")
        self.actionBuscas = tutorial_menu.addAction("Buscas")
        
        # Help menu
        help_menu = menubar.addMenu("Ajuda")
        
        self.actionSobre = help_menu.addAction("Sobre")
        self.actConf_ds = help_menu.addAction("Configurações")
        self.actAboutApp = help_menu.addAction("Sobre o App")
    
    def apply_styles(self):
        """Apply styles to the application"""
        style = """
            QMainWindow {
                background-color: rgb(45, 45, 45);
                color: white;
            }
            
            QTabWidget::pane {
                border: 1px solid rgb(100, 100, 100);
                background-color: rgb(55, 55, 55);
            }
            
            QTabBar::tab {
                background-color: rgb(70, 70, 70);
                color: white;
                padding: 8px 16px;
                border: 1px solid rgb(100, 100, 100);
            }
            
            QTabBar::tab:selected {
                background-color: rgb(100, 100, 100);
            }
            
            QPushButton {
                background-color: rgb(0, 120, 215);
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: rgb(0, 100, 195);
            }
            
            QPushButton:pressed {
                background-color: rgb(0, 80, 175);
            }
            
            QLineEdit {
                background-color: white;
                color: black;
                border: 1px solid rgb(100, 100, 100);
                border-radius: 4px;
                padding: 4px;
            }
            
            QTableWidget {
                background-color: white;
                color: black;
                gridline-color: rgb(200, 200, 200);
            }
            
            QTableWidget::item:selected {
                background-color: rgb(0, 120, 215);
                color: white;
            }
            
            QProgressBar {
                border: 1px solid rgb(100, 100, 100);
                border-radius: 4px;
                text-align: center;
            }
            
            QProgressBar::chunk {
                background-color: rgb(0, 120, 215);
                border-radius: 2px;
            }
            
            QListView {
                background-color: white;
                color: black;
                border: 1px solid rgb(100, 100, 100);
            }
            
            QListView::item:selected {
                background-color: rgb(0, 120, 215);
                color: white;
            }
            
            QSlider::groove:horizontal {
                border: 1px solid rgb(100, 100, 100);
                height: 8px;
                background: rgb(200, 200, 200);
                border-radius: 4px;
            }
            
            QSlider::handle:horizontal {
                background: rgb(0, 120, 215);
                border: 1px solid rgb(0, 100, 195);
                width: 18px;
                margin: -2px 0;
                border-radius: 3px;
            }
        """
        
        # Apply the style to the main window
        # This will be applied by the main window
        self.main_style = style
    
    def listar_arquivos_mp3(self, diretorio):
        """List MP3 files in the given directory"""
        try:
            arquivos_mp3 = []
            for arquivo in os.listdir(diretorio):
                if arquivo.lower().endswith('.mp3'):
                    arquivos_mp3.append(arquivo)
            return sorted(arquivos_mp3)
        except Exception as e:
            print(f"Error listing MP3 files: {str(e)}")
            return []