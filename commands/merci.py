import discord

from commands.command import Command


class Merci(Command):

    def __init__(self):
        super().__init__(
            name="Merci",
            description="Remercie CrousBot",
            author="Paul"
        )

    async def execute(self, message: discord.Message, client: discord.Client, **kwargs):
        msg = "ferme la {0.author.mention}".format(message)
        await message.channel.send(msg)
        return