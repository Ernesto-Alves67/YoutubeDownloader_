"""
Audio actions for the YouTube Downloader application
"""

import pygame
import os
from PySide6.QtWidgets import QMessageBox


class AudioActions:
    """Mixin class that provides audio playback functionality"""
    
    def __init__(self):
        super().__init__()
        # Initialize pygame mixer
        try:
            pygame.mixer.init()
            self.pygame_initialized = True
        except Exception as e:
            print(f"Failed to initialize pygame mixer: {str(e)}")
            self.pygame_initialized = False
    
    def next_button_clicked(self):
        """Handle next button click"""
        if hasattr(self, 'nome_proxima') and self.nome_proxima:
            try:
                if self.pygame_initialized:
                    pygame.mixer.music.stop()
                
                # Load and play next song
                next_path = os.path.join(self.ui.path_musicas, self.nome_proxima)
                if os.path.exists(next_path):
                    if self.pygame_initialized:
                        pygame.mixer.music.load(next_path)
                        pygame.mixer.music.play()
                    self.nome_musica_reproducao = self.nome_proxima
                else:
                    QMessageBox.warning(self, "Aviso", "Próxima música não encontrada.")
                    
            except Exception as e:
                QMessageBox.warning(self, "Erro", f"Erro ao reproduzir próxima música: {str(e)}")
    
    def previuos_button_clicked(self):
        """Handle previous button click"""
        if hasattr(self, 'nome_anterior') and self.nome_anterior:
            try:
                if self.pygame_initialized:
                    pygame.mixer.music.stop()
                
                # Load and play previous song
                prev_path = os.path.join(self.ui.path_musicas, self.nome_anterior)
                if os.path.exists(prev_path):
                    if self.pygame_initialized:
                        pygame.mixer.music.load(prev_path)
                        pygame.mixer.music.play()
                    self.nome_musica_reproducao = self.nome_anterior
                else:
                    QMessageBox.warning(self, "Aviso", "Música anterior não encontrada.")
                    
            except Exception as e:
                QMessageBox.warning(self, "Erro", f"Erro ao reproduzir música anterior: {str(e)}")
    
    def play_button_clicked(self):
        """Handle play button click"""
        try:
            if hasattr(self, 'nome_musica_reproducao') and self.nome_musica_reproducao:
                music_path = os.path.join(self.ui.path_musicas, self.nome_musica_reproducao)
                
                if os.path.exists(music_path):
                    if self.pygame_initialized:
                        if pygame.mixer.music.get_busy():
                            # If music is paused, unpause it
                            pygame.mixer.music.unpause()
                        else:
                            # Load and play the music
                            pygame.mixer.music.load(music_path)
                            pygame.mixer.music.play()
                        
                        self.reproducaostatus = 1
                        
                        # Start timer for progress updates
                        if hasattr(self, 'timer'):
                            self.timer.start(100)
                    else:
                        QMessageBox.warning(self, "Erro", "Sistema de áudio não inicializado.")
                else:
                    QMessageBox.warning(self, "Aviso", "Arquivo de música não encontrado.")
            else:
                QMessageBox.information(self, "Aviso", "Selecione uma música para reproduzir.")
                
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao reproduzir música: {str(e)}")
    
    def pause_button_clicked(self):
        """Handle pause button click"""
        try:
            if self.pygame_initialized and pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
                self.state_pause = 1
                if hasattr(self, 'timer'):
                    self.timer.stop()
            
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao pausar música: {str(e)}")
    
    def stop_button_clicked(self):
        """Handle stop button click"""
        try:
            if self.pygame_initialized:
                pygame.mixer.music.stop()
            
            self.reproducaostatus = 0
            self.state_pause = 0
            
            if hasattr(self, 'timer'):
                self.timer.stop()
            
            # Reset progress slider
            if hasattr(self.ui, 'slider'):
                self.ui.slider.setValue(0)
                
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao parar música: {str(e)}")
    
    def set_music_position(self):
        """Set music position based on slider"""
        # Note: pygame doesn't support seeking easily
        # This is a placeholder for position setting functionality
        pass
    
    def set_music_volume(self):
        """Set music volume based on volume slider"""
        try:
            if hasattr(self.ui, 'volume_slider') and self.pygame_initialized:
                volume = self.ui.volume_slider.value() / 100.0
                pygame.mixer.music.set_volume(volume)
                
        except Exception as e:
            print(f"Error setting volume: {str(e)}")
    
    def update_music_status(self):
        """Update music playback status"""
        try:
            if self.pygame_initialized:
                if not pygame.mixer.music.get_busy() and self.reproducaostatus == 1:
                    # Music finished playing
                    self.reproducaostatus = 0
                    if hasattr(self, 'timer'):
                        self.timer.stop()
                    
                    # Auto-play next song if available
                    if hasattr(self, 'nome_proxima') and self.nome_proxima:
                        self.next_button_clicked()
                        
        except Exception as e:
            print(f"Error updating music status: {str(e)}")