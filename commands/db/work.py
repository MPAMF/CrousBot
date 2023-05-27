import discord
import requests
from datetime import datetime, timedelta
from typing import List
from pony.orm import *

from commands.command import Command

from models import TimeLimits, User

class Work(Command):

    def __init__(self):
        super().__init__(
            name="Travail",
            description="Au charbon",
            author="Vincent W"
        )

        self.work_types = ["freelance", "alternance"]

    @db_session
    async def execute(self, message: discord.Message, client: discord.Client, **kwargs):
        user_id = str(message.author.id)

        options = kwargs['options']

        if options == None or len(options) != 1:
            await message.channel.send(f"{message.author.mention} fdp la commande s'utilise comme ça: `!work <nom-du-travail>`")
            return
        
        work_type = options[0]

        if work_type not in self.work_types:
            await message.channel.send(f"{message.author.mention} fdp tu ne peux pas faire ce type travail.")
            await message.channel.send(f"Types de travail disponibles: **{'/'.join(self.work_types)}**")
            return 
        

        time_query = select(t for t in TimeLimits if t.user.id == user_id)
        user_query = select(u for u in User if u.id == user_id)
        time_limit = list(time_query)[0]
        user = list(user_query)[0]

        if work_type == "freelance":
            last_worked = time_limit.freelance
            diff = datetime.now() - last_worked

            work_delay = timedelta(hours=1)

            if (diff > work_delay): 
                await self.send_worked_message(message, work_type, 10)
                user.money += 10
                time_limit.freelance = datetime.now()
            else:
                await self.send_delay_message(message, work_type, timedelta(hours=1) - diff)
                return
            
        elif work_type == "alternance":
            
            last_worked = time_limit.alternance
            diff = datetime.now() - last_worked
            
            work_delay = timedelta(hours=6)

            if (diff > work_delay): 
                await self.send_worked_message(message, work_type, 100)
                user.money += 100
                time_limit.alternance = datetime.now()
            else:
                await self.send_delay_message(message, work_type, timedelta(hours=6) - diff)
                return
    

    async def send_delay_message(self, message, work_type, delay):
        
        hours, remainder = divmod(delay.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        await message.channel.send(f"{message.author.mention} fdp, tu ne pourras travailler en {work_type} que dans {hours}h{minutes}min{seconds}s")
        return
    
    async def send_worked_message(self, message, work_type, money):
        await message.channel.send(f"{message.author.mention} bravo fdp, tu viens de gagner {money}💸 en travaillant en {work_type}!")
        return