from telethon import TelegramClient, events
from telethon.tl.functions.users import GetFullUserRequest
from telethon.client import bots
from utils.weather import wtr
from requests import get
import os
import requests

os.system("clear")

token = os.environ.get("BOT_TOKEN")
bot = TelegramClient('bot', 8009880, '86d78606689d61db9a904e167a4bbd50').start(
    bot_token=token)


@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    """Send a message when the command /start is issued."""
    await event.respond('Hello :)')
    if event.is_channel:
        await event.respond('Activated Bot For Channel')
    if event.is_group:
        await event.respond('Activated Bot For Group Chat : )')
    if event.is_private:
        await event.respond('Activated Bot For Private Chat : )')
    user = event.chat_id
    full = await bot(GetFullUserRequest(user))
    userDetails = f'''New User ID = {user}\nOther Details:\n{full}'''
    print(userDetails)
    f = open("userData.txt", "a")
    f.write(userDetails)
    f.close()

    raise events.StopPropagation


@bot.on(events.NewMessage(pattern='/whoami'))
async def whoami(event):
    chatid = event.chat_id
    await event.reply(f"Your chat id is: `{chatid}`")


@bot.on(events.NewMessage(pattern='/help'))
async def help(event):
    helpText = '''
List Of all Commands

/start - To Start The Bot
/help - Display List of all Commands
/wassup - EasterEgg
/whoami - Displays You User Id of Telegram
/joke - Displays a Random Joke
/news - Displays a Top 20 Headlines

Some Other USeful Links:

GitHub: https://github.com/QuantumByteStudios
QuantumByteChat: https://t.me/quantumbytechat
Website: https://github.com/QuantumByteStudios

Share this bot with your friends: http://t.me/QuantumByteStudios_bot

You Can Add This Group To Your Telegram Gorups and Channels :) 
    '''
    await event.respond(f"{helpText}")


@bot.on(events.NewMessage(pattern='/wassup'))
async def wassup(event):
    message = "I am Fine Thanks for Asking :)"
    await event.reply(f"{message}")
    raise events.StopPropagation


@bot.on(events.NewMessage(pattern='/joke'))
async def joke(event):
    joke = get("https://v2.jokeapi.dev/joke/Programming,Miscellaneous,Pun?blacklistFlags=nsfw,religious,political&type=twopart").json()
    setup = joke["setup"]
    delivery = joke["delivery"]
    await event.reply(f"{setup}\n\n{delivery}")
    raise events.StopPropagation


@bot.on(events.NewMessage(pattern='/news'))
async def news(event):
    newsapi = os.environ.get("NEWS_API")
    query_params = {
        "source": "news-api",
        "sortBy": "top",
        "apiKey": newsapi
    }
    main_url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=5f1413a68acb460bacbbc67e5d100386"

    # fetching data in json format
    res = requests.get(main_url, params=query_params)
    open_api_page = res.json()
    article = open_api_page["articles"]
    results = []

    for ar in article:
        results.append(ar["title"])

    for i in range(len(results)):
        # News = print()
        await event.respond(f"{i + 1, results[i]}")

    raise events.StopPropagation


# Event == Editing a Message


@bot.on(events.MessageEdited)
async def handler(event):
    # Log the date of new edits
    print('Message', event.id, 'changed at', event.date)
    await event.reply(f"You edited a message :)")
    raise events.StopPropagation

# @bot.on(events.NewMessage(pattern="/weather"))
# async def weather(event):
#     city = event.text
#     temp = wtr(city)
#     print(temp)
#     await event.reply(f"{temp}°C")
#     raise events.StopPropagation
# @bot.on(events.MessageRead)
# async def handler(event):
#     # Log when someone reads your messages
#     print('Someone has read all your messages until', event.max_id)

# CHAT ACTIONS


@bot.on(events.ChatAction)
async def handler(event):
    # Welcome every new user
    if event.user_joined:
        await event.reply('Welcome, to the Group!!')


@bot.on(events.ChatAction)
async def handler(event):
    # Welcome every new user
    if event.user_added:
        await event.reply('New Member added in the Group!!')


@bot.on(events.ChatAction)
async def handler(event):
    # Welcome every new user
    if event.user_kicked:
        await event.reply('User Kicked from the Group!!')


@bot.on(events.ChatAction)
async def handler(event):
    # Welcome every new user
    if event.created:
        await event.reply('Thanks For Inviting me to this Group :)')
        groupID = event.user_ids
        print(groupID)
        groupUserData = f'''Bot was added in a Group. Group IDs = {groupID}\n'''
        f = open("groupUserData.txt", "a")
        f.write(groupUserData)
        f.close()


@bot.on(events.ChatAction)
async def handler(event):
    # Welcome every new user
    if event.new_title:
        await event.reply('Group Title Was Changed :)')


@bot.on(events.UserUpdate)
async def handler(event):
    # If someone is uploading, say something
    if event.uploading:
        await bot.send_message(event.user_id, 'What are you sending?')


@bot.on(events.ChatAction)
async def handler(event):
    if event.user_left:
        await event.reply('Bye Bye!!')


@bot.on(events.NewMessage(pattern='/userid'))
async def useridgetter(target):
    """ For .userid command, returns the ID of the target user. """
    message = await target.get_reply_message()
    if message:
        if not message.forward:
            user_id = message.sender.id
            if message.sender.username:
                name = "@" + message.sender.username
            else:
                name = "**" + message.sender.first_name + "**"
        else:
            user_id = message.forward.sender.id
            if message.forward.sender.username:
                name = "@" + message.forward.sender.username
            else:
                name = "*" + message.forward.sender.first_name + "*"
        await target.edit("**Name:** {} \n**User ID:** `{}`".format(name, user_id))

############################################################################################

os.system("clear")


def main():
    """Start the bot."""
    bot.run_until_disconnected()


if __name__ == '__main__':
    main()
