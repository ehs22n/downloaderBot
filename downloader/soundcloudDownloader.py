import youtube_dl
import os



class SoundCloud:
    def __init__(self):
        
        pass

    def soundDownloader(self , track):
        
        track_url = track

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',
            'noplaylist': False,
        }


        
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(track_url ,download=False)
            title = info.get("title" , "u title")
            ydl.download([track_url])
            return title