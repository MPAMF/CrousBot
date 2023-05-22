import os
import discord

from commands.cours import Cours
from commands.merci import Merci
from commands.ferie import Ferie
from commands.fish import Fish
from commands.menu import Menu
from commands.pendu import Pendu
from commands.think import Think
from commands.love import Love
from commands.insult import Insult
from commands.meme import Meme

class CrousBotClient(discord.Client):
    prefix = "!"

    cmds = {
        "merci mr crous bot": Merci,
        "que penses-tu de": Think,
        "je t'aime crous bot": Love,
        "ntm crous bot": Insult,
        f"{prefix}menu": Menu,
        f"{prefix}fish": Fish,
        f"{prefix}ferie": Ferie,
        f"{prefix}pendu": Pendu,
        f"{prefix}cours": Cours,
        f"{prefix}meme": Meme,
    }

    async def on_ready(self):
        print("Logged on as", self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        content: str = message.content.lower()

        for key in self.cmds.keys():
            if content.startswith(key):
                cmd = self.cmds[key](self, message)
                await cmd.execute()
                break

intents = discord.Intents.default()
intents.message_content = True
client = CrousBotClient(intents=intents)
client.run(os.getenv("DISCORD_API_KEY"))