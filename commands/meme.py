import discord
import requests
import random

# Finds the top 25 memes in reddit and randomly returns 1 to the group using !meme command
class Meme:

    def __init__(self, client, message):
        self.client = client
        self.message = message
        self.name = "Meme"
        self.description = "Trouver les memes de reddit"

    def get_meme(self):
        response = requests.get('https://www.reddit.com/r/memes/top.json', headers={'User-agent': 'Mozilla/5.0'})
        data = response.json()
        meme_index = random.randint(0, 24)  # top 25 memes
        meme_data = data['data']['children'][meme_index]['data']
        return meme_data['title'], meme_data['url']

    async def execute(self):
        title, url = self.get_meme()
        embed = discord.Embed(title=title, color=discord.Color.blue())
        embed.set_image(url=url)

        channel = self.message.channel
        await channel.send(embed=embed)
