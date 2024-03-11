from pytube import YouTube
from moviepy.editor import AudioFileClip
import os
from youtubesearchpython import VideosSearch
#from tabulate import tabulate
import pygame
import time

 # ========== Funçoes ========================== #
 
def exibir_arquivos_mp3(caminho_da_pasta):
    global arquivos_mp3
    # Navega até o diretório especificado
    os.chdir(caminho_da_pasta)

    # Lista todos os arquivos no diretório
    arquivos = os.listdir()

    # Filtra apenas os arquivos com extensão .mp3
    arquivos_mp3 = [arquivo for arquivo in arquivos if arquivo.endswith('.mp3')]

    # Exibe os arquivos mp3 encontrados
    if arquivos_mp3:
        print("\nArquivos MP3 encontrados:")
        for idx, arquivo in enumerate(arquivos_mp3, 1):
            print(f"{idx} | {arquivo}")
    else:
        print("Nenhum arquivo MP3 encontrado neste diretório.")

def reproduzir_audio(arquivo_mp3):
    try:
        # Inicializa o pygame
        pygame.init()

        # Carrega o arquivo MP3 como um objeto Sound
        som = pygame.mixer.Sound(arquivo_mp3)

        # Reproduz o arquivo MP3
        som.play()

        # Obtém a duração da música
        duracao = som.get_length()

        # Loop de controle de reprodução
        inicio = time.time()
        while time.time() - inicio < duracao:
            # Obtém o tempo decorrido da música
            tempo_decorrido = time.time() - inicio

            # Exibe a barra de progresso e o tempo decorrido na mesma linha
            print("\rProgresso: [{:<50}] {:.2f}s/{:.2f}s".format("=" * int(50 * tempo_decorrido / duracao), tempo_decorrido, duracao), end="")
            time.sleep(0.1)

    except KeyboardInterrupt:
        # Se uma interrupção de teclado ocorrer, encerra a reprodução de áudio e encerra o pygame
        som.stop()
        pygame.quit()
    pygame.quit()
    
def download_youtube_audio(youtube_url, output_filename, temp_dir=None):
    if temp_dir is None:
        temp_dir = os.getcwd()  # Define o diretório atual como padrão
    print(temp_dir)
    try:
        # Baixar o vídeo do YouTube
        yt = YouTube(youtube_url)
        video = yt.streams.filter(only_audio=True).first()
        video.download(output_path=temp_dir, filename='temp.mp4')  # Salva o arquivo temporário no diretório especificado

        # Converter o vídeo para MP3
        video_clip = AudioFileClip(os.path.join(temp_dir, 'temp.mp4'))
        video_clip.write_audiofile(output_filename, codec='libmp3lame')

        # Limpar o arquivo temporário
        video_clip.close()
        os.remove(os.path.join(temp_dir, 'temp.mp4'))

        

    except Exception as e:
        print("Erro ao baixar e converter o áudio:", e)


def buscar_videos(entrada):
    global resultBuscas
    global num_buscas_realizadas
    global num_e
    max_results = 10 # Número máximo de resultados a serem retornados
    videos_search = VideosSearch(entrada, limit=max_results)# Realizando a pesquisa no YouTube

    videos = videos_search.result() # Obtendo os resultados da pesquisa
    
    # ============= Verificando quantidade de buscas feitas
    if(num_buscas_realizadas == 1):
        num_e = 11
    elif(num_buscas_realizadas == 2):
        num_e = 21
    elif(num_buscas_realizadas == 3):
        num_e = 31
    elif(num_buscas_realizadas == 4):
        num_e = 41
    elif(num_buscas_realizadas == 5):
        num_e = 51
    
    for index, video in enumerate(videos['result'], num_e): # Extraindo informações dos resultados da pesquisa
        title = video['title']
        video_id = video['id']
        channel = video['channel']['name']
        duration = video['duration']
        views = video['viewCount']['short']
        url = video['link']
        table_data.append([title, channel, duration, url])
    
    resultBuscas.extend(table_data)
    return resultBuscas


# ================================================== [BEGIN] Implementação ================================ #

# ================= Variáveis do programa ================== #
num_buscas_realizadas = 0
num_e = 1 
table_data = [] # lista temporaria para guardar resultados
resultBuscas = []
arquivos_mp3 = []
video = ''
nome = ''



"""

def exibir_resultados_buscas(resultBuscas):
    # Exibindo resultados
    for k in resultBuscas:
        print("---------------------------------------------------------------------")
        for idx, j in enumerate(k):
            if idx == len(k) - 1:  # Último elemento
                break
            elif idx == len(k) - 2:  # Penúltimo elemento
                print('\t\t' + j)
            else:
                print(j, end=' ')

def verifica_escolha(escolha):
    global nome
    global video
    try:
        if escolha.lower() != 'n':
            escolhido = int(input("[Index do Video escollhido]: "))
            video_infos = resultBuscas[escolhido-1]
            nome1 = video_infos[1]
            url1 = video_infos[4]
            url1 = url1.replace("https://", "")
            print(nome1)
            print(url1)
            print(video_infos)
            
            video = url1
            nome = nome1
            
        else:
            pass
    except ValueError:
            print("Por favor, digite 's' para 'sim' ou 'n' para 'não'.")



print(" O que deseja realizar? ") 
opcao = input("[1] Busca  | [2] Download | [3] Escutar Musicas Baixadas |[0] Finalizar programa\t")

# ================ Main Loop =============================== #
while(opcao != "0"):
    
    if(opcao == "1"): # ======== Busca das musicas =========== #
       
        proximo = 1
       
        search_query = input("[Buscar]: ")  # Termo de pesquisa
        
        while(proximo != 0):

            buscar_videos(search_query)
          
            opcao = input('Buscar mais algum vídeo? [S]im ou [N]ão: ')
            if(opcao.lower() == 'sim' or opcao.lower() == 's'):
                proximo = 1 
                num_buscas_realizadas += 1
                search_query = input("[Buscar:] ")
            else:
                
                proximo = 0
              
    elif(opcao == "2"): # ============== Download de musica ========== #
        proximo = 1
        
        exibir_resultados_buscas(resultBuscas)
        op_2 = input("Escolher da lista de buscas? [s]im ou [n]ao: ")
        verifica_escolha(op_2)
            
            
        while(proximo != 0):
            
            if(nome != ''):
                pass
            else:
                video = input('Entre com a URL do vídeo a ser baixado(YouTube urls olny for now!): ')
                nome= input('Digite o nome do arquivo final(mp3): ')
            
            
            youtube_url = video  # URL do vídeo do YouTube
            output_filename = f'{nome}.mp3'  # Nome do arquivo de saída MP3

            download_youtube_audio(youtube_url, output_filename)
            print("Download e conversão concluídos!")
            opcao1 = input('Baixar mais algum vídeo? [S]im ou [N]ão ou [R]eproduzir [Buscar]: ')
            
            
            if(opcao1.lower() == 'sim' or opcao1.lower() == 's'):
                proximo = 1
                nome = ''
                video = ''
                exibir_resultados_buscas(resultBuscas)
                op_2 = input("Escolher da lista de buscas? [s]im ou [n]ao: ")
                verifica_escolha(op_2)
            elif(opcao1.lower() == 'reproduzir' or opcao1.lower() == 'r'):
                reproduzir_audio(output_filename)
            elif(opcao1.lower() == 'buscar' or opcao1.lower() == 'b'):
                opcao = 1
                break
                #continue
            else:
                proximo = 0

        print('======= YouTube Downloader Finalizado! ======= ')
    
    elif( opcao == "3"): # ============== Reprodução de musica ========== #
        try:
            current_directory = os.getcwd()
            exibir_arquivos_mp3(current_directory)
            op_music = int(input("Escolha o index da musica a ser reproduzida | s para voltar menu inicial \t"))
            reproduzir_audio(arquivos_mp3[op_music-1])
            
        except ValueError as ve:
            if(ve.args[0] == "s"):    
               opcao = input("[1] Busca  | [2] Download | [3] Escutar Musicas Baixadas |[0] Finalizar programa\t")
            else:
                op_music = int(input("Digite um valor valido. | s para voltar menu inicial \t"))
    else:
        opcao = input("[1] Busca  | [2] Download | [3] Escutar Musicas Baixadas |[0] Finalizar programa\t")
"""        