import threading
import time
from datetime import datetime
import telebot
from telebot import types
bot_token = '7910066292:AAEuvtunpzB5AI9-d-cbirO9hoiwKgFirVM'
bot = telebot.TeleBot(bot_token)
recipient_id = 1149560913
user_state = {}
user_data = {}
user_birthdays = {}
# Обработчик команды start
@bot.message_handler(commands=['start'])
def start(message):
    # Создаем клавиатуру с кнопками
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Заказать поздравление')
    button2 = types.KeyboardButton('Отсчет до дня рождения')
    keyboard.add(button1, button2)
    # Отправляем сообщение с кнопками
    bot.send_message(message.chat.id, 'Тебя приветствует команда ПрофДР. Выберите действие: ', reply_markup=keyboard)

# Обработчик кнокпи 1
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    chat_id = message.chat.id

    if message.text == 'Заказать поздравление':
        # Устанавливаем состояние пользователя в 'waiting_for_name'
        user_state[chat_id] = 'waiting_for_name'
        user_data[chat_id] = {}  # Создаем пустой словарь для хранения данных пользователя
        bot.send_message(chat_id, 'Введите ваше ФИО (Фамилия Имя Отчество):')

    elif user_state.get(chat_id) == 'waiting_for_name':

        # Сохраняем введенные ФИО в словарь user_data
        user_data[chat_id]['ФИО'] = message.text
        # Переходим к следующему шагу
        user_state[chat_id] = 'waiting_for_tg'
        bot.send_message(chat_id, 'Теперь введите ваш ник в телеграмме:')

    elif user_state.get(chat_id) == 'waiting_for_tg':

        # Сохраняем введенный Telegram-ник
        user_data[chat_id]['НикТГ'] = message.text
        # Переходим к следующему шагу
        user_state[chat_id] = 'waiting_for_FIOimeninnika'
        bot.send_message(chat_id, 'Введите ФИО именинника:')

    elif user_state.get(chat_id) == 'waiting_for_FIOimeninnika':

        # Сохраняем ФИО именинника
        user_data[chat_id]['ФИО именинника'] = message.text
        # Переходим к следующему шагу
        user_state[chat_id] = 'waiting_for_vkImeninnika'
        bot.send_message(chat_id, 'Введите ВК именинника:')

    elif user_state.get(chat_id) == 'waiting_for_vkImeninnika':

        # Сохраняем ссылку на ВК именинника
        user_data[chat_id]['ВК именинника'] = message.text
        # Переходим к следующему шагу
        user_state[chat_id] = 'waiting_for_NumberGroupImeninnika'
        bot.send_message(chat_id, 'Введите номер группы именинника:')

    elif user_state.get(chat_id) == 'waiting_for_NumberGroupImeninnika':

        # Сохраняем номер группы именинника
        user_data[chat_id]['Номер группы именинника'] = message.text
        # Переходим к следующему шагу
        user_state[chat_id] = 'waiting_for_tgProforga'
        bot.send_message(chat_id, 'Введите ник в телеграмме профорга группы именинника:')

    elif user_state.get(chat_id) == 'waiting_for_tgProforga':

        # Сохраняем ник профорга
        user_data[chat_id]['ТГПрофорга'] = message.text
        # Переходим к следующему шагу
        user_state[chat_id] = 'waiting_for_date'
        bot.send_message(chat_id, 'Введите дату поздравления:')

    elif user_state.get(chat_id) == 'waiting_for_date':

        # Сохраняем дату поздравления
        user_data[chat_id]['Дата поздравления'] = message.text
        # Переходим к следующему шагу
        user_state[chat_id] = 'waiting_for_korpus'
        bot.send_message(chat_id, 'Введите корпус поздравления:')

    elif user_state.get(chat_id) == 'waiting_for_korpus':

        # Сохраняем корпус поздравления
        user_data[chat_id]['Корпус'] = message.text
        # Переходим к следующему шагу
        user_state[chat_id] = 'waiting_for_time'
        bot.send_message(chat_id, 'Укажите время поздравления')

    elif user_state.get(chat_id) == 'waiting_for_time':
        # Сохраняем время поздравления
        user_data[chat_id]['Время'] = message.text
        # Переходим к следующему шагу
        user_state[chat_id] = None
        # Подтверждаем сохранение данных
        bot.send_message(chat_id, 'Спасибо! Ваши данные успешно сохранены и отправлены на дальнейшее рассмотрение.')

        # Отправляем сообщение с данными для проверки
        message_to_send = "Новые данные от пользователя:\n"
        for key, value in user_data[chat_id].items():
            message_to_send += f"{key}: {value}\n"
        bot.send_message(recipient_id, message_to_send)



# Запускаем бота и отправку сообщений
if __name__ == '__main__':
    bot.polling(none_stop=True)