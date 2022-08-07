import telebot
from telebot import types
import os
from PIL import ImageGrab
from winsound import Beep
from datetime import datetime
import webbrowser


class data:
    starttime = datetime.now()
    shutdowncheck = 0
    restartcheck = 0


os.system("cls")
print("Bot is ready!\n")

TOKEN = "5596137032:AAGvO8d1yViXiFsRTKSO1XvSMr7TYOgVRAI"
bot = telebot.TeleBot(TOKEN)


# *** 1. Files RW functions ;
def getfile(filename):
    with open(filename, "r+") as myfile:
        return myfile.read()


def putfile(filename, filedata):
    with open(filename, "w+") as myfile:
        return myfile.write(filedata)


# *** 2. Power Options ;
def poweroptions(user):
    userchatid = user.chat.id
    markups = types.ReplyKeyboardMarkup(row_width=2)
    markup1 = types.KeyboardButton("Shutdown 🖲")
    markup2 = types.KeyboardButton("Restart 🔄")
    markup3 = types.KeyboardButton("home 🏠")
    markups.add(markup1, markup2, markup3)
    bot.send_message(
        userchatid, "🔌 Choose a power option from the menu: ", reply_markup=markups)


def shutdownbtn(user):
    userchatid = user.chat.id
    bot.send_chat_action(userchatid, "typing")
    bot.send_message(
        userchatid, "Request to shut down your computer:\nSend /yes to conform, or send /no to cancel.")
    data.shutdowncheck = 1
    data.restartcheck = 0


def restartbtn(user):
    userchatid = user.chat.id
    bot.send_chat_action(userchatid, "typing")
    bot.send_message(
        userchatid, "Request to restart your computer:\nSend /yes to conform, or send /no to cancel.")
    data.shutdowncheck = 0
    data.restartcheck = 1


def shutdown_or_restart(user):
    userchatid = user.chat.id
    if data.shutdowncheck == 1 and data.restartcheck == 0:
        bot.send_chat_action(userchatid, "typing")
        bot.send_message(userchatid, "Your computer is shutting down.")
        os.system("shutdown /s /t 1")
    elif data.shutdowncheck == 0 and data.restartcheck == 1:
        bot.send_chat_action(userchatid, "typing")
        bot.send_message(userchatid, "Your computer is restarting.")
        os.system("shutdown /r /t 1")
    else:
        bot.send_chat_action(userchatid, "typing")
        bot.send_message(userchatid, "❌ An error accured!")
    data.shutdowncheck = 0
    data.restartcheck = 0
    startcmd(user, "home")


def cancelaction(user):
    userchatid = user.chat.id
    if data.shutdowncheck or data.restartcheck:
        bot.send_chat_action(userchatid, "typing")
        bot.send_message(userchatid, "Action canceled.")
    else:
        bot.send_chat_action(userchatid, "typing")
        bot.send_message(userchatid, "❌ An error accured!")
    data.shutdowncheck = 0
    data.restartcheck = 0
    startcmd(user, "home")


# *** 3. Screen Shot Option ;
def takescreenshot(user):
    userchatid = user.chat.id
    bot.send_chat_action(userchatid, "typing")
    bot.send_message(userchatid, "👀 Taking a screenshot...")
    screenshot = ImageGrab.grab()
    screenshot.save("screenshot.png")
    photo = open("screenshot.png", "rb")
    caption = datetime.now().strftime("%H:%M:%S\n%A, %B %d, %Y")
    bot.send_document(userchatid, photo, caption=caption)
    photo.close()
    os.remove("screenshot.png")
    startcmd(user, "home")


# *** 4. Play a Sound Option ;
def playasound(user):
    userchatid = user.chat.id
    bot.send_chat_action(userchatid, "typing")
    bot.send_message(userchatid, "▶️ Playing a sound...")
    for i in range(1, 10):
        Beep((i * 500), 700 - (i * 50))
    bot.send_message(userchatid, "⏹ A beep sound was successfully played.")
    startcmd(user, "home")


# *** 5. File Manager Options ;
def filemanager(user):
    userchatid = user.chat.id
    markups = types.ReplyKeyboardMarkup(row_width=2)
    markup1 = types.KeyboardButton("Download 📥")
    markup2 = types.KeyboardButton("Local Files 📂")
    markup3 = types.KeyboardButton("home 🏠")
    markups.add(markup1, markup2, markup3)
    bot.send_message(
        userchatid, "🗃 Choose an action from the menu:", reply_markup=markups)


def downloadbtn(user):
    userchatid = user.chat.id
    bot.send_chat_action(userchatid, "typing")
    bot.send_message(
        userchatid, "To download a file from your computer, send your file name in this format:\n\n```\n/download [filename or fileaddress]```", parse_mode='MarkdownV2')


def downloadfile(user):
    usertext = user.text
    userchatid = user.chat.id
    thefile = usertext.replace("/download ", "").strip()
    if os.path.isdir(thefile):
        bot.send_chat_action(userchatid, "typing")
        bot.send_message(userchatid, "❌ This is a directory.")
    elif os.path.isfile(thefile):
        bot.send_chat_action(userchatid, "typing")
        bot.send_message(userchatid, f"📲 Downloading {thefile} ❕")
        thefile = open(thefile, "rb")
        bot.send_document(userchatid, thefile)
    else:
        bot.send_chat_action(userchatid, "typing")
        bot.send_message(userchatid, "❌ File or path was not found.")
    startcmd(user, "home")


def filelistbtn(user):
    userchatid = user.chat.id
    bot.send_chat_action(userchatid, "typing")
    bot.send_message(
        userchatid, "To get a list of folders and files in a directory, send your directory in this format:\n\n```\n/filelist [dir]```", parse_mode='MarkdownV2')


def showfilelist(user):
    usertext = user.text
    userchatid = user.chat.id
    thefolder = usertext.replace("/filelist ", "").strip()
    if os.path.isdir(thefolder):
        bot.send_chat_action(userchatid, "typing")
        bot.send_message(userchatid, f"🔎 Scanning... ❕")
        folderlist = ""
        foldercount = 0
        filelist = ""
        filecount = 0
        for r, d, f in os.walk(thefolder):
            for folder in d:
                if foldercount < 30:
                    folderlist += f"\n📁 {r}\\{folder}"
                    foldercount += 1
                else:
                    break
            for file in f:
                if filecount < 30:
                    filelist += f"\n📄 {r}\\{file}"
                    filecount += 1
                else:
                    break
        bot.send_chat_action(userchatid, "typing")
        bot.send_message(
            userchatid, f"🗄 List of the first {foldercount} folders in {thefolder}:\n\n{folderlist}")
        bot.send_chat_action(userchatid, "typing")
        bot.send_message(
            userchatid, f"📇 List of the first {filecount} files in {thefolder}:\n\n{filelist}")
    elif os.path.isfile(thefolder):
        bot.send_chat_action(userchatid, "typing")
        bot.send_message(userchatid, "❌ This is a file.")
    else:
        bot.send_chat_action(userchatid, "typing")
        bot.send_message(userchatid, "❌ Directory was not found.")
    startcmd(user, "home")


# *** 6. Web Browsing Option ;
def webbrowserbtn(user):
    userchatid = user.chat.id
    bot.send_message(
        userchatid, "To open a web page in your computer's browser, send your link in this format:\n\n```\n/web [link]```", parse_mode="MarkdownV2")


def openwebpage(user):
    usertext = user.text
    userchatid = user.chat.id
    link = usertext.replace("/web ", "").strip()
    bot.send_chat_action(userchatid, "typing")
    bot.send_message(userchatid, f"💠 Openning {link} ❕")
    webbrowser.get(
        "C:/Program Files (x86)/Google/Chrome/Application/Chrome.exe %s").open(link, new=2)
    bot.send_message(userchatid, f"✅ {link} is now open in your computer.")
    startcmd(user, "home")


# *** 7. Oppening an App Option ;
def openappbtn(user):
    userchatid = user.chat.id
    bot.send_message(
        userchatid, "To open an app on your computer, send the program name in this format:\n\n```\n/openapp [appname]```", parse_mode="MarkdownV2")


def openapp(user):
    usertext = user.text
    userchatid = user.chat.id
    appname = usertext.replace("/openapp ", "").strip()
    bot.send_chat_action(userchatid, "typing")
    bot.send_message(userchatid, f"💠 Openning {appname} ❕")
    respond = os.system(f"start {appname}")
    bot.send_chat_action(userchatid, "typing")
    bot.send_message(userchatid, f"✅ {appname} is now open on your computer.") if respond == 0 else bot.send_message(
        userchatid, f"❌ Failed to open {appname}.")
    startcmd(user, "home")


# *** 8. Saving to DataBase Options ;
def savetodb(user):
    usertext = user.text
    userchatid = user.chat.id
    thetext = usertext.replace("/save ", "").strip()
    dataid = datetime.now().strftime("%m%d%H%M")
    putfile(f"database/data_{dataid}.txt", str(thetext))
    bot.send_chat_action(userchatid, "typing")
    bot.send_message(
        userchatid, f"✅ Your text is saved with ```{dataid}``` id\.", parse_mode='MarkdownV2')
    startcmd(user, "home")


def dbsavelist(user):
    userchatid = user.chat.id
    fileslist = ""
    for r, d, f in os.walk("database"):
        for file in f:
            fileslist += f"\n{file}"
    bot.send_chat_action(userchatid, "typing")
    bot.send_message(userchatid, f"Your saved files list:\n{fileslist}")
    startcmd(user, "home")


# *** 9. Start Bot Settings ;
def startcmd(user, state):
    userchatid = user.chat.id
    markups = types.ReplyKeyboardMarkup(row_width=2)
    markup1 = types.KeyboardButton("Take a Screenshot 🖥")
    markup2 = types.KeyboardButton("Power Options 🔋")
    markup3 = types.KeyboardButton("Play a Sound 🔊")
    markup4 = types.KeyboardButton("File Manager 🗂")
    markup5 = types.KeyboardButton("Web Browser 🌐")
    markup6 = types.KeyboardButton("Open an App 💾")
    markups.add(markup1, markup2, markup3, markup4, markup5, markup6)
    if state == "start":
        bot.send_message(
            userchatid, """Hello, welcome to my os remoter bot. 🤠

            
🧑🏻‍💻 Coded by: Roya Salehi

📬 Contact info:
📧 Roya.79.Salehi@gmail.com
🌐 www.github.com/Roya-Salehi""", reply_markup=markups)
        print(f"user {userchatid} started the bot.")
        pcuser = os.getlogin()
        cpuusage = os.popen("wmic cpu get loadpercentage").read()
        runtime = str(datetime.now() - data.starttime)
        bot.send_message(
            userchatid, f"⏱ Server Run time : {runtime.partition('.')[0]}\n🥸 User: {pcuser}\n📊 CPU: {cpuusage.splitlines()[2].strip()}%")
    elif state == "home":
        bot.send_chat_action(userchatid, "typing")
        bot.send_message(
            userchatid, "What would you like to do? 😀", reply_markup=markups)


# *** 10. Checking User's Input ;
@bot.message_handler(content_types=["text"])
def get_user_info(user):
    admins = "R0yA_Slh"
    usertext = user.text
    userchatid = user.chat.id
    userusername = user.chat.username
    userfirstname = user.chat.first_name
    userlastname = user.chat.last_name
    if userusername == admins:
        if usertext == "/start":
            startcmd(user, "start")
        elif usertext == "home 🏠":
            startcmd(user, "home")
        elif usertext == "/save":
            bot.send_chat_action(userchatid, "typing")
            bot.send_message(
                userchatid, "To save a message in your database, send your text in this format:\n\n```\n/save [message]```", parse_mode='MarkdownV2')
        elif usertext.startswith("/save "):
            savetodb(user)
        elif usertext == "/savelist":
            dbsavelist(user)
        elif usertext == "Power Options 🔋":
            poweroptions(user)
        elif usertext == "Shutdown 🖲":
            shutdownbtn(user)
        elif usertext == "Restart 🔄":
            restartbtn(user)
        elif usertext == "/yes":
            shutdown_or_restart(user)
        elif usertext == "/no":
            cancelaction(user)
        elif usertext == "Take a Screenshot 🖥":
            takescreenshot(user)
        elif usertext == "Play a Sound 🔊":
            playasound(user)
        elif usertext == "File Manager 🗂":
            filemanager(user)
        elif usertext == "Download 📥" or usertext == "/download":
            downloadbtn(user)
        elif usertext.startswith("/download "):
            downloadfile(user)
        elif usertext == "Local Files 📂" or usertext == "/filelist":
            filelistbtn(user)
        elif usertext.startswith("/filelist "):
            showfilelist(user)
        elif usertext == "Web Browser 🌐" or usertext == "/web":
            webbrowserbtn(user)
        elif usertext.startswith("/web "):
            openwebpage(user)
        elif usertext == "Open an App 💾" or usertext == "/openapp":
            openappbtn(user)
        elif usertext.startswith("/openapp "):
            openapp(user)
    else:
        bot.send_message(
            userchatid, "You are not authorized to access this bot.")


bot.polling(True)
