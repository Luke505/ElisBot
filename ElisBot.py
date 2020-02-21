# -*- coding: utf-8 -*-
import telepot, time, requests, telepot.api, json, pymysql, tempfile
from telepot.namedtuple import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from config import Config, Messages
from db import Connection

#   Show keyboard options bar
def showOptions(options):
    buttons = []
    if type(options) != str:
        for option in options:
            buttons.append([KeyboardButton(text = option)])
    else:
        buttons.append([KeyboardButton(text = options)])
    return ReplyKeyboardMarkup(keyboard = buttons, resize_keyboard = True, one_time_keyboard = True, selective = True)

#   Check if the user is in the 'admins' list
def adminCheck(chat_id):
    return chat_id in Config.admins

#   
def handle(msg):
    global user_states
    chat_id = msg['chat']['id']

    if 'text' in msg:
        message = msg['text'].lower()
        file = None
    elif 'document' in msg:
        file = msg['document']['file_id']
        message = "- File (id: " + file + ") -"
        file = bot.getFile(file)
    else:
        bot.sendMessage(chat_id, Messages.unknowCMD, reply_markup = showOptions(Config.commands))
        return

    print(" Got message : " + message)
    if message == "/start":
        bot.sendMessage(chat_id, Config.welcome, reply_markup = showOptions(Config.commands))
        user_states[chat_id] = None
        # print(bot.getChat(chat_id))
    elif chat_id in user_states.keys():
        if message == "/id":
            user_states[chat_id] = "id"
            bot.sendMessage(chat_id, Messages.typeID, reply_markup = ReplyKeyboardRemove())
        elif message == "/name":
            user_states[chat_id] = "name"
            bot.sendMessage(chat_id, Messages.typeName, reply_markup = ReplyKeyboardRemove())
        elif message == "/room":
            user_states[chat_id] = "room"
            bot.sendMessage(chat_id, Messages.typeRoom, reply_markup = showOptions(Connection.getRooms()))
        elif message == "/job":
            user_states[chat_id] = "job"
            bot.sendMessage(chat_id, Messages.typeJob, reply_markup = showOptions(Connection.getJobs()))
        elif message == "/update" and adminCheck(chat_id):
            user_states[chat_id] = "update"
            bot.sendMessage(chat_id, Messages.typeUpdate, reply_markup = ReplyKeyboardRemove())
        elif user_states[chat_id] == "id":
            if message.isdigit():
                response = Connection.getResidentById(int(message))
                if response != None:
                    user = response
                    room = user['room']
                    face = Messages.face.get("default")

                    if user['roomHead']:
                        face = Messages.face.get("roomHead")
                        room += " - " + Messages.roomHead
                    elif user['areaHead']:
                        face = Messages.face.get("areaHead")
                        room += " - " + Messages.areaHead

                    data = (
                        face + " " + user['name'] + " " + user['surname'] + "\n" +
                        Messages.icons["mailbox"] + " " + user['email'] + "\n" +
                        Messages.icons["telephone"] + " " + user['cell'] + "\n" +
                        Messages.icons["books"] + " " + user['course'] + "\n" +
                        Messages.icons["hotel"] + " " + room + "\n\n"
                    )

                    bot.sendMessage(chat_id, data, reply_markup = showOptions(Config.commands))
                else:
                    bot.sendMessage(chat_id, Messages.noID, reply_markup = showOptions(Config.commands))
            else:
                bot.sendMessage(chat_id, Messages.noID, reply_markup = showOptions(Config.commands))
            user_states[chat_id] = None
        elif user_states[chat_id] == "name":
            response = Connection.getResidentByName(message)
            if response != None and len(response) > 0:
                data = ""

                for user in response:
                    room = user['room']
                    face = Messages.face.get("default")

                    if user['roomHead']:
                        face = Messages.face.get("roomHead")
                        room += " - " + Messages.roomHead
                    elif user['areaHead']:
                        face = Messages.face.get("areaHead")
                        room += " - " + Messages.areaHead

                    data += (
                        face + " " + user['name'] + " " + user['surname'] + "\n" +
                        Messages.icons["mailbox"] + " " + user['email'] + "\n" +
                        Messages.icons["telephone"] + " " + user['cell'] + "\n" +
                        Messages.icons["books"] + " " + user['course'] + "\n" +
                        Messages.icons["hotel"] + " " + room + "\n" +
                        Messages.icons["ticket"] + " " + str(user['id']) + "\n\n"
                    )

                bot.sendMessage(chat_id, data, reply_markup = showOptions(Config.commands))
            else:
                bot.sendMessage(chat_id, Messages.noName, reply_markup = showOptions(Config.commands))
            user_states[chat_id] = None
        elif user_states[chat_id] == "room":
            response = Connection.getRoomResidents(message)
            if response != None and len(response) > 0:
                data = ""

                for user in response:
                    extra = ""
                    face = Messages.face.get("default")

                    if user["roomHead"]:
                        face = Messages.face.get("roomHead") + "*"
                        extra = " - " + Messages.roomHead + "*"
                    elif user["areaHead"]:
                        face = Messages.face.get("areaHead") + "*"
                        extra = " - " + Messages.areaHead + "*"

                    data += (face + " " + user['name'] + " " + user['surname'] + extra + "\n")

                bot.sendMessage(chat_id, data, parse_mode = "Markdown", reply_markup = showOptions(Config.commands))
            else:
                bot.sendMessage(chat_id, Messages.noRoom, reply_markup = showOptions(Config.commands))
            user_states[chat_id] = None
        elif user_states[chat_id] == "job":
            response = Connection.getEmployees(message)
            if response != None and len(response) > 0:
                data = ""

                for user in response:
                    face = Messages.face.get("default")
                    extra = ""
                    if(user['manager']):
                        face = Messages.face.get("manager") + "*"
                        extra = " - " + Messages.jobManager + "*"
                    data += (face + " " + user['name'] + " " + user['surname'] + extra + "\n")

                bot.sendMessage(chat_id, data, parse_mode = "Markdown", reply_markup = showOptions(Config.commands))
            else:
                bot.sendMessage(chat_id, Messages.noJob, reply_markup = showOptions(Config.commands))
            user_states[chat_id] = None
        elif user_states[chat_id] == "update" and adminCheck(chat_id) and file != None:
            connection = Connection.connect()
            f = tempfile.TemporaryFile()
            try:
                bot.download_file(file['file_id'], f)
                f.flush()
                f.seek(0)
                sql = [x.strip() for x in f.readlines()]
                results = []
                with connection.cursor() as cursor:
                    print(sql)
                    for query in sql:
                        cursor.execute(query)
                        result = cursor.fetchall()
                        if(Config.debug):
                            print(result)
                        results.append(result)
                        bot.sendMessage(chat_id, results)
                    connection.commit()
                    bot.sendMessage(chat_id, Messages.updated, reply_markup = showOptions(Config.commands))
            except (RuntimeError, TypeError, NameError, pymysql.ProgrammingError, pymysql.Error) as err:
                bot.sendMessage(chat_id, "Error: {}".format(err), reply_markup = showOptions(Config.commands))
            finally:
                connection.close()
                f.close()
            user_states[chat_id] = None
        else:
            bot.sendMessage(chat_id, Messages.unknowCMD, reply_markup = showOptions(Config.commands))
            user_states[chat_id] = None
    else:
        bot.sendMessage(chat_id, Config.update, reply_markup = showOptions("/start"))

#****************************************** End methods ****************************************************************************

bot = telepot.Bot(Config.token_bot)
bot.message_loop(handle)
user_states = {}
print("BOT Started!")

while True:
    try:
        time.sleep(10)
    except requests.exceptions.ConnectionError as e:
        print(str(e))
