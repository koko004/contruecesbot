import os
import telebot
import time
import requests

with open("config.txt", "r") as f:
    TOKEN = f.read().strip()

bot = telebot.TeleBot(TOKEN)

servers = {}  # Diccionario para almacenar los servidores y los puertos correspondientes

def check_server_status(server, port):
    url = f"http://{server}:{port}/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
    except:
        pass
    return False

def send_message(chat_id, text):
    bot.send_message(chat_id=chat_id, text=text)

def start_message():
    message = "¡Hola! Soy un bot de Telegram para verificar el estado de los servidores. Puedes utilizar los siguientes comandos:\n"
    message += "/add - Agregar un servidor\n"
    message += "/list - Listar todos los servidores agregados\n"
    message += "/delete - Eliminar un servidor\n"
    message += "/help - Mostrar esta ayuda\n"
    return message

def add_server(chat_id, server, port):
    if server in servers:
        message = "¡El servidor ya ha sido agregado anteriormente!"
    else:
        servers[server] = port
        message = "¡El servidor ha sido agregado correctamente!"
    return message

def list_servers(chat_id):
    if not servers:
        message = "¡No se han agregado servidores todavía!"
    else:
        message = "Los siguientes servidores han sido agregados:\n"
        for server, port in servers.items():
            message += f"{server}:{port}\n"
    return message

def delete_server(chat_id, server):
    if server in servers:
        del servers[server]
        message = "¡El servidor ha sido eliminado correctamente!"
    else:
        message = "¡El servidor no existe en la lista!"
    return message

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    message_text = start_message()
    bot.reply_to(message, message_text)

@bot.message_handler(commands=['add'])
def handle_add(message):
    chat_id = message.chat.id
    message_text = "Por favor, introduce el nombre del servidor que deseas agregar:"
    bot.send_message(chat_id, message_text)
    bot.register_next_step_handler(message, add_server_step1)

def add_server_step1(message):
    chat_id = message.chat.id
    server = message.text
    message_text = "Por favor, introduce el número de puerto del servidor:"
    bot.send_message(chat_id, message_text)
    bot.register_next_step_handler(message, add_server_step2, server)

def add_server_step2(message, server):
    chat_id = message.chat.id
    port = message.text
    message_text = add_server(chat_id, server, port)
    bot.send_message(chat_id, message_text)

@bot.message_handler(commands=['list'])
def handle_list(message):
    chat_id = message.chat.id
    message_text = list_servers(chat_id)
    bot.send_message(chat_id, message_text)

@bot.message_handler(commands=['delete'])
def handle_delete(message):
    chat_id = message.chat.id
    message_text = "Por favor, introduce el nombre del servidor que deseas eliminar:"
    bot.send_message(chat_id, message_text)
    bot.register_next_step_handler(message, delete_server_step1)

def delete_server_step1(message):
    chat_id = message.chat.id
    server = message.text
    message_text = delete_server(chat_id, server)

bot.infinity_polling()
