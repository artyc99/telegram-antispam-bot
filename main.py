import datetime

import telebot

from secrets import BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)


TIMEOUT_MIN = 1

ADMINS_ID = set()

LOGIN = 'admin'
PASSWORD = 'admin'


@bot.message_handler(commands=['start'])
def start_message(message):
    data = message.text.split(' ')

    if message.from_user.id == message.chat.id:
        if len(data) == 3:
            login = data[1]
            password = data[2]

            if login == LOGIN and password == PASSWORD:
                ADMINS_ID.add(message.from_user.id)

                bot.send_message(message.chat.id, 'Привет, я тебя запомнил и не буду тебе мешать')
            else:
                bot.send_message(message.chat.id, 'Неверные логин и пароль')
        else:
            bot.send_message(message.chat.id, 'Для общения с этим ботом необходимо авторизоваться')


@bot.message_handler(content_types=['photo', 'text', "document"])
def check_message(message):
    print(message)
    if message.content_type == 'document':
        if 'image' in message.document.mime_type:
            print('Изображение: докумен!')

            try:
                if message.from_user.id not in ADMINS_ID:
                    new_datetime = datetime.datetime.fromtimestamp(message.date) + datetime.timedelta(minutes=TIMEOUT_MIN)
                    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
                    bot.restrict_chat_member(chat_id=message.chat.id,
                                             user_id=message.from_user.id,
                                             until_date=new_datetime,
                                             can_send_media_messages=False)
            except Exception as ex:
                print(ex)

    if message.content_type == 'photo':
        print('Изображение: фото!')

        try:
            if message.from_user.id not in ADMINS_ID:
                new_datetime = datetime.datetime.fromtimestamp(message.date) + datetime.timedelta(minutes=TIMEOUT_MIN)
                bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
                bot.restrict_chat_member(chat_id=message.chat.id,
                                         user_id=message.from_user.id,
                                         until_date=new_datetime,
                                         can_send_media_messages=False)
        except Exception as ex:
            print(ex)

    if message.content_type == 'text':
        print('Текст')

        try:
            if hasattr(message, 'entities'):
                if message.entities:
                    for entity in message.entities:
                        if entity.type == 'url':
                            if message.from_user.id not in ADMINS_ID:
                                new_datetime = datetime.datetime.fromtimestamp(message.date) + datetime.timedelta(minutes=TIMEOUT_MIN)
                                bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
                                bot.restrict_chat_member(chat_id=message.chat.id,
                                                         user_id=message.from_user.id,
                                                         until_date=new_datetime,
                                                         can_send_messages=False)
        except Exception as ex:
            print(ex)


def main() -> None:
    bot.infinity_polling()


if __name__ == '__main__':
    main()
