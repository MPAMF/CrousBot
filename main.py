import datetime
import os

import discord
import requests
import random
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
        print("Logged on as", self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        content: str = message.content

        if content.startswith("merci mr crous bot"):
            msg = "ferme la {0.author.mention}".format(message)
            await message.channel.send(msg)
            return

        if content.startswith("Que penses-tu de"):
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
                if message.mentions[0].id == 198138552662360073: # little piece of code that we should not pay attention to..
                    msg = "{0.author.mention} est vraiment très très très cool, rien à redire, bon gars...".format(message)
                    await message.channel.send(msg)
                    return
                else:
                    r = random.random()
                    if r < 0.5:
                        msg = "{0.author.mention} est une énorme merde".format(message)
                    elif r < 0.75:
                        msg = "{0.author.mention} est vraiment pas ouf".format(message)
                    elif r < 0.95:
                        msg = "{0.author.mention} est pas trop trop mal".format(message)
                    else:
                        msg = "{0.author.mention} est bien!".format(message)
                    await message.channel.send(msg)
                    return


        if content.startswith("!menu"):
            args = content.split(" ")
            url = self.sites["illkirch"]

            if len(args) == 2:
                if args[1] in self.sites.keys():
                    url = self.sites[args[1]]
                else:
                    await message.channel.send(
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
                await message.channel.send(
                    "Tu mangeras pas à midi fdp (y'a "
                    "rien sur le menu)")
                return

            await message.channel.send("\n".join(msg))


intents = discord.Intents.default()
intents.message_content = True
client = CrousBotClient(intents=intents)
client.run(os.getenv("DISCORD_API_KEY"))
