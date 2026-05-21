import customtkinter as ctk
import threading
from tkinter import messagebox, filedialog
from downloader import get_video_info, download_video
import os

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class VideoDownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Video Downloader")
        self.geometry("600x450")

        # Set window icon if available
        icon_path = os.path.join(os.path.dirname(__file__), "app_icon.ico")
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)
            
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0) # Title
        self.grid_rowconfigure(1, weight=0) # Input
        self.grid_rowconfigure(2, weight=0) # Info
        self.grid_rowconfigure(3, weight=0) # Options
        self.grid_rowconfigure(4, weight=0) # Path Selection
        self.grid_rowconfigure(5, weight=0) # Progress
        self.grid_rowconfigure(6, weight=0) # Status

        # Title
        self.label_title = ctk.CTkLabel(self, text="Video Downloader", font=("Roboto", 24))
        self.label_title.grid(row=0, column=0, padx=20, pady=20)

        # Input Frame
        self.frame_input = ctk.CTkFrame(self)
        self.frame_input.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.frame_input.grid_columnconfigure(0, weight=1)

        self.entry_url = ctk.CTkEntry(self.frame_input, placeholder_text="Paste YouTube or TikTok link here")
        self.entry_url.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.btn_fetch = ctk.CTkButton(self.frame_input, text="Fetch Info", command=self.start_fetch_info)
        self.btn_fetch.grid(row=0, column=1, padx=10, pady=10)

        # Info Label (Hidden initially)
        self.label_info = ctk.CTkLabel(self, text="", font=("Roboto", 14))
        self.label_info.grid(row=2, column=0, padx=20, pady=5)

        # Options Frame
        self.frame_options = ctk.CTkFrame(self)
        self.frame_options.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        self.frame_options.grid_columnconfigure(0, weight=1)
        self.frame_options.grid_columnconfigure(1, weight=1)

        self.radio_var = ctk.IntVar(value=0)
        self.radio_video = ctk.CTkRadioButton(self.frame_options, text="Video + Audio", variable=self.radio_var, value=0, command=self.update_options)
        self.radio_video.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.radio_video_silent = ctk.CTkRadioButton(self.frame_options, text="Video (No Audio)", variable=self.radio_var, value=2, command=self.update_options)
        self.radio_video_silent.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.radio_audio = ctk.CTkRadioButton(self.frame_options, text="Audio Only", variable=self.radio_var, value=1, command=self.update_options)
        self.radio_audio.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # Format Selection
        self.label_format = ctk.CTkLabel(self.frame_options, text="Format:")
        self.label_format.grid(row=2, column=0, padx=10, pady=(10,0), sticky="e")
        
        self.option_format = ctk.CTkOptionMenu(self.frame_options, values=["mp4", "webm"])
        self.option_format.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Resolution Selection
        self.label_res = ctk.CTkLabel(self.frame_options, text="Resolution:")
        self.label_res.grid(row=3, column=0, padx=10, pady=(10,0), sticky="e")

        self.option_resolution = ctk.CTkOptionMenu(self.frame_options, values=["Best"])
        self.option_resolution.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        # Path Selection Frame
        self.frame_path = ctk.CTkFrame(self)
        self.frame_path.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        self.frame_path.grid_columnconfigure(0, weight=1)

        self.entry_path = ctk.CTkEntry(self.frame_path, placeholder_text="Select download folder")
        self.entry_path.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.entry_path.insert(0, os.getcwd()) # Default to current dir

        self.btn_browse = ctk.CTkButton(self.frame_path, text="Browse", command=self.browse_folder)
        self.btn_browse.grid(row=0, column=1, padx=10, pady=10)

        self.btn_download = ctk.CTkButton(self, text="Download", command=self.start_download, state="disabled")
        self.btn_download.grid(row=5, column=0, padx=20, pady=20)

        # Progress
        self.progressbar = ctk.CTkProgressBar(self)
        self.progressbar.grid(row=6, column=0, padx=20, pady=10, sticky="ew")
        self.progressbar.set(0)

        self.label_status = ctk.CTkLabel(self, text="Ready")
        self.label_status.grid(row=7, column=0, padx=20, pady=10)

        self.video_data = None

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.entry_path.delete(0, "end")
            self.entry_path.insert(0, folder_selected)

    def start_fetch_info(self):
        url = self.entry_url.get()
        if not url:
            messagebox.showerror("Error", "Please enter a URL")
            return

        self.label_status.configure(text="Fetching info...")
        self.btn_fetch.configure(state="disabled")
        
        thread = threading.Thread(target=self.fetch_info_thread, args=(url,))
        thread.start()

    def fetch_info_thread(self, url):
        self.video_data = get_video_info(url)
        self.after(0, self.update_ui_after_fetch)

    def update_ui_after_fetch(self):
        self.btn_fetch.configure(state="normal")
        if not self.video_data or 'error' in self.video_data:
            self.label_status.configure(text="Error fetching info")
            messagebox.showerror("Error", self.video_data.get('error', 'Unknown error'))
            return

        title = self.video_data.get('title', 'Unknown')
        self.label_info.configure(text=f"Found: {title[:50]}...")
        self.label_status.configure(text="Ready to download")
        self.btn_download.configure(state="normal")

        # Update resolutions
        resolutions = self.video_data.get('resolutions', [])
        if resolutions:
            self.option_resolution.configure(values=resolutions)
            self.option_resolution.set(resolutions[0])
        else:
            self.option_resolution.configure(values=["Best"])
            self.option_resolution.set("Best")

    def update_options(self):
        mode = self.radio_var.get()
        if mode == 1: # Audio Only
             self.option_resolution.configure(state="disabled")
             self.option_format.configure(state="disabled") # Usually mp3 is preferred for audio only
        else:
             self.option_resolution.configure(state="normal")
             self.option_format.configure(state="normal")

    def start_download(self):
        if not self.video_data:
            return

        url = self.video_data.get('webpage_url')
        if not url:
             url = self.entry_url.get() # Fallback

        output_path = self.entry_path.get()
        if not output_path or not os.path.exists(output_path):
            messagebox.showerror("Error", "Invalid download path")
            return
        
        mode = self.radio_var.get()
        # 0: Video+Audio, 1: Audio Only, 2: Video (No Audio)
        
        dl_type = 'video'
        if mode == 1:
            dl_type = 'audio'
        elif mode == 2:
            dl_type = 'video_no_audio'

        options = {
            'type': dl_type,
            'resolution': self.option_resolution.get(),
            'format': self.option_format.get(),
            'output_path': output_path
        }

        self.label_status.configure(text="Downloading...")
        self.btn_download.configure(state="disabled")
        self.progressbar.set(0)

        thread = threading.Thread(target=self.download_thread, args=(url, options))
        thread.start()

    def download_thread(self, url, options):
        def progress_callback(percent, eta):
            self.after(0, lambda: self.update_progress(percent, eta))

        result = download_video(url, options, progress_callback)
        self.after(0, lambda: self.download_finished(result))

    def update_progress(self, percent, eta):
        self.progressbar.set(percent / 100)
        self.label_status.configure(text=f"Downloading: {percent:.1f}% (ETA: {eta})")

    def download_finished(self, result):
        self.btn_download.configure(state="normal")
        if result.get('status') == 'success':
            self.label_status.configure(text="Download Complete!")
            self.progressbar.set(1)
            messagebox.showinfo("Success", "Download completed successfully!")
        else:
            self.label_status.configure(text="Error")
            messagebox.showerror("Error", result.get('message', 'Unknown error'))

if __name__ == "__main__":
    app = VideoDownloaderApp()
    app.mainloop()
