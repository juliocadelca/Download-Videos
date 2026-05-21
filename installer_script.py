import os
import sys
import shutil
import winshell
from win32com.client import Dispatch
import tkinter as tk
from tkinter import messagebox
import subprocess

APP_NAME = "VideoDownloader"
EXE_NAME = "VideoDownloader.exe"

def create_shortcut(target_path, shortcut_path):
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = target_path
    shortcut.WorkingDirectory = os.path.dirname(target_path)
    shortcut.IconLocation = target_path # The exe itself acts as the icon source
    shortcut.save()

def install():
    # 1. Define Install Path (%LOCALAPPDATA%/VideoDownloader)
    local_app_data = os.environ.get('LOCALAPPDATA')
    if not local_app_data:
        local_app_data = os.path.expanduser("~/AppData/Local")
    
    install_dir = os.path.join(local_app_data, APP_NAME)
    
    # 2. Extract embedded EXE
    # PyInstaller extracts to sys._MEIPASS
    if hasattr(sys, '_MEIPASS'):
        # When added with --add-data "dist/VideoDownloader.exe;." it sits in root of _MEIPASS
        source_exe = os.path.join(sys._MEIPASS, EXE_NAME)
    else:
        # Dev mode: assume it's in the current directory or dist
        source_exe = os.path.join(os.getcwd(), EXE_NAME)
        if not os.path.exists(source_exe) and os.path.exists(os.path.join("dist", EXE_NAME)):
             source_exe = os.path.join("dist", EXE_NAME)

    if not os.path.exists(source_exe):
        messagebox.showerror("Error", f"Installer corrupted: Source file not found at {source_exe}")
        return

    try:
        if not os.path.exists(install_dir):
            os.makedirs(install_dir)
        
        dest_exe = os.path.join(install_dir, EXE_NAME)
        
        # Copy file
        shutil.copy2(source_exe, dest_exe)
        
        # 3. Create Desktop Shortcut
        desktop = winshell.desktop()
        shortcut_path = os.path.join(desktop, f"{APP_NAME}.lnk")
        create_shortcut(dest_exe, shortcut_path)
        
        messagebox.showinfo("Success", f"{APP_NAME} installed successfully!\nA shortcut has been created on your Desktop.")
        
        # Open the app
        subprocess.Popen([dest_exe])
        
    except Exception as e:
        messagebox.showerror("Installation Failed", str(e))

if __name__ == "__main__":
    # Hide console window if possible (managed by pyinstaller --noconsole)
    root = tk.Tk()
    root.withdraw() # Hide main window
    
    result = messagebox.askyesno("Install Video Downloader", "Do you want to install Video Downloader and create a desktop shortcut?")
    if result:
        install()
