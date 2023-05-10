class Fish:

    def __init__(self, client, message):
        self.client = client
        self.message = message
        self.name = "Fish"
        self.description = "Fish react un mec"

    async def execute(self):
        if self.message.reference == None:
            msg = "{0.author.mention} fdp, tu dois mentionner faire référence à un message".format(self.message)
            await self.message.channel.send(msg)
        else:
            referenced_message = self.message.reference.resolved 
            if referenced_message != None:
                await referenced_message.reply("https://tenor.com/view/fish-react-fish-react-him-thanos-gif-26859685")
                await referenced_message.add_reaction("🐟")
                await self.message.delete() # should we delete the message the author sent ?? 
        return