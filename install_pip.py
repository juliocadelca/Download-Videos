import urllib.request
import subprocess
import sys
import os

def install_pip():
    url = "https://bootstrap.pypa.io/get-pip.py"
    file_path = "get-pip.py"
    
    print(f"Downloading {url}...")
    try:
        urllib.request.urlretrieve(url, file_path)
        print("Downloaded get-pip.py")
    except Exception as e:
        print(f"Failed to download get-pip.py: {e}")
        return

    print("Installing pip...")
    try:
        subprocess.check_call([sys.executable, file_path])
        print("pip installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install pip: {e}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == "__main__":
    install_pip()
