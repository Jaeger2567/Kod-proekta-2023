import telebot
from icrawler.builtin import GoogleImageCrawler
import os
import zipfile
import glob

TOKEN = "5830855805:AAFXxQG0uX7AOYRSNZ0H4e4B6-VvzYwLcR4"
bot = telebot.TeleBot(TOKEN)


#Тут будет сохранена информация, которую мы получим в ходе диалога с ботом
user_data = {
    'slovo': '',
    'kolvo': ''
}
user_data['kolvo'] = int()


#Собираем нужную информацию для поиска
@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/start':
        bot.send_message(message.from_user.id, "Привет!\nЯ Search_Picture_Bot, Бот созданный для поиска изображений.\nКакое изображение Вы хотите найти?")
        bot.register_next_step_handler(message, get_slovo)
    else:
        bot.send_message(message.from_user.id, 'Напиши /start')


def get_slovo(message):
    user_data['slovo'] = message.text
    bot.send_message(message.from_user.id, 'Сколько изображений должно быть?')
    bot.register_next_step_handler(message, get_rezultat)


def get_rezultat(message):
    user_data['kolvo'] = int(message.text)
    bot.send_message(message.chat.id, 'Сейчас найду : )')

#Удаляем уже имеющиеся файлы в папке
    removing_files = glob.glob('D:/Documents/Desktop/Python/Питон/Практики/Проект/Изображения/*.*g')
    for i in removing_files:
        os.remove(i)

#Ищем и сохраняем нужные нам изображения
    google = GoogleImageCrawler(storage={'root_dir': 'D:\Documents\Desktop\Python\Питон\Практики\Проект\Изображения'})
    google.crawl(keyword=user_data['slovo'], max_num=user_data['kolvo'])
    os.chdir('D:\Documents\Desktop\Python\Питон\Практики\Проект')

#Архивируем изображения для отправки их пользователю
    zip_file = zipfile.ZipFile('Готовые_фото.zip', 'w')
    for root, dirs, files in os.walk('Изображения'):
        for file in files:
            zip_file.write(os.path.join(root,file))
    zip_file.close()

    #Путь в котором сохраняется архив
    doc = open('D:/Documents/Desktop/Python/Питон/Практики/Проект/Готовые_фото.zip', 'rb')
    bot.send_document(message.chat.id, doc)


bot.polling(none_stop=True, interval=1)
