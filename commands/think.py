import random

import discord

from commands.command import Command


class Think(Command):

    def __init__(self):
        super().__init__(
            name="Think",
            description="CrousBot donne son avis",
            author="Vincent W"
        )

    async def execute(self, message: discord.Message, client: discord.Client):
        if len(message.mentions) == 0:
            msg = "fdp, tu dois mentionner quelqu'un"
            await message.channel.send(msg)
            await message.author.send("Tu es un fils de pute")
            return
        elif len(message.mentions) > 1:
            msg = "fdp, tu dois mentionner qu'une seule personne"
            await message.channel.send(msg)
            await message.author.send("Tu es un fils de pute")
            return
        else:
            mention = message.mentions[0]
            if mention.id == 198138552662360073: # little piece of code that we should not be pay attention to..
                msg = "{0.mention} est vraiment très très très cool, rien à redire, bon gars...".format(mention)
                await message.channel.send(msg)
                return
            else:
                r = random.random()
                if r < 0.5:
                    msg = "{0.mention} est une énorme merde".format(mention)
                elif r < 0.75:
                    msg = "{0.mention} est vraiment pas ouf".format(mention)
                elif r < 0.95:
                    msg = "{0.mention} est pas trop trop mal".format(mention)
                else:
                    msg = "{0.mention} est bien!".format(mention)
                await message.channel.send(msg)
                return