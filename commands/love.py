import discord

from commands.command import Command
from utils import react_with_emojis

class Love(Command):

    def __init__(self):
        super().__init__(
            name="Love",
            description="Donne de l'amour à CrousBot",
            author="Vincent W"
        )

    async def execute(self, message: discord.Message, client: discord.Client, **kwargs):
        await react_with_emojis(["🇹", "🇬", "🇧", "🇴", "🇿", "🅾️"], message)
        return