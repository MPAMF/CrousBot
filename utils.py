from typing import List

async def react_with_emojis(emojis: List[str], message):
    for emoji in emojis:
        await message.add_reaction(emoji)
    return