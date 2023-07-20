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

    if message.content.startswith('!img_amount'):
        try:
            int(message.content[12:])

            if int(message.content[12:]) <= 0:
                raise TypeError

        except:
            await message.channel.send(f"Ammout of creating images has to be an integer bigger than 0, you entered: \"{message.content[12:]}\"")
        finally:
            IMG_AMMOUT = int(message.content[12:])
            await message.channel.send(f"Ammout of creating images has been succesfully saved \nCurrent number of images: {IMG_AMMOUT}")

    if message.content.startswith('!create_img'):
        await message.channel.send(f"Generating an image for you input: \"{message.content[12:]}\"")
        print(message.content[12:])
        image = openai.Image.create(
        prompt=f"{message.content[12:]}",
        n=IMG_AMMOUT,
        size="1024x1024"
        )
        for i in range(IMG_AMMOUT):
            await message.channel.send(f"Picture no.{i}")
            await message.channel.send(image["data"][i]['url'])

    if message.content.startswith('!answer'):
        await message.channel.send(f"Generating an answer for you question: \"{message.content[8:]}\"")
        print(message.content[8:])
        answer = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"{message.content[8:]}"}
        ]
        )

        await message.channel.send(answer.choices[0].message.content)


client.run(TOKEN)
