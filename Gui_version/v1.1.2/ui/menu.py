"""
Menu mixin for the main window
"""

from PySide6.QtWidgets import QMessageBox, QFileDialog
import os
import subprocess
import platform


class MenuMixin:
    """Mixin class that provides menu functionality"""
    
    def abrir_pasta(self):
        """Open the music folder in the file explorer"""
        try:
            path = getattr(self.ui, 'path_musicas', os.getcwd())
            
            # Cross-platform folder opening
            if platform.system() == "Windows":
                os.startfile(path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", path])
            else:  # Linux and other Unix-like systems
                subprocess.run(["xdg-open", path])
                
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Não foi possível abrir a pasta: {str(e)}")
    
    def abrir_musica(self):
        """Open a music file"""
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self, 
                "Abrir Música", 
                getattr(self.ui, 'path_musicas', os.getcwd()),
                "Arquivos de Áudio (*.mp3 *.wav *.flac *.ogg *.m4a)"
            )
            
            if file_path:
                # You can implement music opening logic here
                # For now, just show a message
                QMessageBox.information(self, "Música Selecionada", f"Arquivo: {file_path}")
                
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Não foi possível abrir a música: {str(e)}")
    
    def tutorial_reproducao(self):
        """Show reproduction tutorial"""
        msg = """Tutorial de Reprodução:

1. Vá para a aba 'Reprodução'
2. Selecione uma música da lista
3. Use os botões de controle para:
   - ▶️ Play: Reproduzir
   - ⏸️ Pause: Pausar
   - ⏹️ Stop: Parar
   - ⏮️ Anterior: Música anterior
   - ⏭️ Próxima: Próxima música
4. Use o slider para controlar o volume"""
        
        QMessageBox.information(self, "Tutorial - Reprodução", msg)
    
    def tutorial_download(self):
        """Show download tutorial"""
        msg = """Tutorial de Download:

1. Digite o termo de busca no campo de pesquisa
2. Clique em 'Buscar' ou pressione Enter
3. Selecione uma música da tabela de resultados
4. Clique em 'Baixar' para download individual
5. Ou selecione múltiplas músicas e clique 'Baixar Vários'

Para download direto por URL:
1. Cole a URL do YouTube no campo URL
2. Pressione Enter
3. Escolha a pasta de destino
4. Digite o nome do arquivo"""
        
        QMessageBox.information(self, "Tutorial - Downloads", msg)
    
    def tutorial_buscas(self):
        """Show search tutorial"""
        msg = """Tutorial de Buscas:

1. Digite o nome da música, artista ou palavras-chave
2. Clique no botão 'Buscar' ou pressione Enter
3. Os resultados aparecerão na tabela
4. Clique em uma linha para selecioná-la
5. Use Ctrl+Click para seleção múltipla
6. Clique em 'Histórico' para ver buscas anteriores"""
        
        QMessageBox.information(self, "Tutorial - Buscas", msg)
    
    def mostrar_sobre_dialog(self):
        """Show about dialog"""
        # This will be implemented when SobreDialog is created
        QMessageBox.information(self, "Sobre", "YouTube Downloader v1.1.2\n\nDesenvolvido por Ernesto Alves")
    
    def mostrar_configuracoes(self):
        """Show configuration dialog"""
        QMessageBox.information(self, "Configurações", "Configurações em desenvolvimento")
    
    def mostrar_sobre_ytd_dialog(self):
        """Show about YouTube Downloader dialog"""
        msg = """YouTube Downloader v1.1.2

Um programa para baixar e reproduzir músicas do YouTube.

Recursos:
• Busca de vídeos do YouTube
• Download em formato MP3
• Reprodução de áudio
• Interface gráfica amigável

Desenvolvido por: Ernesto Alves
GitHub: Ernesto-Alves67"""
        
        QMessageBox.about(self, "Sobre YouTube Downloader", msg)