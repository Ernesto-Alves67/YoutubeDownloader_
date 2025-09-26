"""
YouTube search functionality module
"""

from youtubesearchpython import VideosSearch
import re


def buscar_videos(query, max_results=10):
    """
    Search for YouTube videos using the provided query
    
    Args:
        query (str): Search query
        max_results (int): Maximum number of results to return
        
    Returns:
        list: List of videos with format [title, channel, duration, url]
    """
    try:
        print(f"Buscando vídeos para: {query}")
        
        videos_search = VideosSearch(query, limit=max_results)
        results = videos_search.result()
        
        video_list = []
        
        for video in results['result']:
            title = video.get('title', 'Unknown Title')
            channel = video.get('channel', {}).get('name', 'Unknown Channel')
            duration = video.get('duration', 'Unknown Duration')
            url = video.get('link', '')
            
            # Clean up title to remove problematic characters for filename  
            clean_title = clean_filename(title)
            
            video_info = [clean_title, channel, duration, url]
            video_list.append(video_info)
            
        print(f"Encontrados {len(video_list)} vídeos")
        return video_list
        
    except Exception as e:
        print(f"Error in buscar_videos: {str(e)}")
        return []


def clean_filename(filename):
    """
    Clean filename to remove problematic characters
    
    Args:
        filename (str): Original filename
        
    Returns:
        str: Cleaned filename
    """
    # Remove or replace problematic characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    filename = re.sub(r'[|┃]', ' ', filename)
    filename = filename.replace('(', '').replace(')', '')
    
    # Limit length
    if len(filename) > 50:
        filename = filename[:50]
    
    # Remove extra spaces
    filename = ' '.join(filename.split())
    
    return filename