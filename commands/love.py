from utils import react_with_emojis

class Love:

    def __init__(self, client, message):
        self.client = client
        self.message = message
        self.name = "Love"
        self.description = "Donne de l'amour à CrousBot"

    async def execute(self):
        await react_with_emojis(["🇹", "🇬", "🇧", "🇴", "🇿", "🅾️"], self.message)
        return