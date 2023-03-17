import os
import telebot
import time
import requests
import csv

TOKEN = "TOKEN"
bot = telebot.TeleBot(TOKEN)

HOSTS_FILE = "hosts.csv"

def read_hosts():
    try:
        with open(HOSTS_FILE, mode='r') as file:
            reader = csv.reader(file)
            return {rows[0]: rows[1] for rows in reader}
    except FileNotFoundError:
        return {}

def write_hosts(hosts):
    with open(HOSTS_FILE, mode='w') as file:
        writer = csv.writer(file)
        for server, port in hosts.items():
            writer.writerow([server, port])

servers = read_hosts()

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
        write_hosts(servers)
        message = "¡El servidor ha sido agregado correctamente!"
    return message

@bot.message_handler(commands=['list'])
def list_servers(message):
    chat_id = message.chat.id
    if not servers:
        message_text = "¡No se han agregado servidores todavía!"
    else:
        message_text = "Los siguientes servidores han sido agregados:\n"
        for server, port in servers.items():
            message_text += f"{server}:{port}\n"
    bot.send_message(chat_id, message_text)

@bot.message_handler(commands=['delete'])
def delete_server(message):
    chat_id = message.chat.id
    if not servers:
        message_text = "¡No se han agregado servidores todavía!"
        bot.send_message(chat_id, message_text)
        return

    message_text = "Por favor, selecciona el servidor que deseas eliminar:\n"
    for server, port in servers.items():
        message_text += f"{server}:{port}\n"
    bot.send_message(chat_id, message_text)

    bot.register_next_step_handler(message, delete_server_step)

def delete_server_step(message):
    chat_id = message.chat.id
    server_to_delete = message.text

    if server_to_delete in servers:
        del servers[server_to_delete]
        write_hosts(servers)
        message_text = "¡El servidor ha sido eliminado correctamente!"
    else:
        message_text = "¡El servidor no existe en la lista!"
    bot.send_message(chat_id, message_text)

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    message_text = start_message()
    bot.reply_to(message, message_text)

@bot.message_handler(commands=['add'])
def handle_add(message):
    chat_id = message.chat

bot.infinity_polling()
