import yt_dlp
import os

import imageio_ffmpeg

def get_video_info(url):
    """
    Fetches video metadata including title, thumbnail, and available formats.
    """
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'simulate': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Filter formats to unique resolutions for video
            formats = []
            seen_resolutions = set()
            
            for f in info.get('formats', []):
                if f.get('vcodec') != 'none' and f.get('resolution') and f.get('height'):
                    res = f"{f['height']}p"
                    if res not in seen_resolutions:
                        formats.append(res)
                        seen_resolutions.add(res)
            
            # Sort resolutions (numerically descending)
            formats.sort(key=lambda x: int(x[:-1]), reverse=True)
            
            return {
                'title': info.get('title', 'Unknown Title'),
                'thumbnail': info.get('thumbnail'),
                'duration': info.get('duration'),
                'resolutions': formats,
                'webpage_url': info.get('webpage_url'),
                'extractor': info.get('extractor')
            }
    except Exception as e:
        return {'error': str(e)}

def download_video(url, options, progress_callback=None):
    """
    Downloads video or audio based on options.
    options: {
        'type': 'video' or 'audio',
        'resolution': '720p', '1080p', etc. (ignored if audio),
        'output_path': 'path/to/save'
    }
    """
    
    def my_hook(d):
        if d['status'] == 'downloading':
            if progress_callback:
                try:
                    p = d.get('_percent_str', '0%').replace('%','')
                    progress_callback(float(p), d.get('_eta_str', 'Unknown'))
                except:
                    pass
        elif d['status'] == 'finished':
            if progress_callback:
                progress_callback(100.0, "Processing...")

    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
    
    ydl_opts = {
        'outtmpl': os.path.join(options.get('output_path', '.'), '%(title)s.%(ext)s'),
        'progress_hooks': [my_hook],
        'quiet': True,
        'no_warnings': True,
        'ffmpeg_location': ffmpeg_path,
    }

    if options['type'] == 'audio':
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    else:
        # Video download
        target_format = options.get('format', 'mp4')
        res = options.get('resolution', 'best')
        
        format_str = ""
        if res == 'best':
            if options['type'] == 'video_no_audio':
                format_str = 'bestvideo'
            else:
                format_str = 'bestvideo+bestaudio/best'
        else:
            # removing 'p' from resolution string '720p' -> '720'
            height = res.replace('p', '')
            if options['type'] == 'video_no_audio':
                format_str = f'bestvideo[height<={height}]/bestvideo'
            else:
                format_str = f'bestvideo[height<={height}]+bestaudio/best[height<={height}]/best'
        
        ydl_opts['format'] = format_str

        # Enforce Output Format
        ydl_opts['merge_output_format'] = target_format
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': target_format,
        }]

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return {'status': 'success'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

if __name__ == "__main__":
    # Test
    info = get_video_info("https://www.youtube.com/watch?v=BaW_jenozKc") # Example video
    print(info)
