import discord
import requests
from pony.orm import *

from commands.command import Command

from models import User

class Profile(Command):

    def __init__(self):
        super().__init__(
            name="Profile",
            description="Affiche le profile du user",
            author="Vincent W"
        )

    @db_session
    async def execute(self, message: discord.Message, client: discord.Client, **kwargs):
        user_id = str(message.author.id)
        name    = message.author.name 
        mention = message.author.mention

        existing_user = select(u for u in User if u.id == user_id)
        
        if len(existing_user) == 0:
            await message.channel.send(f"{message.author.mention} fdp tu dois d'abord t'inscrire (`!register`)")
            return

        user = list(existing_user)[0]

        embed = discord.Embed(
            title=user.name, 
            description=f"Profile de {user.name}", 
            color=discord.Color.red() if user.is_admin else discord.Color.green()
        )
        embed.set_thumbnail(url=user.display_avatar_url)
        embed.add_field(name="Argent 💸", value=user.money, inline=False)
        embed.add_field(name="Victoires Pendu", value=user.pendu_completed, inline=False)
        embed.add_field(name="Victoires Puissance4", value=user.puissance4_won, inline=False)

        channel = message.channel
        await channel.send(embed=embed)