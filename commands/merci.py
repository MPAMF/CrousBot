class Merci: 

    def __init__(self, client, message):
        self.client = client
        self.message = message
        self.name = "Merci"
        self.description = ""

    async def execute(self):
        msg = "ferme la {0.author.mention}".format(self.message)
        await self.message.channel.send(msg)
        return