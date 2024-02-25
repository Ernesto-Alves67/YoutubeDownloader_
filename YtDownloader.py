from pytube import YouTube
from moviepy.editor import AudioFileClip
import os

def download_and_convert_youtube_audio(youtube_url, output_filename):
    # Baixar o vídeo do YouTube
    yt = YouTube(youtube_url)
    video = yt.streams.filter(only_audio=True).first()
    video.download(filename='temp.mp4')

    # Converter o vídeo para MP3
    video_clip = AudioFileClip('temp.mp4')
    video_clip.write_audiofile(output_filename)

    # Limpar o arquivo temporário
    video_clip.close()
    os.remove('temp.mp4')

# Exemplo de uso

video = input('Entre com a URL do vídeo a ser baixado(YouTube urls olny for now!: ')
proximo = 1

while(proximo != 0):
    nome= input('Digite o nome do arquivo final(mp3): ')
    youtube_url = video  # URL do vídeo do YouTube
    output_filename = f'{nome}.mp3'  # Nome do arquivo de saída MP3

    download_and_convert_youtube_audio(youtube_url, output_filename)
    print("Download e conversão concluídos!")
    opcao = input('Baixar mais algum vídeo? [S]im ou [N]ão: ')
    if(opcao.lower() == 'sim' or opcao.lower() == 's'):
        proximo = 1 
        video = input('Entre com a URL do próximo vídeo a ser baixado: ')
    else:
        proximo = 0

print('======= YouTube Downloader Finalizado! ======= ')
