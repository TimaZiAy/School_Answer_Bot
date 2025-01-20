import telebot
import sqlite3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from text import *
from constants import *

bot = telebot.TeleBot(TOKEN)


class UserState:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.state = 'idle'
        self.selected_teacher = None
        self.message_text = ''


states = {}


def get_state(chat_id):
    if chat_id in states:
        return states[chat_id]
    else:
        new_state = UserState(chat_id)
        states[chat_id] = new_state
        return new_state


def update_state(state):
    states[state.chat_id] = state


def connect_db():
    conn = sqlite3.connect('data1.db')
    cursor = conn.cursor()
    return conn, cursor


def close_db(conn):
    conn.close()


def fetch_teacher_email(name):
    conn, cursor = connect_db()
    cursor.execute("SELECT email FROM teachers WHERE name LIKE ?", ('%' + name + '%',))
    result = cursor.fetchone()
    close_db(conn)
    return result[0] if result else None


def send_email(to_address, subject, message_body, mesg):
    from_address = "timaziay@gmail.com"
    password = "mbza xepi vhpm ypiz"

    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject
    body = (f"Здравствуйте, вам доступно новое сообщение: {message_body}. Это сообщение оставлено пользователем {mesg.from_user.first_name}"
            f"\n\n\n"
            f"Проект учеников ЛИТ 1533.")
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(from_address, password)
        server.send_message(msg)


@bot.message_handler(commands=['start'])
def handle_start_command(message):
    state = get_state(message.chat.id)
    state.state = 'idle'
    update_state(state)
    bot.reply_to(message, b1)
    bot.send_message(message.chat.id,
                     text="В настоящий момент доступна только бета-версия. Для дополнительной информации '/info'.\n"
                          "Чтобы начать консультацию, введите команду /create")


@bot.message_handler(commands=["info"])
def info_message(message):
    bot.send_message(message.chat.id, text=b1dop)


@bot.message_handler(commands=["create"])
def create_message(message):
    state = get_state(message.chat.id)
    state.state = 'select_teacher'
    update_state(state)

@bot.message_handler(func=lambda m: True)
def handle_all_messages(message):
    state = get_state(message.chat.id)
    if state.state == 'idle':
        bot.reply_to(message, "Пожалуйста, введите команду '/create' для создания консультации.")
    elif state.state == 'select_teacher':
        teacher_email = fetch_teacher_email(message.text)
        if teacher_email:
            state.selected_teacher = teacher_email
            state.state = 'enter_message'
            update_state(state)
            bot.reply_to(message, "Отлично! Теперь напишите текст сообщения.")
        else:
            bot.reply_to(message, "Не нашел учителя с таким именем. Попробуйте еще раз.")
    elif state.state == 'enter_message':
        state.message_text = message.text
        update_state(state)
        send_email(state.selected_teacher, 'School Answer. Новое сообщение.', state.message_text, message)
        bot.reply_to(message, "Сообщение успешно отправлено!")
        state.state = 'idle'
        update_state(state)


if __name__ == '__main__':
    bot.polling(none_stop=True)
