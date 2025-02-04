# Импорт модулей.
import telebot
from telebot import types
import config as cfg
import os
import text_messages as msg_txt
import button_mesages as btn_txt

bot = telebot.TeleBot(cfg.token_tg)
path = cfg.path
personal_data = ''
username_data = ''


# Реакция на команду старт и главный экран
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_main_info = types.KeyboardButton(btn_txt.btn_txt_main_info)
    btn_main_survey = types.KeyboardButton(btn_txt.btn_txt_main_survey)
    markup.add(btn_main_info, btn_main_survey)
    bot.send_message(message.chat.id, text=msg_txt.greening.format(message.from_user), reply_markup=markup)
    bot.send_message(message.chat.id, text='Информация о боте доступна по нажатиию команды /info', reply_markup=markup)


# Вывод команды инфо
@bot.message_handler(commands=['info'])
def start(message):
    global user_id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_info_info = types.KeyboardButton('Написать мне')
    markup.add(btn_info_info)
    bot.send_message(message.chat.id,
                     text=f'Для продолжения использования бота нажмите /start '.format(
                         message.from_user), reply_markup=markup)


# Основное тело бота
@bot.message_handler(content_types=['text'])
def func(message):
    # Вывод информации из вклаадки обо мне
    if message.text == btn_txt.btn_txt_main_info:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_info_portfolio = types.KeyboardButton(btn_txt.btn_txt_info_portfolio)
        btn_info_social = types.KeyboardButton(btn_txt.btn_txt_info_social)
        btn_info_main = types.KeyboardButton(btn_txt.btn_txt_info_main)
        markup.add(btn_info_portfolio, btn_info_social, btn_info_main)
        bot.send_message(message.chat.id, text=msg_txt.info_main_text, reply_markup=markup)

    # Ссылка на портфолио
    elif message.text == btn_txt.btn_txt_info_portfolio:
        bot.send_message(message.chat.id, text=msg_txt.info_portfolio_text)
    # Ссылки на социальные сети
    elif message.text == btn_txt.btn_txt_info_social:
        bot.send_message(message.chat.id, text=msg_txt.info_social_text)
    # Возврат на главную страницу
    elif message.text == btn_txt.btn_txt_info_main:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_main_info = types.KeyboardButton(btn_txt.btn_txt_main_info)
        btn_main_survey = types.KeyboardButton(btn_txt.btn_txt_main_survey)
        markup.add(btn_main_info, btn_main_survey)
        bot.send_message(message.chat.id, text=msg_txt.return_main_text)
        bot.send_message(message.chat.id, text=msg_txt.main_page_text, reply_markup=markup)

    # Разрешение на обработку персональных данных
    elif message.text == btn_txt.btn_txt_main_survey:
        keyboard = types.InlineKeyboardMarkup()
        key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
        keyboard.add(key_yes)
        key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
        keyboard.add(key_no)
        question = msg_txt.personal_data_agreement
        bot.send_message(message.chat.id, text=question, reply_markup=keyboard)

    elif message.text == btn_txt.btn_txt_photo_return:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_main_info = types.KeyboardButton(btn_txt.btn_txt_main_info)
        btn_main_survey = types.KeyboardButton(btn_txt.btn_txt_main_survey)
        markup.add(btn_main_info, btn_main_survey)
        bot.send_message(message.chat.id, text=msg_txt.return_main_text)
        bot.send_message(message.chat.id, text=msg_txt.main_page_text, reply_markup=markup)

    # Ввод неизвестной команды
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_main_page = btn_txt.btn_txt_info_main
        markup.add(btn_main_page)
        bot.send_message(message.chat.id, text=msg_txt.error_text, reply_markup=markup)


# Получение данных от пользователя и запрос фотографий
@bot.message_handler(content_types=['text'])
def get_personal_data(message):
    global path
    global personal_data
    global username_data
    username_data = message.from_user.username
    data_path = path + username_data
    list_data_path = os.listdir(path)
    if username_data in list_data_path:
        pass
    else:
        os.mkdir(data_path)
    personal_data = message.text
    medias = [types.InputMediaPhoto(open(cfg.photo_1, 'rb')), types.InputMediaPhoto(open(cfg.photo_2, 'rb')), types.InputMediaPhoto(open(cfg.photo_3, 'rb'))]
    bot.send_media_group(message.chat.id, medias)
    bot.send_message(message.chat.id, text='Загрузите фото как на примере выше')
    bot.register_next_step_handler(message, get_photos)
    with open(path + username_data + '/data.txt', 'w') as data_file:
        data_file.write(personal_data + ' ' + 't.me/' + username_data)


# загрузка фото
@bot.message_handler(content_types=['photo', 'document'])
def get_photos(message):
    try:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        return_btn = btn_txt.btn_txt_info_main
        markup.add(return_btn)
        global path
        global username_data
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = path + username_data + '/' + message.photo[1].file_id
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_message(message.chat.id, text='Данные загружены, спасибо', reply_markup=markup)
    except:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        photo_return = btn_txt.btn_txt_photo_return
        markup.add(photo_return)
        bot.send_message(message.chat.id, text=msg_txt.wrong_type, reply_markup=markup)


# Выбор согласия обработки персональных данных
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        global path
        global username_data
        markup = types.ReplyKeyboardRemove()
        bot.send_message(call.message.chat.id, text=msg_txt.personal_data_text, reply_markup=markup)
        bot.register_next_step_handler(call.message, get_personal_data)
    elif call.data == "no":
        bot.send_message(call.message.chat.id, text=msg_txt.personal_data_disagree)


if __name__ == '__main__':
    bot.polling(none_stop=True)
