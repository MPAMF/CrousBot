import discord

from commands.command import Command

#TODO:
class Puissance4(Command):

    current_games: []
    def __init__(self):
        super().__init__(
            name="Puissance4",
            description="Joue un puissance 4 avec un ami",
            author="Paul"
        )
        self.board_width = 6
        self.board_height = 6
        self.start_line = False
        self.current_games = []

    async def execute(self, message: discord.Message, client: discord.Client, **kwargs):
        channel = self.message.channel

        arr = self.message.content.split(" ")

        mentioned_users = self.message.mentions

        if len(arr) < 2 or len(mentioned_users) == 0:
            await channel.send(
                "t con utilise ça comme ça: !puissance4 @joueur")
            return

        player1 = self.message.author
        player2 = mentioned_users[0]

        if player1 in self.current_games or player2 == self.client.user:
            await channel.send(
                "t con utilise ça comme ça: !puissance4 @joueur")
            return

        board = [[0 for _ in range(self.board_width)]
                 for _ in range(self.board_height)]

        self.current_games.append(player1)

        await channel.send(
            f"Bienvenue au puissance4!\n"
            f"{player1.mention} VS {player2.mention}"
            f"\nBonne chance!!")

        while self.check_win(board):
            pass

    def check_win(self, board) -> bool:
        return True

    def gen_line(self, width: int) -> str:
        return "+---" * width + "+"

    def gen_start_line(self, width: int) -> str:
        result = ""

        for i in range(0, width):
            result += "| %d " % i

        return result + "|"

    def gen_board(self, width: int, height: int, cases):
        result = [self.gen_line(width=width)]
        for x in range(width):
            line = ""
            for y in range(height):
                val = cases[x][y]

                if val == 1:
                    line += "| X "
                elif val == 2:
                    line += "| ○ "
                else:
                    line += "|   "

            result.append(line + "|")
            result.append(self.gen_line(width=width))

        if self.start_line:
            result.append(self.gen_start_line(width=width))

        return result
