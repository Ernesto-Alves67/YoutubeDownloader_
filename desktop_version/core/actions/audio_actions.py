import os
import threading

import pygame


class AudioActions:
    def __init__(self, ):
        pass
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
        value = value /100
        pygame.mixer.music.set_volume(value)


    # # ================================================================= [Reproducao de Audio]
    def update_music_status(self):
        if pygame.mixer.music.get_busy():
            # Obter a posição atual da reprodução da música e atualizar a barra de deslize
            current_pos = pygame.mixer.music.get_pos() / 1000  # Em segundos
            self.ui.slider.setValue(int(current_pos))

    def reproduzir_musica(self, arquivo):
        self.reproducaostatus = 1
        # if(self.diretorio != arquivo):
        if arquivo.startswith('C:\\'):
            nome_abs = arquivo.split('\\')
            parte_diferente = nome_abs[-1]
            parte_diferente = parte_diferente.rstrip('.mp3')
            self.ui.lbl_nome_musica.setText("Playing:  " +parte_diferente)
        elif arquivo.startswith('C://'):
            nome_abs = arquivo.split('//')
            parte_diferente = nome_abs[-1]
            parte_diferente = parte_diferente.rstrip('.mp3')
            self.ui.lbl_nome_musica.setText("Playing:  " +parte_diferente)
        else:
            nome_sem_extensao = arquivo.rstrip('.mp3')
            self.ui.lbl_nome_musica.setText("Playing:  " +nome_sem_extensao)
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
        # if(self.diretorio != arquivo):
        nome_arquivo = os.path.basename(arquivo)
        if ('C://' in arquivo):
            nome_abs = arquivo.split('//')
            parte_diferente = nome_abs[-1]
            parte_diferente = parte_diferente.rstrip('.mp3')
            self.ui.lbl_nome_musica.setText("Playing:  " +parte_diferente)
        elif ('C:\\' in arquivo):
            nome_abs = arquivo.split('\\')
            parte_diferente = nome_abs[-1]
            parte_diferente = parte_diferente.rstrip('.mp3')
            self.ui.lbl_nome_musica.setText("Playing:  " +parte_diferente)
        else:
            nome_sem_extensao = nome_arquivo.rstrip('.mp4')
            self.ui.lbl_nome_musica.setText("Playing:  " +nome_sem_extensao)

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

