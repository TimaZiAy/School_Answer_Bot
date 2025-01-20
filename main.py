from tg import *
import smtplib  # Импортируем библиотеку по работе с SMTP



# Добавляем необходимые подклассы - MIME-типы
from email.mime.multipart import MIMEMultipart  # Многокомпонентный объект
from email.mime.text import MIMEText  # Текст/HTML


def send(email, name, text):
    addr_from = "ziyatdinov.timur@gmail.com"
    password = "dpwt zaxy iydx zmek"
    SERVER = "smtp.gmail.com"
    addr_to = email

    msg = MIMEMultipart()  # Создаем сообщение
    msg['From'] = addr_from  # Адресат
    msg['To'] = addr_to  # Получатель
    msg['Subject'] = 'School Answer. Новое сообщение.'  # Тема сообщения

    body = f"Здравствуйте, {name}. Вам доступно новое сообщение (вопрос/предложение): {text}"
    msg.attach(MIMEText(body, 'plain'))  # Добавляем в сообщение текст

    server = smtplib.SMTP_SSL(SERVER, 465)  # Создаем объект SMTP
    # server.starttls()             # Начинаем шифрованный обмен по TLS
    server.login(addr_from, password)  # Получаем доступ
    server.send_message(msg)  # Отправляем сообщение
    server.quit()  # Выходим
