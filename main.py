
import telebot
import os
import shutil
import sqlite3


from readTXT import Txt
from instadownloader import Downloader
from soundcloudDownloader import SoundCloud



database = "Downloadmen.db"
conn = sqlite3.connect(database,check_same_thread=True)
cursor = conn.cursor()
cursor.execute("""
CREATE Table if not exists download(
               id INTEGER PRIMARY KEY,
               chatid TEXT,
               url TEXT
                );

""")   
conn.commit()
conn.close()





token = "7941633129:AAElRQPa_NsRiWJtmiO5bOGYWaNm94e7MaA"
bot = telebot.TeleBot(token , threaded=True ,num_threads=5)



@bot.message_handler(commands=['start'])
def start(msg):
    welcome ="""

Hey buddy, welcome to the downloader bot! Just send me the link you have, and I'll download it for you 🤖

Platforms I can download from so far:
▪️ Instagram
▪️ Soundcloud

"""

    try:
        bot.reply_to(msg , welcome)
        
        conn = sqlite3.connect(database,check_same_thread=True)
        cursor = conn.cursor()
        cursor.execute("""
    INSERT INTO download (chatid , url) values (?,?)
    """,(msg.chat.id , " "))
        conn.commit()
        conn.close()
    except:
        bot.reply_to(msg , welcome)

@bot.message_handler(regexp="https://www.instagram.com")
def instagram(message):

    try:
        reelUrl = message.text
        


        #Download instagram reel
        post = Downloader()
        sent_message = bot.reply_to(message,"Downloading...")
        downloadedPost = post.download(reelUrl)
        print(downloadedPost)
       

       
        code =str(reelUrl).split('/')[-2]
        if downloadedPost == True:

            #read instagram caption
            caption = Txt()
            readCaption = caption.read(f"{code}/")
            ############################################

            #sned the video
            for i in os.listdir():
                if i.endswith(".mp4"):
                    if os.path.exists(i) and os.path.getsize(i) > 0:
                        with open(i, 'rb') as video:
                            bot.send_video(message.chat.id, video , caption=f"{readCaption} \n made BY : @DownloadMenbot")
            bot.delete_message(message.chat.id, sent_message.message_id)

            #delete the downloaded video
            os.chdir("..")
            shutil.rmtree(f"{code}/")

            conn = sqlite3.connect(database,check_same_thread=True)
            cursor = conn.cursor()
            cursor.execute("""
UPDATE download SET url = ? WHERE chatid = ?
""",(f"{message.text} , " , message.chat.id))
            conn.commit()
            conn.close()


        else:
            bot.reply_to(message , "there is a problem!")
    except  Exception as e:
        bot.reply_to(message , "there is a problem!")
        print(e)




@bot.message_handler(regexp="https://soundcloud")
def soundcloud(message):
    try:
        bot.reply_to(message , "downloading...")

        #download soundCloud track 
        sound = SoundCloud()
        download = sound.soundDownloader(track=message.text)

        #find and send the track
        for i in os.listdir():
            if i.startswith(download):
                splitCode = i.split("-")[-1]
                code = download + "-" + splitCode
                if os.path.exists(code) and os.path.getsize(code) > 0:
                        bot.send_audio(message.chat.id , caption="made By @DownloadMenbot"  , audio=open(code, 'rb'))



        os.remove(code)
    except:
        bot.reply_to(message , "there is a problem please try agian!")
    





if __name__ == "__main__":
    print("Bot ins running...")
    bot.infinity_polling()

