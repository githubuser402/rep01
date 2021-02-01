import telebot
import sqlite3
from random import choice
from config import p_path, TOKEN, db_path, users, admin_id, tags, start_message
'''в файлі config знаходиться каталог, в якому знаходяться фотографії,
ідентифікатор бота, шлях до бази даних, шлях до файлу з запитами користувачів, теги, стартове сповіщення'''

def Bot():
    @bot.message_handler(commands = ['start'])
    def st(message):
        bot.send_message(message.chat.id, start_message)
    
    @bot.message_handler(content_types = ['photo'])
    def get_file(message):
        if str(message.chat.id) == admin_id:
            if message.caption != None:
                conn = sqlite3.connect(db_path)#відкриття бази даних
                cursor = conn.cursor()
                file_info = bot.get_file(message.photo[-1].file_id)#інформація про файл
                file_num = file_info.file_id[-10:]#десять останніх цифр ідентифікатора знімка
                inscr = sorted(set(message.caption.split(' ')))
                b = False
                sql = cursor.execute('''SELECT file_id FROM files''')
                conn.commit()
                
                #перевірка належності файлу до бази даних
                for i in sql.fetchall():
                    if i[0] == file_num:
                        b = True
                
                #Якщо b - False, то знімка немаж в базі даних
                if b == False:
                    path = file_info.file_path.split('/')[-1][:-3] + 'txt'
                    #завантаження файлу
                    file_d = bot.download_file(file_info.file_path)
                    with open(p_path + path, 'wb') as f:
                        f.write(file_d)
                    #додавання шляху файлу в базу даних
                    cursor.execute('''INSERT INTO files(file_path, file_id) VALUES(?, ?)''', (path, file_num))
                    conn.commit()
                    l_n = cursor.execute('''SELECT f_id FROM files ORDER BY f_id DESC LIMIT 1''')
                    conn.commit()
                    last_num = l_n.fetchall()
                    #додавання тегів в базу даних
                    for i in inscr:
                        cursor.execute('''INSERT INTO linking(f_id, t_id) VALUES(?, ?);''', (last_num[0][0], tags[i]))
                        conn.commit()
                    bot.reply_to(message, 'Фото отримано, шлях: {0}'.format(path))
                    
                elif b == True:
                    bot.reply_to(message, 'Фото вже наявне в базі даних')
                    
                #закриття бази даних
                conn.close()
                
    @bot.message_handler(content_types = ['text'])
    def send_file(message):
        conn = sqlite3.connect(db_path)#відкриття бази даних
        cursor = conn.cursor()
        user_tags = sorted(set(message.text.split(' ')))#сортування, видалення дублікатів
        req_tags = ''
        #видалення неіснуючих тегів
        for t in user_tags:
            if t in tags:
                req_tags += t
            
        #запис інформації про користувача с текстовий файл 
        with open(users, 'a') as user_info:
            user_info.write(message.chat.first_name + '|' + str(message.chat.id) + '|' + req_tags + '\n')
            
        #запит в базу даних
        sql = cursor.execute('''SELECT files.file_path, group_concat(tags.tag, '') FROM files
                                          JOIN linking ON linking.f_id = files.f_id
                                          JOIN tags ON linking.t_id = tags.t_id
                                          GROUP BY files.f_id''')
        conn.commit()
        
        #массив шляхів до файлів з необхідним тегом
        file_paths = [i[0] for i in sql.fetchall() if req_tags in i[1]]
        
        if len(file_paths) != 0:
            fp = choice(file_paths)
            with open(p_path + fp, 'rb') as f:
                bot.send_photo(message.chat.id, f)
        else:
            bot.send_message(message.chat.id, 'Фото з таким тегом поки немає в базі даних')
        
        #закриття бази даних
        conn.close()
        
if __name__ == '__main__':
    bot = telebot.TeleBot(TOKEN)
    Bot()
    bot.polling()