import discord
import responses



link = "https://discord.com/api/oauth2/authorize?client_id=1121205986091343905&permissions=534723950656&scope=bot"


async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


def run_discord_bot():
    TOKEN = 'MTEyMTIwNTk4NjA5MTM0MzkwNQ.GY-Jt-.fpmJYbPIj3Rk82lW96cVKp0Ig-AgfVvKg0nCHY'
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client_user} is now running!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        
        username = str(message.author)
        user_message = str(message_content)
        channel = str(message.channel)

        print(f'{username} said: "{user_message}" ({user_channel})')

        if user_message[0] == '?':
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)

        client.run(TOKEN)