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
DRIVER_ANNOUNCEMENT_MESSAGE_ID = None

#need to test these two functions
async def geth_signup_reminder(channel):
    while True:
        now = datetime.datetime.now()
        print(f"current time is {now.hour}:{now.minute}:{now.second} on {now.month}/{now.day}")

        while now.date.weekday()!=4:
            print('gonna sleep for 4 hours')
            await asyncio.sleep(14400)   #4 hours
            now = datetime.datetime.now()
            print(f"current time is {now.hour}:{now.minute}:{now.second} on {now.month}/{now.day}")

        if now.date.weekday()==4:
            print('entered the dream land')
            reminder_time = now.replace(hour = 11, minute=0, second = 0, microsecond=0)
            wait_time = (reminder_time-now).total_seconds()
            await asyncio.sleep(wait_time)
            
            await channel.send("Sign up for Gethsemane by today 3PM!! If you have to make any changes, just fill out the google form again :smiley: ")
            await channel.send(f"{GETH_LINK}")

            await asyncio.sleep(86400)   #24 hours
        

async def driver_geth_reminder(channel):
    while True:
        now = datetime.datetime.now()
        print(f"driver time is {now.hour}:{now.minute}:{now.second} on {now.month}/{now.day}")

        while now.date.weekday()!=3:
            print('driver gonna sleep for 4 hours')
            await asyncio.sleep(14400)   #4 hours
            now = datetime.datetime.now()
            print(f"driver time is {now.hour}:{now.minute}:{now.second} on {now.month}/{now.day}")

        if now.date.weekday()==3:
            print('entered the drivers land')
            reminder_time = now.replace(hour = 18, minute=0, second = 0, microsecond=0)
            wait_time = (reminder_time-now).total_seconds()
            await asyncio.sleep(wait_time)
            
            await channel.send("Please react if you can drive going to/returning from Gethsemane tomorrow and also if you're willing to be early car!!")

            await asyncio.sleep(86400)   #24 hours


async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(user_message)
        #await message.author.send(response) if is_private else await message.channel.send(response)
        await message.channel.send(response)
    except Exception as e:
        print(e)


def run_discord_bot():
    TOKEN = 'MTEyMTIwNTk4NjA5MTM0MzkwNQ.GY-Jt-.fpmJYbPIj3Rk82lW96cVKp0Ig-AgfVvKg0nCHY'
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
        await geth_signup_reminder(client.get_channel(ANNOUCEMENT_CHANNEL_ID))
        await driver_geth_reminder(client.get_channel(DRIVER_CHANNEL_ID))

    #need to test these two also
    @client.event
    async def on_raw_reaction_add(payload):
        if not DRIVER_ANNOUNCEMENT_MESSAGE_ID:
            return
        if payload.message_id==DRIVER_ANNOUNCEMENT_MESSAGE_ID:
            driver = client.get_user(payload.user_id).display_name
            if payload.emoji.name=='ohmyohmygah':
                add_driver_going(driver)
            elif payload.emoji.name=='CHIRAQ':
                add_driver_returning(driver)
            elif payload.emoji.name=='yeehuh':
                add_early_driver(driver)
            else:
                print('some other emoji idk lol')

    @client.event
    async def on_raw_reaction_remove(payload):
        if not DRIVER_ANNOUNCEMENT_MESSAGE_ID:
            return
        if payload.message_id==DRIVER_ANNOUNCEMENT_MESSAGE_ID:
            driver = client.get_user(payload.user_id).display_name
            if payload.emoji.name=='ohmyohmygah':
                remove_driver_going(driver)
            elif payload.emoji.name=='CHIRAQ':
                remove_driver_returning(driver)
            elif payload.emoji.name=='yeehuh':
                remove_early_driver(driver)
            else:
                print('some other emoji idk lol')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            if message.channel.id==DRIVER_CHANNEL_ID:
                DRIVER_ANNOUNCEMENT_MESSAGE_ID = message.id
                await message.add_reaction(client.get_emoji(1093664350960615495))
                await message.add_reaction(client.get_emoji(1085361216211390535))
                await message.add_reaction(client.get_emoji(1093664232995815566))
            return
        
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'{username} said: "{user_message}" ({channel})')

        # if user_message[0] == '?':
        #     user_message = user_message[1:]
        #     await send_message(message, user_message, is_private=True)
        # else:
        #     await send_message(message, user_message, is_private=False)

        await send_message(message, user_message)
    

    client.run(TOKEN)