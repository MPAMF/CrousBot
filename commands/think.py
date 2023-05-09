import random
class Think:

    def __init__(self, client, message):
        self.client = client
        self.message = message
        self.name = "Think"
        self.description = "CrousBot donne son avis"

    async def execute(self):
        if len(self.message.mentions) == 0:
            msg = "fdp, tu dois mentionner quelqu'un"
            await self.message.channel.send(msg)
            await self.message.author.send("Tu es un fils de pute")
            return
        elif len(self.message.mentions) > 1:
            msg = "fdp, tu dois mentionner qu'une seule personne"
            await self.message.channel.send(msg)
            await self.message.author.send("Tu es un fils de pute")
            return
        else:
            mention = self.message.mentions[0]
            if mention.id == 198138552662360073: # little piece of code that we should not be pay attention to..
                msg = "{0.mention} est vraiment très très très cool, rien à redire, bon gars...".format(mention)
                await self.message.channel.send(msg)
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
                await self.message.channel.send(msg)
                return