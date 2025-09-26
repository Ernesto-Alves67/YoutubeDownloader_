import yt_dlp
import os


def download_youtube_video_yt_dlp(url, output_path="downloads"):
    """
    Baixa um vídeo do YouTube usando yt-dlp.

    Args:
        url (str): URL do vídeo do YouTube.
        output_path (str, optional): Diretório onde o vídeo será salvo. Padrão é "downloads".

    Returns:
        str: Mensagem com o resultado do download.
    """
    try:
        # Criar diretório de saída, se não existir
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # Configurações do yt-dlp
        ydl_opts = {
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',  # Nome do arquivo baseado no título
            'format': 'bestvideo+bestaudio/best',  # Melhor qualidade de vídeo e áudio
            'merge_output_format': 'mp4',  # Forçar saída em MP4
        }

        # Baixar o vídeo
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return f"Vídeo baixado com sucesso em: {output_path}"

    except Exception as e:
        return f"Erro ao baixar o vídeo: {str(e)}"


# Exemplo de uso
if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=-pZ6noOdRXo"
    result = download_youtube_video_yt_dlp(video_url)
    print(result)