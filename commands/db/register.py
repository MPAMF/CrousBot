import discord
import requests
from pony.orm import *

from commands.command import Command

from models import User, TimeLimits

class Register(Command):

    def __init__(self):
        super().__init__(
            name="Inscirption",
            description="S'incrit au système de sous et tout",
            author="Vincent W"
        )

        self.admin_user_ids = ['198138552662360073', '435872053929967636']

    @db_session
    async def execute(self, message: discord.Message, client: discord.Client, **kwargs):
        author = message.author
        user_id = str(author.id)
        name    = author.name 
        mention = author.mention
        display_avatar_url = author.display_avatar.url

        existing_user = select(u for u in User if u.id == user_id)

        if len(existing_user) != 0:
            await message.channel.send(f"{message.author.mention}, fdp de pute, tu t'es déjà register con de toi")
            return

        await message.channel.send(f"Bravo {author.mention}, tu viens de t'inscrire fdp")
        
        user = User(
            id=user_id, 
            display_avatar_url=display_avatar_url, 
            name=name, 
            mention=mention, 
            is_admin=user_id in self.admin_user_ids
        )
        time_limits = TimeLimits(user=user)