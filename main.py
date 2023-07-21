import discord
import openai
from create_help_mess import HELP_MESSAGE

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

openai.api_key = OPENAI_API_KEY

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
IMG_AMMOUT = 1
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    global IMG_AMMOUT

    if message.content.startswith('!help'):
        await message.channel.send(HELP_MESSAGE)

    elif message.content.startswith('!img_amount'):
        try:
            int(message.content[12:])

            if (int(message.content[12:]) <= 0) or (int(message.content[12:]) > 5):
                raise TypeError

            IMG_AMMOUT = int(message.content[12:])
            await message.channel.send(f"```Ammout of creating images has been succesfully saved \nCurrent number of images: {IMG_AMMOUT}```")

        except:
            await message.channel.send(f"```Ammout of creating images has to be an integer bigger than 0 and less than 5, you entered: \"{message.content[12:]}\"```")

    elif message.content.startswith('!img_create'):
        await message.channel.send(f"```Generating an image for you input: \"{message.content[12:]}\"```")
        print(message.content[12:])
        try:
            image = openai.Image.create(
            prompt=f"{message.content[12:]}",
            n=IMG_AMMOUT,
            size="1024x1024"
            )
            for i in range(IMG_AMMOUT):
                await message.channel.send(f"Picture no.{i+1}")
                await message.channel.send(image["data"][i]['url'])
        except:
            await message.channel.send(f"```Slow down my circuts are burning! 🥵\nRate limit exceeded for images per minute. Limit: five pictures per one minute.```")

    elif message.content.startswith('!answer'):
        await message.channel.send(f"```Generating an answer for you question: \"{message.content[8:]}\"```")
        print(message.content[8:])
        answer = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"{message.content[8:]}"}
        ]
        )

        await message.channel.send(answer.choices[0].message.content)

    elif message.content.startswith('!'):
        await message.channel.send("```Sorry but this comand does not exist, try use !help comand.```")


client.run(TOKEN)
