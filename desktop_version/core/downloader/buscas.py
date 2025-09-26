from googleapiclient.discovery import build
import os
import re  # Necessário para a função de conversão

table_data = []
resultBuscas = []
arquivos_mp3 = []


# FUNÇÃO ADICIONADA: Converte a duração de ISO 8601 para MM:SS ou HH:MM:SS
def converter_duracao_iso8601(iso_duration):
    """Converte uma string de duração ISO 8601 (ex: PT1H30M15S) para o formato HH:MM:SS ou MM:SS."""
    # A duração do vídeo começa com 'PT'
    match = re.search(r'PT(\d+H)?(\d+M)?(\d+S)?', iso_duration)
    if not match:
        return "N/D"

    hours = 0
    minutes = 0
    seconds = 0

    # Extrai e converte horas, minutos e segundos
    h = match.group(1)
    m = match.group(2)
    s = match.group(3)

    if h:
        hours = int(h[:-1])
    if m:
        minutes = int(m[:-1])
    if s:
        seconds = int(s[:-1])

    total_seconds = hours * 3600 + minutes * 60 + seconds

    # Formatação para HH:MM:SS ou MM:SS
    h_f = total_seconds // 3600
    m_f = (total_seconds % 3600) // 60
    s_f = total_seconds % 60

    if h_f > 0:
        return f"{h_f:02d}:{m_f:02d}:{s_f:02d}"  # Formato HH:MM:SS
    else:
        return f"{m_f:02d}:{s_f:02d}"  # Formato MM:SS


def buscar_videos(entrada, num_results=None):
    global resultBuscas
    global table_data

    if num_results is None:
        max_results = 10
    else:
        max_results = num_results

    # Configurar a chave da API
    # NOTA: Certifique-se de que sua chave real seja válida.
    api_key = 'AIzaSyA8tSnXkr6f7wvZCF3FCDofkb_X1A8n2PI'
    if not api_key:
        raise ValueError("A chave da API do YouTube não está configurada. Defina YOUTUBE_API_KEY.")

    # Criar cliente da API do YouTube
    youtube = build('youtube', 'v3', developerKey=api_key)

    # 1. Realizando a pesquisa no YouTube (para obter os IDs)
    videos_search = youtube.search().list(
        q=entrada,
        part='snippet',
        type='video',
        maxResults=max_results
    )

    videos = videos_search.execute()
    table_data.clear()

    # Obter IDs dos vídeos para buscar detalhes (incluindo duração)
    video_ids = [video['id']['videoId'] for video in videos.get('items', [])]
    video_durations = {}

    # 2. Buscar detalhes dos vídeos (para obter a duração em contentDetails)
    if video_ids:
        video_details = youtube.videos().list(
            part='contentDetails,snippet',  # O 'contentDetails' é crucial para a duração
            id=','.join(video_ids)
        ).execute()

        # Armazena a duração no formato ISO 8601
        video_durations = {
            video['id']: video['contentDetails']['duration']
            for video in video_details.get('items', [])
        }

    # 3. Processar e formatar os resultados
    for video in videos.get('items', []):
        title = video['snippet']['title']
        video_id = video['id']['videoId']
        channel = video['snippet']['channelTitle']

        # OBTÉM DURAÇÃO ISO 8601 E CONVERTE PARA FORMATO LEGÍVEL
        iso_duration = video_durations.get(video_id, 'N/D')
        duration = converter_duracao_iso8601(iso_duration)  # <--- AQUI ESTÁ A MUDANÇA

        url = f"https://www.youtube.com/watch?v={video_id}"
        table_data.append([title, channel, duration, url])

    resultBuscas.extend(table_data)
    print(resultBuscas)

    return resultBuscas


# Exemplo de uso
if __name__ == "__main__":
    try:
        resultados = buscar_videos("sectio aurea", num_results=5)
        for video in resultados:
            print(f"Título: {video[0]}")
            print(f"Canal: {video[1]}")
            print(f"Duração: {video[2]}")
            print(f"URL: {video[3]}")
            print("-" * 50)
    except Exception as e:
        print(f"Erro ao buscar vídeos: {e}")