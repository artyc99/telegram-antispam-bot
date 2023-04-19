import datetime

import telebot

from secrets import BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)


TIMEOUT_MIN = 1


@bot.message_handler(content_types=['photo', 'text', "document"])
def start_message(message):
    print(message)
    if message.content_type == 'document':
        if 'image' in message.document.mime_type:
            print('Изображение: докумен!')

            new_datetime = datetime.datetime.fromtimestamp(message.date) + datetime.timedelta(minutes=TIMEOUT_MIN)
            bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            bot.restrict_chat_member(chat_id=message.chat.id,
                                     user_id=message.from_user.id,
                                     until_date=new_datetime,
                                     can_send_media_messages=False)

    if message.content_type == 'photo':
        print('Изображение: фото!')

        try:
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
