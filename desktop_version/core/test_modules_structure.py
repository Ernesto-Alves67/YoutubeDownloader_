#!/usr/bin/env python3
"""
Test script to verify that all required modules exist and have correct structure.
This tests the module structure without requiring external dependencies.
"""

import sys
import os
import ast


def test_module_exists(module_path):
    """Test if a module file exists and is syntactically correct"""
    if not os.path.exists(module_path):
        return False, f"Module {module_path} does not exist"
    
    try:
        with open(module_path, 'r') as f:
            content = f.read()
        
        # Parse the Python code to check syntax
        ast.parse(content)
        return True, "Module exists and has valid syntax"
    
    except SyntaxError as e:
        return False, f"Syntax error in {module_path}: {e}"
    except Exception as e:
        return False, f"Error reading {module_path}: {e}"


def test_module_has_class_or_function(module_path, target_name):
    """Test if a module contains a specific class or function"""
    try:
        with open(module_path, 'r') as f:
            content = f.read()
        
        # Parse and look for the target
        tree = ast.parse(content)
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
                if node.name == target_name:
                    return True, f"Found {target_name} in {module_path}"
        
        return False, f"{target_name} not found in {module_path}"
    
    except Exception as e:
        return False, f"Error checking {module_path}: {e}"


def main():
    """Test all required modules"""
    print("YouTube Downloader Module Structure Test")
    print("=" * 50)
    
    # Define tests: (module_path, expected_class_or_function)
    tests = [
        ("downloader/__init__.py", None),
        ("downloader/audio_downloader.py", "AudioDownloader"),
        ("downloader/buscas.py", "buscar_videos"),
        ("ui/__init__.py", None),
        ("ui/ui_ytdownloader.py", "Ui_MainWindow"),
        ("ui/dialogs.py", "SobreDialog"),
        ("ui/menu.py", "MenuMixin"), 
        ("actions/__init__.py", None),
        ("actions/audio_actions.py", "AudioActions"),
    ]
    
    passed = 0
    total = len(tests)
    
    for module_path, target in tests:
        print(f"\nTesting {module_path}...")
        
        # Test if module exists and has valid syntax
        exists, msg = test_module_exists(module_path)
        if not exists:
            print(f"  ✗ {msg}")
            continue
        else:
            print(f"  ✓ Module exists and has valid syntax")
        
        # Test if it has the expected class/function (if specified)
        if target:
            has_target, msg = test_module_has_class_or_function(module_path, target)
            if has_target:
                print(f"  ✓ {msg}")
                passed += 1
            else:
                print(f"  ✗ {msg}")
        else:
            print(f"  ✓ Init file OK")
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ ALL MODULES CREATED SUCCESSFULLY!")
        print("\nModule structure is correct. The download functionality should now work")
        print("when the required dependencies (pytube, moviepy, PySide6, etc.) are installed.")
        print("\nNext steps:")
        print("1. Install dependencies: pip install pytube moviepy PySide6 youtube-search-python pygame")
        print("2. Run the application: python3 ytdl_main.py")
        print("3. Test the 'Baixar' button functionality")
        return True
    else:
        print("✗ Some modules are missing or incomplete.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)