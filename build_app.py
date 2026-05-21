import PyInstaller.__main__
import customtkinter
import os
import shutil

# Clean previous builds
if os.path.exists('build'):
    shutil.rmtree('build')
if os.path.exists('dist'):
    shutil.rmtree('dist')

import imageio_ffmpeg

# Get customtkinter path for add-data
ctk_path = os.path.dirname(customtkinter.__file__)
# Get ffmpeg path
ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

print("Building Video Downloader...")

PyInstaller.__main__.run([
    'main.py',
    '--name=VideoDownloader',
    '--onefile',
    '--noconsole',
    '--icon=app_icon.ico',
    f'--add-data={ctk_path};customtkinter/',
    f'--add-data={ffmpeg_path};imageio_ffmpeg/binaries',
    '--add-data=app_icon.ico;.',  # Ensure icon is available for runtime
    '--collect-all=customtkinter',
])

print("Build complete. Executable is in dist/VideoDownloader.exe")
