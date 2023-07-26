import discord
import responses
import datetime, asyncio

from assign import add_driver_going
from assign import add_driver_returning
from assign import add_early_driver
from assign import remove_driver_going
from assign import remove_driver_returning
from assign import remove_early_driver

GETH_LINK = "https://forms.gle/RUF7kQoBSGLRRrxW8"
ANNOUCEMENT_CHANNEL_ID = 1131018704033955940
DRIVER_CHANNEL_ID = 1131665880032493608

driver_message_id = None

async def geth_signup_reminder(channel):
    #thursday but after the reminder time
    now = datetime.datetime.now()
    if now.date.weekday()==3 and now.hour > 11:
        wait_time = datetime.timedelta(hours=24).total_seconds()
        await asyncio.sleep(wait_time)

    #wait in 8 hour intervals until it's thursday
    now = datetime.datetime.now()
    if now.date.weekday()!=3:
        while now.date.weekday()!=3:
            wait_time = datetime.timedelta(hours=8).total_seconds()
            await asyncio.sleep(wait_time)
            now = datetime.datetime.now()

    #wait until thursday 11am
    now = datetime.datetime.now()
    reminder_time = now.replace(hour=11, minute=0, second=0, microsecond=0)
    wait_time - (reminder_time-now).total_seconds()
    await asyncio.sleep(wait_time)

    #send reminder then wait a week
    while True:
        await channel.send("Sign up for Gethsemane by today 3PM!! If you have to make any changes, just fill out the google form again :smiley: ")
        await channel.send(f"{GETH_LINK}")

        wait_time = datetime.timedelta(days=7).total_seconds()
        await asyncio.sleep(wait_time)
        

async def driver_geth_reminder(channel):
    #wednesday but after the reminder time
    now = datetime.datetime.now()
    if now.date.weekday()==2 and now.hour > 17:
        wait_time = datetime.timedelta(hours=24).total_seconds()
        await asyncio.sleep(wait_time)

    #wait in 8 hour intervals until it's wednesday
    now = datetime.datetime.now()
    if now.date.weekday()!=2:
        while now.date.weekday()!=2:
            wait_time = datetime.timedelta(hours=8).total_seconds()
            await asyncio.sleep(wait_time)
            now = datetime.datetime.now()

    #wait until wednesday 5:00 pm
    now = datetime.datetime.now()
    reminder_time = now.replace(hour=17, minute=0, second=0, microsecond=0)
    wait_time - (reminder_time-now).total_seconds()
    await asyncio.sleep(wait_time)

    #send reminder then wait a week
    while True:
        await channel.send("Please react if you can drive going to/returning from Gethsemane tomorrow and also if you're willing to be early car!!")

        wait_time = datetime.timedelta(days=7).total_seconds()
        await asyncio.sleep(wait_time)


async def reminder_test(channel):
    while True:
        now = datetime.datetime.now()
        print(f"current time is {now.hour}:{now.minute}:{now.second} on {now.month}/{now.day}")

        wait_time = datetime.timedelta(minutes=1).total_seconds()
        await asyncio.sleep(wait_time)
        
        await channel.send("Sign up for Gethsemane :smiley: ")

        await asyncio.sleep(60)   #1 minute


async def send_message(message, user_message):
    try:
        response = responses.get_response(user_message)
        await message.channel.send(response)
    except Exception as e:
        print(e)


def run_discord_bot():
    TOKEN = 'MTEyMTIwNTk4NjA5MTM0MzkwNQ.GY-Jt-.fpmJYbPIj3Rk82lW96cVKp0Ig-AgfVvKg0nCHY'
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
        # await geth_signup_reminder(client.get_channel(ANNOUCEMENT_CHANNEL_ID))
        # await driver_geth_reminder(client.get_channel(DRIVER_CHANNEL_ID))
        await reminder_test(client.get_channel(DRIVER_CHANNEL_ID))

    @client.event
    async def on_raw_reaction_add(payload):
        if not driver_message_id:
            return
        if payload.user_id==client.user.id:      #reactions that aren't the bot's
            return
        if payload.message_id==driver_message_id:
            driver = client.get_user(payload.user_id).display_name
            if payload.emoji.name=='ucisoon':
                add_driver_going(driver)
            elif payload.emoji.name=='bfuel':
                add_driver_returning(driver)
            elif payload.emoji.name=='sussy':
                add_early_driver(driver)
            #for later
            # if payload.emoji.name=='ohmyohmygah':
            #     add_driver_going(driver)
            # elif payload.emoji.name=='CHIRAQ':
            #     add_driver_returning(driver)
            # elif payload.emoji.name=='yeehuh':
            #     add_early_driver(driver)
            else:
                print('some other emoji idk lol')

    @client.event
    async def on_raw_reaction_remove(payload):
        if not driver_message_id:
            return
        elif payload.user_id==client.user.id:      #reactions that aren't the bot's
            return
        if payload.message_id==driver_message_id:
            driver = client.get_user(payload.user_id).display_name
            if payload.emoji.name=='ucisoon':
                remove_driver_going(driver)
            elif payload.emoji.name=='bfuel':
                remove_driver_returning(driver)
            elif payload.emoji.name=='sussy':
                remove_early_driver(driver)
            # if payload.emoji.name=='ohmyohmygah':
            #     remove_driver_going(driver)
            # elif payload.emoji.name=='CHIRAQ':
            #     remove_driver_returning(driver)
            # elif payload.emoji.name=='yeehuh':
            #     remove_early_driver(driver)
            else:
                print('some other emoji idk lol')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            if message.channel.id==DRIVER_CHANNEL_ID:
                global driver_message_id
                driver_message_id = message.id
                await message.add_reaction(client.get_emoji(1133173727660617822))
                await message.add_reaction(client.get_emoji(1133173565815017503))
                await message.add_reaction(client.get_emoji(1133173630340177940))
                #for later
                # await message.add_reaction(client.get_emoji(1093664350960615495))       #ohmyohmygah
                # await message.add_reaction(client.get_emoji(1085361216211390535))       #CHIRAQ
                # await message.add_reaction(client.get_emoji(1093664232995815566))       #yeehuh
            return
        
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'{username} said: "{user_message}" ({channel})')
        await send_message(message, user_message)
    

    client.run(TOKEN)