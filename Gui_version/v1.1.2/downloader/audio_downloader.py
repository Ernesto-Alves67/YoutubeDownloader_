"""
Audio downloader module for YouTube Downloader GUI
Based on the working CLI functionality from YtDownloader_CLI.py
"""

from pytube import YouTube
from moviepy import AudioFileClip
import os
import threading
from PySide6.QtCore import QObject, Signal


class AudioDownloader(QObject):
    """Audio downloader class that provides download functionality with progress updates"""
    
    progress_updated = Signal(int)  # Signal to emit progress updates
    
    def __init__(self, youtube_url, output_filename, label_widget=None, temp_dir=None):
        super().__init__()
        self.youtube_url = youtube_url
        self.output_filename = output_filename
        self.label_widget = label_widget
        self.temp_dir = temp_dir if temp_dir else os.getcwd()
        
    def download_and_convert_audio(self):
        """
        Download and convert YouTube audio to MP3
        This is the core functionality from YtDownloader_CLI.py adapted for GUI
        """
        try:
            if self.label_widget:
                self.label_widget.setText("Conectando ao YouTube...")
            
            # Create YouTube object
            yt = YouTube(self.youtube_url)
            
            if self.label_widget:
                self.label_widget.setText(f"Baixando: {yt.title}")
            
            # Get audio stream
            video = yt.streams.filter(only_audio=True).first()
            
            # Set temporary filename
            temp_filename = os.path.join(self.temp_dir, 'temp.mp4')
            output_path = os.path.join(self.temp_dir, self.output_filename)
            
            if self.label_widget:
                self.label_widget.setText("Baixando stream de áudio...")
            
            # Download the audio stream
            video.download(filename=temp_filename)
            
            # Emit progress
            self.progress_updated.emit(50)
            
            if self.label_widget:
                self.label_widget.setText("Convertendo para MP3...")
            
            # Convert to MP3
            video_clip = AudioFileClip(temp_filename)
            video_clip.write_audiofile(output_path, verbose=False, logger=None)
            
            # Cleanup
            video_clip.close()
            
            # Remove temporary file
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
            
            # Emit completion
            self.progress_updated.emit(100)
            
            if self.label_widget:
                self.label_widget.setText("Download concluído!")
                
            return True
            
        except Exception as e:
            if self.label_widget:
                self.label_widget.setText(f"Erro no download: {str(e)}")
            
            # Clean up temp file if it exists
            temp_filename = os.path.join(self.temp_dir, 'temp.mp4')
            if os.path.exists(temp_filename):
                try:
                    os.remove(temp_filename)
                except:
                    pass
                    
            # Emit error progress
            self.progress_updated.emit(0)
            return False


def download_and_convert_youtube_audio(youtube_url, output_filename):
    """
    Simplified function for direct download (compatibility with CLI version)
    """
    try:
        # Baixar o vídeo do YouTube
        yt = YouTube(youtube_url)
        video = yt.streams.filter(only_audio=True).first()
        video.download(filename='temp.mp4')

        # Converter o vídeo para MP3
        video_clip = AudioFileClip('temp.mp4')
        video_clip.write_audiofile(output_filename, verbose=False, logger=None)

        # Limpar o arquivo temporário
        video_clip.close()
        os.remove('temp.mp4')
        
        return True
        
    except Exception as e:
        print(f"Error in download_and_convert_youtube_audio: {str(e)}")
        # Clean up temp file if it exists
        if os.path.exists('temp.mp4'):
            try:
                os.remove('temp.mp4')
            except:
                pass
        return False