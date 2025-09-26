import os

import pygame
import yt_dlp
from PySide6.QtCore import QObject, Signal


class AudioDownloader(QObject):
    progress_updated = Signal(int)

    def __init__(self, youtube_url, output_filename, label, temp_dire=None, parent=None):
        super(AudioDownloader, self).__init__(parent)
        if not pygame.get_init():
            pygame.init()

        if not pygame.mixer.get_init():
            # Exemplo de inicialização com parâmetros comuns:
            # Frequência=44100, Tamanho do bit=-16 (assinado), Canais=2 (estéreo)
            pygame.mixer.init(44100, -16, 2, 2048)

        self.youtube_url = youtube_url
        self.output_filename = output_filename
        self.label2 = label
        self.temp_dir = temp_dire if temp_dire is not None else os.getcwd()

    def download_and_convert_audio(self):
        """
        Baixa o áudio de um vídeo do YouTube e salva como MP3 usando yt-dlp.

        Emite sinais de progresso e atualiza o label durante o processo.
        """
        try:
            # Criar diretório temporário, se não existir
            if not os.path.exists(self.temp_dir):
                os.makedirs(self.temp_dir)

            # Configurações do yt-dlp para baixar áudio como MP3
            ydl_opts = {
                'outtmpl': os.path.join(self.temp_dir, self.output_filename),  # Caminho do arquivo de saída
                'format': 'bestaudio',  # Selecionar melhor qualidade de áudio
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',  # Extrair áudio usando ffmpeg
                    'preferredcodec': 'mp3',  # Formato MP3
                    'preferredquality': '192',  # Qualidade do áudio (192 kbps)
                }],
            }

            # Atualizar progresso (início do download)
            self.label2.setText("Baixando")
            print(self.youtube_url)
            self.progress_updated.emit(25)
            # Baixar e converter áudio
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.youtube_url])

            # # Atualizar progresso (download concluído, "convertendo")
            # self.label2.setText("Convertendo")
            # self.progress_updated.emit(50)
            #
            # # Verificar se o arquivo foi criado
            output_path = os.path.join(self.temp_dir, self.output_filename)
            if not os.path.exists(output_path):
                raise FileNotFoundError(f"Arquivo {output_path} não foi criado.")
            #
            # Atualizar progresso (concluído)
            self.label2.setText("Concluído")
            self.progress_updated.emit(100)

            return f"Áudio baixado com sucesso: "

        except Exception as e:
            self.label2.setText("Erro")
            self.progress_updated.emit(0)
            print(str(e))
            return f"Erro ao baixar o áudio: {str(e)}"
