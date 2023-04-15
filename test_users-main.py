# connect library
import json
from secrets import token_urlsafe

from faker import Faker
from telebot import TeleBot, types

# TODO: put token
TOKEN = 'token'
bot = TeleBot(TOKEN, parse_mode='html')
# choose language
faker = Faker('ru_RU') 

# keyboard object
main_menu_reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
# buttons - first row
main_menu_reply_markup.row(
    types.KeyboardButton(text="1️⃣"), types.KeyboardButton(text="2️⃣")
)
# buttons - second row
main_menu_reply_markup.row(
    types.KeyboardButton(text="5️⃣"), types.KeyboardButton(text="🔟")
)

# '/start'
@bot.message_handler(commands=['start'])
def start_message_handler(message: types.Message):
    # send respond to '/start'
    # IMPORTANT! keyboard object
    bot.send_message(
        chat_id=message.chat.id,
        text="Привет!\nЭто бот для генерации тестовых пользователей. "\
        "Выбери сколько пользователей тебе нужно 👇🏻",
        reply_markup=main_menu_reply_markup
    )


# other messages
@bot.message_handler()
def message_handler(message: types.Message):
    # define number of users
    # or send error
    payload_len = 0
    if message.text == "1️⃣":
        payload_len = 1
    elif message.text == "2️⃣":
        payload_len = 2
    elif message.text == "5️⃣":
        payload_len = 5
    elif message.text == "🔟":
        payload_len = 10
    else:
        bot.send_message(chat_id=message.chat.id, text="Не понимаю тебя :(")
        return

    # generate data of users
    # method - simple_profile
    total_payload = []
    for _ in range(payload_len):
        user_info = faker.simple_profile()
        user_info['phone'] = f'+7{faker.msisdn()[3:]}'
        # при помощи библиотеки secrets генерируем пароль
        user_info['password'] = token_urlsafe(10)
        total_payload.append(user_info)

    # make series of data
    payload_str = json.dumps(
        obj=total_payload,
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
        default=str
    )

    # send result
    bot.send_message(
        chat_id=message.chat.id,
        text=f"Данные {payload_len} тестовых пользователей:\n<code>"\
        f"{payload_str}</code>"
    )
    bot.send_message(
        chat_id=message.chat.id,
        text="Если нужны еще данные, можешь выбрать еще раз 👇🏻",
        reply_markup=main_menu_reply_markup
    )
    

# main function
def main():
    # bot start
    bot.infinity_polling()


if __name__ == '__main__':
    main()
