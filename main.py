from telethon import TelegramClient, events
from telethon.tl.functions.users import GetFullUserRequest
from telethon.client import bots
from utils.weather import wtr
from requests import get
import os
import requests
import random

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


@bot.on(events.NewMessage(pattern='/website'))
async def websiteLink(event):
    message = "Website: https://quantumbyteofficial.tech/"
    await event.reply(f"{message}")
    raise events.StopPropagation

Truth = [
"What’s the last lie you told?",
"What was the most embarrassing thing you’ve ever done on a date?",
"Have you ever accidentally hit something (or someone!) with your car?",
"Name someone you’ve pretended to like but actually couldn’t stand.",
"What’s your most bizarre nickname?",
"What’s been your most physically painful experience?",
"What bridges are you glad that you burned?",
"What’s the craziest thing you’ve done on public transportation?",
"If you met a genie, what would your three wishes be?",
"If you could write anyone on Earth in for President of the United States, who would it be and why?",
"What’s the meanest thing you’ve ever said to someone else?",
"Who was your worst kiss ever?",
"What’s one thing you’d do if you knew there no consequences?",
"What’s the craziest thing you’ve done in front of a mirror?",
"What’s the meanest thing you’ve ever said about someone else?",
"What’s something you love to do with your friends that you’d never do in front of your partner?",
"Who are you most jealous of?",
"What do your favorite pajamas look like?",
"Have you ever faked sick to get out of a party?",
"Who’s the oldest person you’ve dated?",
"How many selfies do you take a day?",
"Meatloaf says he’d do anything for love, but he won’t do “that.” What’s your “that?”",
"How many times a week do you wear the same pants?",
"Would you date your high school crush today?",
"Where are you ticklish?",
"Do you believe in any superstitions? If so, which ones?",
"What’s one movie you’re embarrassed to admit you enjoy?",
"What’s your most embarrassing grooming habit?",
"When’s the last time you apologized? What for?",
"How do you really feel about the Twilight saga?",
"Where do most of your embarrassing odors come from?",
"Have you ever considered cheating on a partner?",
"Have you ever cheated on a partner?",
"Boxers or briefs?",
"Have you ever peed in a pool?",
"What’s the weirdest place you’ve ever grown hair?",
"If you were guaranteed to never get caught, who on Earth would you murder?",
"What’s the cheapest gift you’ve ever gotten for someone else?",
"What app do you waste the most time on?",
"What’s the weirdest thing you’ve done on a plane?",
"Have you ever been nude in public?",
"How many gossip blogs do you read a day?",
"What is the youngest age partner you’d date?",
"Have you ever picked your nose in public?",
"Have you ever lied about your age?",
"If you had to delete one app from your phone, which one would it be?",
"What’s your most embarrassing late night purchase?",
"What’s the longest you’ve gone without showering?",
"Have you ever used a fake ID?", "Who’s your hall pass?",]

Dare =[
"Do freestyle rap for 1 minute about the other participants and send video.",
"Kiss the person to your left and send video.",
"Do an impression of another player until someone can figure out who it is and send video.",
"Call your crush.",
"Dance with no music for 1 minute and send video.",
"Do a cartwheel and send video.",
"Let the person on your right draw on your face.",
"Give your phone to another player who can send one text saying anything they want to one of your contacts.",
"Drink lemon juice.",
"Crack an egg on our head and send video.",
"Swap clothes with someone of the opposite gender for 2 rounds and send video.",
"Act like a chicken until your next turn.",
"Burp the alphabet.",
"Talk in a Jamaican accent until your next turn.",
"Call a friend, pretend it’s their birthday, and sing “Happy Birthday” to them.",
"Perform ballet for 1 minute.",
"Shower with your clothes on.",
"Take a selfie on the toilet and post it.",
"End each sentence with the word “not” until your next turn.",
"Name a famous person that looks like each player.",
"Dance like your life depends on it.",
"Eat a packet of hot sauce or ketchup straight.",
"Pour ice down your pants and send video.",
"Spin around 12 times and try to walk straight.",
"Put on a blindfold and touch the other players’ faces until you can figure out who it is.",
"Let the other players redo your hairstyle.",
"Eat a raw egg and send video.",
"Let the player to your right redo your makeup.",
"Pretend to be a squirrel until your next turn.",
"Dump a bucket of cold water on your head and send video.",
"Lick a bar of soap and send video.",
"Eat a teaspoon of mustard.",
"Talk without closing your mouth and send video.",
"You have 5 minutes to write a country song and perform it.",
"Let someone paint your nails any way they want.",
"Do 5 minutes of stand-up comedy and send video.",
"Quack like a duck until your next turn.",
"Sing the national anthem in a British accent and send video."
]

@bot.on(events.NewMessage(pattern='/truth&dare'))
async def websiteLink(event):
    message = "Inorder to play Truth and Dare add this bot in your friends group, then type \"\\truth\" for a truth questinon and \"\\dare\" for a dare."
    await event.reply(f"{message}")
    raise events.StopPropagation


@bot.on(events.NewMessage(pattern='/truth'))
async def websiteLink(event):
    number = int(random.uniform(0, 100))
    sawal = Truth[number]
    await event.reply(f"{sawal}")
    raise events.StopPropagation

@bot.on(events.NewMessage(pattern='/dare'))
async def websiteLink(event):
    number = int(random.uniform(0, 40))
    sawal = Dare[number]
    await event.reply(f"{sawal}")
    raise events.StopPropagation

############################################################################################

os.system("clear")


def main():
    """Start the bot."""
    bot.run_until_disconnected()


if __name__ == '__main__':
    main()
