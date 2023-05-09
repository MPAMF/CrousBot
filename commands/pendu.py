class Pendu:

    def __init__(self, client, message):
        self.client = client
        self.message = message
        self.name = "Ferié"
        self.description = "Affiche les jours feriés"

    async def execute(self):
        word = "FILS DE PUTE"