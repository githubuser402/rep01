import telebot
import sqlite3
from random import choice
#C:/Users/KOSE/Desktop/hbot/

def Bot():
    @bot.message_handler(commands = ['start'])
    def st(message):
        bot.send_message(message.chat.id, 'Хентай-бот, ось теги: \n #neko \n #milf \n #ass \n #tits \n #milf \n #guro')
    
    @bot.message_handler(content_types = ['photo'])
    def get_tag(message):
        if str(message.chat.id) == '559592369' and 'тег:' in message.caption.lower():
            if message.caption != None:
                m = message.caption[4:].strip()
                if m in tags:
                    conn = sqlite3.connect('henbot.db')
                    cursor = conn.cursor()
                    file_info = bot.get_file(message.photo[-1].file_id)
                    path = file_info.file_path.split('/')[-1][:-4] + '.txt'
                    d_file = bot.download_file(file_info.file_path)
                    file = open(p_path + path, 'wb')
                    file.write(d_file)
                    file.close()
                    cursor.execute('''INSERT INTO txtph(file_path, tag) VALUES(?, ?);''', (path, m))
                    conn.commit()
                    conn.close()
            else:
                bot.reply_to(message, 'Фото без підпису')
    
    @bot.message_handler(content_types = ['text'])
    def send_file(message):
        tag = message.text.strip()
        if tag in tags:
            try:
                conn = sqlite3.connect('henbot.db')
                cursor = conn.cursor()
                p_arr = cursor.execute('''SELECT file_path FROM txtph WHERE tag = ?;''', (tag,))
                conn.commit()
                photo_path = choice(p_arr.fetchall())
                print(photo_path[0])
                with open(p_path + photo_path[0], 'rb') as f:
                    p = f.read()
                    bot.send_photo(message.chat.id, p)
            except:
                bot.send_message(message.chat.id, 'Тут поки пусто')
            finally:
                conn.close()
        
if __name__ == '__main__':
    p_path = 'C:/Users/KOSE/Desktop/hbot/h_files/'
    bot = telebot.TeleBot('990227536:AAFxnAsTEwCLrFjRsQ-RfpxCAhLAEVCiRao')
    tags = ['#neko', '#ass', '#tits', '#milf', '#guro']
    Bot()
    bot.polling()