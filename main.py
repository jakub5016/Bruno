import discord
import openai

TOKEN = None
OPENAI_API_KEY = None

# Get the token
with open('TOKEN.txt', 'r') as file:
    data = file.readline().replace('\n', '')
    TOKEN = data[6:]

# Get the api key
with open('OPENAI_API_KEY.txt', 'r') as file:
    data = file.readline().replace('\n', '')
    OPENAI_API_KEY = data[4:]

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.content.startswith('!create_img'):
        openai.api_key = OPENAI_API_KEY
        print(message.content[12:])
        image = openai.Image.create(
        prompt=f"{message.content[12:]}",
        n=1,
        size="1024x1024"
        )

        await message.channel.send(image["data"][0]['url'])


client.run(TOKEN)
