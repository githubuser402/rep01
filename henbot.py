import telebot
import sqlite3
from random import choice
#C:/Users/KOSE/Desktop/hbot/

def Bot():
    @bot.message_handler(commands = ['start'])
    def st(message):
        bot.send_message(message.chat.id, 'Це мій невеликий проект, темою якого є хентай-бот. \nБот не має обмежень по кількості тегів. \nКатеорії: \n#ass \n#pussy \n#tits \n#legs \n#neko \n#cute \n#toys \n#penetration \n#anal \n#furry \n#milf \n#creampie \n#ero \nВказівка до використання: категорії потрібно вказувати, розділивши їх пропуском, не використовувати інших знаків.')
    
    @bot.message_handler(content_types = ['photo'])
    def get_file(message):
        if str(message.chat.id) == '559592369':
            if message.caption != None:
                conn = sqlite3.connect('henbot.db')
                cursor = conn.cursor()
                inscr = sorted(set(message.caption.split(' ')))
                file_info = bot.get_file(message.photo[-1].file_id)
                path = file_info.file_path.split('/')[-1][:-3] + 'txt'
                
                file_d = bot.download_file(file_info.file_path)
                with open(p_path + path, 'wb') as f:
                    f.write(file_d)
                    
                cursor.execute('''INSERT INTO files(file_path) VALUES(?)''', (path,))
                conn.commit()
                l_n = cursor.execute('''SELECT f_id FROM files ORDER BY f_id DESC LIMIT 1''')
                conn.commit()
                last_num = l_n.fetchall()
                
                for i in inscr:
                    cursor.execute('''INSERT INTO linking(f_id, t_id) VALUES(?, ?);''', (last_num[0][0], tags[i]))
                    conn.commit()
                bot.reply_to(message, 'Фото отримано')
                conn.close()
                
    @bot.message_handler(content_types = ['text'])
    def send_file(message):
        pass
        
if __name__ == '__main__':
    p_path = 'D:/My_packages/Pyprojects/hbot/h_files/'
    bot = telebot.TeleBot('990227536:AAFxnAsTEwCLrFjRsQ-RfpxCAhLAEVCiRao')
    tags = {'#ass':1, '#pussy':2, '#tits':3, '#legs':4, '#neko':5, '#cute':6, '#toys':7, '#penetration':8, '#anal':9, '#furry':10, '#milf':11, '#creampie':12, '#ero':13}
    Bot()
    bot.polling()