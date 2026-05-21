import PyInstaller.__main__
import os
import shutil

# Ensure dist/VideoDownloader.exe exists from previous build
if not os.path.exists('dist/VideoDownloader.exe'):
    print("Error: dist/VideoDownloader.exe not found. Run build_app.py first.")
    exit(1)

print("Building Installer...")

PyInstaller.__main__.run([
    'installer_script.py',
    '--name=Install_VideoDownloader',
    '--onefile',
    '--noconsole',
    '--icon=app_icon.ico',
    '--add-data=dist/VideoDownloader.exe;.', # Embed the main app exe
    '--clean',
])

print("Installer build complete. Executable is in dist/Install_VideoDownloader.exe")
