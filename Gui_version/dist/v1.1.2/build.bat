@echo off


pyinstaller --hidden-import=PyQt5 --hidden-import=threading --hidden-import=time --hidden-import=pytube --hidden-import=moviepy.editor --hidden-import=os --hidden-import=sys --hidden-import=youtubesearchpython --hidden-import=pygame --add-data "YtDloader.py;." --add-data "menu.py;." --add-data "icons\*;icons" menuteste.py
