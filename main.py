import discord

TOKEN = None

# Get the roken
with open('TOKEN.txt', 'r') as file:
    data = file.readline().replace('\n', '')
    TOKEN = data[6:]

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(TOKEN)
