from youtubesearchpython import VideosSearch

table_data = [] # lista temporaria para guardar resultados
resultBuscas = []
arquivos_mp3 = []


def buscar_videos(entrada, num_results = None):
    global resultBuscas
    global table_data
    
    if num_results is None:
        max_results = 10 # Número máximo de resultados a serem retornados
    else:
        max_results = num_results
        
    videos_search = VideosSearch(entrada, limit=max_results)# Realizando a pesquisa no YouTube
    videos = videos_search.result() # Obtendo os resultados da pesquisa
    table_data.clear()

    if(num_results is not None):
        videos_search.next()
        videos = videos_search.result() # Obtendo os resultados da pesquisa
        table_data.clear()
        for video in videos['result']: # Extraindo informações dos resultados da pesquisa
            title = video['title']
            video_id = video['id']
            channel = video['channel']['name']
            duration = video['duration']
            views = video['viewCount']['short']
            url = video['link']
            table_data.append([title, channel, duration, url])
        resultBuscas.extend(table_data)
    else:
        for video in videos['result']: # Extraindo informações dos resultados da pesquisa
            title = video['title']
            video_id = video['id']
            channel = video['channel']['name']
            duration = video['duration']
            views = video['viewCount']['short']
            url = video['link']
            table_data.append([title, channel, duration, url])
        resultBuscas.extend(table_data)
 
    return resultBuscas

