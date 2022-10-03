import datetime
import os

import discord
import requests
from babel.dates import format_date
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()


class CrousBotClient(discord.Client):
    sites = {
        "illkirch": "https://www.crous-strasbourg.fr/restaurant/resto-u-illkirch/",
        "esplanade": "https://www.crous-strasbourg.fr/restaurant/resto-u-esplanade/",
        "paulappel": "https://www.crous-strasbourg.fr/restaurant/resto-u-paul-appell/"
    }

    names = {
        "illkirch": "Illkirch",
        "esplanade": "Esplanade",
        "paulappel": "Paul Appel"
    }

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        content: str = message.content

        if content.startswith('!menu'):
            args = content.split(" ")
            url = self.sites["illkirch"]

            if len(args) == 2:
                if args[1] in self.sites.keys():
                    url = self.sites[args[1]]
                else:
                    await message.channel.send(
                        'Arguments possibles: !menu illkirch/esplanade/paulappel')
                    return

            r = requests.get(url, verify=False)
            soup = BeautifulSoup(r.text, features="html.parser")

            date = "Menu du %s" % format_date(datetime.date.today(),
                                              'EEEE d MMMM y',
                                              locale='fr_FR')

            parent = None
            name = self.names[args[1] if len(args) == 2 else 'illkirch']

            for h in soup.findAll('h3'):
                if h.text.lower() == date.lower():
                    parent = h.parent

            if parent is None:
                await message.channel.send("Ce menu n'a pas été trouvé")
                return

            for h in parent.findAll("h4"):
                if h.text == 'Déjeuner':
                    parent = h.parent

            content = parent.find('div', {"class": "content-repas"}).find(
                'div').contents

            msg = ["%s à %s" % (date, name), ""]

            if len(content) == 0 or 'Menu non communiqué' in content[0].get_text():
                await message.channel.send("Tu mangeras pas à midi fdp (y'a "
                                           "rien sur le menu)")
                return

            for i in range(0, len(content), 2):
                text = content[i].get_text()
                if 'PERSONNELS' in text or 'Origines' in text:
                    continue
                msg.append(text)

                plats = content[i + 1].findAll('li')

                for p in plats:
                    if p.text == '' or p.text == '-':
                        continue
                    msg.append("• %s" % p.get_text())

                msg.append("")

            await message.channel.send("\n".join(msg))


intents = discord.Intents.default()
intents.message_content = True
client = CrousBotClient(intents=intents)
client.run(os.getenv('DISCORD_API_KEY'))
