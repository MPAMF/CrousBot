import discord
import requests
from pony.orm import *

from commands.command import Command

from models import User, Level

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

        levels_query = select(l for l in Level)
        levels = list(levels_query)
        user_level = None
        next_threshold = 0

        for [i, level] in enumerate(levels):
            if i == len(levels) - 1:
                user_level = level
                break
            
            if user.xp < level.threshold:
                user_level = levels[i - 1]
                next_threshold = level.threshold
                next_level = level.name
                break

        embed = discord.Embed(
            title=user.name, 
            description=f"Profile de {user.name}", 
            color=discord.Color.red() if user.is_admin else discord.Color.green()
        )
        embed.set_thumbnail(url=user.display_avatar_url)
        embed.add_field(name=f"{user_level.name} (Suivant: **{'Aucun' if next_threshold == 0 else str(next_level)}**)", value=self.get_xp_visual(user.xp, levels))
        embed.add_field(name="XP", value=f"{user.xp} (Rang suivant: **{'Aucun' if next_threshold == 0 else str(next_threshold)}**)", inline=False)
        embed.add_field(name="Argent 💸", value=user.money, inline=False)
        embed.add_field(name="Victoires Pendu", value=user.pendu_completed, inline=False)
        embed.add_field(name="Victoires Puissance4", value=user.puissance4_won, inline=False)

        channel = message.channel
        await channel.send(embed=embed)

    def get_xp_visual(self, xp: int, levels):

        previous_threshold = levels[0].threshold
        next_threshold = levels[1].threshold

        for [i, level] in enumerate(levels):
            if i == len(levels) - 1:
                return '🟩'*10
            
            if xp < level.threshold:
                next_threshold = level.threshold
                previous_threshold = levels[i - 1].threshold 
                break
        
        steps = (next_threshold - previous_threshold) // 10
        current_progression = (xp - previous_threshold)
        green = (current_progression // steps) 

        return  green * '🟩' + (10 - green) * '⬛'
