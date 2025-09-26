#!/usr/bin/env python3
"""
Simple launcher script for the YouTube Downloader GUI application.
This script checks dependencies and provides helpful error messages.
"""

import sys
import subprocess
import importlib

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        ('pytube', 'pytube'),
        ('moviepy', 'moviepy'),
        ('PySide6', 'PySide6'), 
        ('youtubesearchpython', 'youtube-search-python'),
        ('pygame', 'pygame')
    ]
    
    missing_packages = []
    
    for package_name, pip_name in required_packages:
        try:
            importlib.import_module(package_name)
            print(f"✓ {package_name}")
        except ImportError:
            print(f"✗ {package_name} (missing)")
            missing_packages.append(pip_name)
    
    if missing_packages:
        print(f"\nMissing packages. Install with:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def main():
    """Main function to run the application"""
    print("YouTube Downloader GUI v1.1.2")
    print("=" * 40)
    
    print("Checking dependencies...")
    if not check_dependencies():
        print("\n✗ Please install missing dependencies before running the application.")
        return 1
    
    print("\n✓ All dependencies satisfied!")
    print("Starting YouTube Downloader GUI...")
    
    try:
        # Import and run the main application
        from ytdl_main import MyMainWindow, QApplication
        import os
        
        app = QApplication(sys.argv)
        
        # Set application icon if available
        icon_path = os.path.join("icons", "app-64.png")
        if os.path.exists(icon_path):
            from PySide6 import QtGui
            app.setWindowIcon(QtGui.QIcon(icon_path))
        
        window = MyMainWindow()
        window.show()
        
        print("✓ Application started successfully!")
        print("You can now:")
        print("  1. Search for YouTube videos")
        print("  2. Select a video from the results")
        print("  3. Click 'Baixar' to download")
        
        return app.exec()
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        print("Make sure you're running this from the correct directory (Gui_version/v1.1.2)")
        return 1
    except Exception as e:
        print(f"✗ Error starting application: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())