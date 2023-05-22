import discord

from commands.command import Command


class Fish(Command):

    def __init__(self):
        super().__init__(
            name="Fish",
            description="Fish react un mec",
            author="Vincent W"
        )

    async def execute(self, message: discord.Message, client: discord.Client):
        if message.reference is None:
            msg = "{0.author.mention} fdp, tu dois mentionner faire référence à un message".format(message)
            await message.channel.send(msg)
        else:
            referenced_message = message.reference.resolved
            if referenced_message is not None:
                await referenced_message.reply("https://tenor.com/view/fish-react-fish-react-him-thanos-gif-26859685")
                await referenced_message.add_reaction("🐟")
                await message.delete() # should we delete the message the author sent ??
        return