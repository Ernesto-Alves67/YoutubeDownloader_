"""
Dialog classes for the YouTube Downloader application
"""

from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QListWidget, QMessageBox
from PySide6.QtCore import Qt


class SobreDialog(QDialog):
    """Dialog for various purposes (renaming, about, etc.)"""
    
    def __init__(self, dialog_type="about", data=None, parent=None):
        super().__init__(parent)
        self.dialog_type = dialog_type
        self.data = data
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the dialog UI based on type"""
        self.setModal(True)
        
        if self.dialog_type == "about":
            self.setup_about_dialog()
        elif self.dialog_type == "rnv":  # Rename various
            self.setup_rename_various_dialog()
        else:
            self.setup_generic_dialog()
    
    def setup_about_dialog(self):
        """Setup about dialog"""
        self.setWindowTitle("Sobre")
        self.setFixedSize(400, 300)
        
        layout = QVBoxLayout()
        
        title_label = QLabel("YouTube Downloader")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(title_label)
        
        version_label = QLabel("Versão 1.1.2")
        version_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(version_label)
        
        description = QLabel("""
Um programa para baixar e reproduzir músicas do YouTube.

Recursos:
• Busca de vídeos
• Download em MP3
• Reprodução de áudio
        """)
        description.setAlignment(Qt.AlignCenter)
        layout.addWidget(description)
        
        author_label = QLabel("Desenvolvido por: Ernesto Alves")
        author_label.setAlignment(Qt.AlignCenter)
        author_label.setStyleSheet("margin-top: 20px;")
        layout.addWidget(author_label)
        
        # OK button
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)
        
        self.setLayout(layout)
    
    def setup_rename_various_dialog(self):
        """Setup dialog for renaming multiple files"""
        self.setWindowTitle("Renomear Arquivos")
        self.setFixedSize(500, 400)
        
        layout = QVBoxLayout()
        
        info_label = QLabel("Edite os nomes dos arquivos que serão baixados:")
        layout.addWidget(info_label)
        
        # List widget for file names
        self.file_list = QListWidget()
        
        if self.data:
            for item in self.data:
                if len(item) > 1:
                    self.file_list.addItem(item[1])  # Add filename
        
        layout.addWidget(self.file_list)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        button_layout.addWidget(ok_button)
        
        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def setup_generic_dialog(self):
        """Setup generic dialog"""
        self.setWindowTitle("Informação")
        self.setFixedSize(300, 150)
        
        layout = QVBoxLayout()
        
        label = QLabel("Dialog genérico")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)
        
        self.setLayout(layout)