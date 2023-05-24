import discord
import requests
import random

from commands.command import Command


# Finds the top 25 memes in reddit and randomly returns 1 to the group using !meme command
class Meme(Command):

    def __init__(self):
        super().__init__(
            name="Meme",
            description="Trouver les memes de reddit",
            author="Iman"
        )

    def get_meme(self):
        response = requests.get('https://www.reddit.com/r/memes/top.json',
                                headers={'User-agent': 'Mozilla/5.0'})
        data = response.json()
        meme_index = random.randint(0, 24)  # top 25 memes
        meme_data = data['data']['children'][meme_index]['data']
        return meme_data['title'], meme_data['url']

    async def execute(self, message: discord.Message, client: discord.Client, **kwargs):
        title, url = self.get_meme()
        embed = discord.Embed(title=title, color=discord.Color.blue())
        embed.set_image(url=url)

        channel = message.channel
        await channel.send(embed=embed)
