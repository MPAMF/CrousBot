from typing import Optional, List

import discord


class Command:
    name: str
    author: Optional[str]
    description: Optional[str]
    help_msg: Optional[str]

    def __init__(self, name: str,
                 author: Optional[str] = None,
                 description: Optional[str] = None,
                 help_msg: Optional[str] = None):
        self.name = name
        self.author = author
        self.description = description
        self.help_msg = help_msg

    async def execute(self, message: discord.Message, client: discord.Client, **kwargs):
        pass

    def __str__(self):
        result = "• %s:" % self.name
        if self.author is not None:
            result += "\nAuthor: %s" % self.author
        if self.description is not None:
            result += "\nDescription: %s" % self.description
        if self.help_msg is not None:
            result += "\nHelp: %s" % self.help_msg
        return result
