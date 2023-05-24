import random

import discord

from commands.command import Command


class Insult(Command):

    def __init__(self):
        super().__init__(
            name="Insulte",
            description="CrousBot t'insulte",
            author="Vincent W"
        )

    async def execute(self, message: discord.Message, client: discord.Client, **kwargs):
        insults = open("assets/insultes.txt", "r")
        insult = random.choice(insults.readlines()).lower().strip()

        voyelles = ['a', 'e', 'i', 'o', 'u', 'y']

        d = 'd\'' if insult[0] in voyelles else 'de '

        await message.channel.send("{0}, va te faire foutre, espèce {1}{2}".format(message.author.mention, d, insult))
        return