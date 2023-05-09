from babel.dates import format_date
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests
import datetime

load_dotenv()

class Menu:

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

    def __init__(self, client, message):
        self.client = client
        self.message = message
        self.name = "Menu"
        self.description = "Affiche le menu du Crous"

    async def execute(self):
        
        content: str = self.message.content.lower()
        
        args = content.split(" ")
        url = self.sites["illkirch"]

        if len(args) == 2:
            if args[1] in self.sites.keys():
                url = self.sites[args[1]]
            else:
                await self.message.channel.send(
                    "Arguments possibles: !menu illkirch/esplanade/paulappel")
                return

        r = requests.get(url, verify=False)
        soup = BeautifulSoup(r.text, features="html.parser")

        date = "Menu du %s" % format_date(datetime.date.today(),
                                              "EEEE d MMMM y",
                                              locale="fr_FR")

        name = self.names[args[1] if len(args) == 2 else "illkirch"]
        msg = ["%s à %s" % (date, name), ""]

        for h in soup.findAll("div", {"class": "menu"}):
            content = h.find("time", {"class", "menu_date_title"})

            if len(content) == 0:
                continue

            found_date = content.get_text()

            if found_date != date:
                continue

            content = h.find("ul", {"class": "meal_foodies"}).findAll("li")

            if content is None or len(content) == 0:
                continue

            for c in content:
                text = c.contents

                if len(text) < 2:
                    continue

                title = text[0].get_text()

                if "PERSONNELS" in title or "Origines" in title:
                    continue

                msg.append(title)

                for li in text[1].contents:
                    if li.text == "" or li.text == "-":
                        continue
                    msg.append("• %s" % li.text)

                msg.append("")

        if len(msg) == 1:
            await self.message.channel.send(
                "Tu mangeras pas à midi fdp (y'a "
                "rien sur le menu)")
            return

        await self.message.channel.send("\n".join(msg))