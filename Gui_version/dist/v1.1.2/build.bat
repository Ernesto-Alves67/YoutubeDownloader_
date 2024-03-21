@echo off


pyinstaller --hidden-import=PyQt5 --hidden-import=threading --hidden-import=time --hidden-import=pytube --hidden-import=moviepy.editor --hidden-import=os --hidden-import=sys --hidden-import=youtubesearchpython --hidden-import=pygame --add-data "buscas.py;." --add-data "ui_ytdownloader.py;." --add-data "icons\*;icons" ytdl_main.py
