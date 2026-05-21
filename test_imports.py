try:
    import customtkinter
    import yt_dlp
    import PIL
    import requests
    print("Imports successful")
except ImportError as e:
    print(f"Import failed: {e}")
    exit(1)
