import os
import discord

from commands.command import Command
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

from commands.db.register import Register
from commands.db.work import Work
from commands.db.profile import Profile

from models import db, User
from pony.orm import *

class CrousBotClient(discord.Client):
    prefix = "!"

    async def top(self, message: discord.Message, client: discord.Client):
        top = {}
        for cmd in self.cmds:
            if not isinstance(self.cmds[cmd], Command): continue
            author = self.cmds[cmd].author
            if author is None: continue
            if author in top: top[author] += 1
            else: top[author] = 1
        items = sorted(top.items(), key=lambda item: item[1], reverse=True)
        msg = "Meilleurs devs du monde:\n"
        for i in range(len(items)):
            key, val = items[i]
            msg += "%d. %s (%d)\n" % (i+1, key, val)
        await message.channel.send(msg)

    cmds = {
        "merci mr crous bot": Merci(),
        "que penses-tu de": Think(),
        "je t'aime crous bot": Love(),
        "ntm crous bot": Insult(),
        f"{prefix}menu": Menu(),
        f"{prefix}fish": Fish(),
        f"{prefix}ferie": Ferie(),
        f"{prefix}pendu": Pendu(),
        f"{prefix}cours": Cours(),
        f"{prefix}meme": Meme(),
        f"{prefix}top": top,
        
        f"{prefix}register": Register(),
        f"{prefix}work": Work(),
        f"{prefix}profile": Profile()
    }

    async def on_ready(self):
        print("Logged on as", self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        content: str = message.content.lower()

        xp = 5

        for key in self.cmds.keys():
            if content.startswith(key):
                cmd = self.cmds[key]

                if isinstance(cmd, Command):
                    await cmd.execute(client=self, message=message, options=content.split(" ")[1:])
                    xp = 10
                elif callable(cmd):
                    await cmd(self, client=self, message=message)
                    xp = 10
                break

        if len(message.attachments) > 0:
            xp += 5

        self.give_xp_to_user(message.author.id, xp)

    @db_session
    def give_xp_to_user(self, user_id, xp):
        user_query = select(u for u in User if u.id == user_id)

        if len(user_query) == 0: return

        user = list(user_query)[0]
        user.xp += xp


intents = discord.Intents.default()
intents.message_content = True
client = CrousBotClient(intents=intents)
client.run(os.getenv("DISCORD_API_KEY"))