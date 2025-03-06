import instaloader


class Downloader:
    def __init__(self):
        pass
    def download(self,link : str) -> bool:
        print(link)
        try:
            print("download...")

            insta = instaloader.Instaloader()

            reelURL = link
            shortcode = reelURL.split('/')[-2]
            post = instaloader.Post.from_shortcode(insta.context, shortcode)

            downloadedPost = insta.download_post(post, target=shortcode)
            return downloadedPost
        except Exception as e:
            print(e)        
        