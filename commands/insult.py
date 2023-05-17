import random 
class Insult:

    def __init__(self, client, message):
        self.client = client
        self.message = message
        self.name = "Insulte"
        self.description = "CrousBot t'insulte"

    async def execute(self):
        insults = open("assets/insultes.txt", "r")
        insult = random.choice(insults.readlines()).lower().strip()

        voyelles = ['a', 'e', 'i', 'o', 'u', 'y']

        d = 'd\'' if insult[0] in voyelles else 'de '

        await self.message.channel.send("{0}, va te faire foutre, espèce {1}{2}".format(self.message.author.mention, d, insult))
        return