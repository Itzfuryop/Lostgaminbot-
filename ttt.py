import discord
from discord.ext import commands
import random

class TicTacToe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.player1 = ""
        self.player2 = ""
        self.turn = ""
        self.gameOver = True
        self.board = []
        self.winningConditions = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6]
        ]

    @commands.command()
    async def ttt(self, ctx, p1: discord.Member, p2: discord.Member):
        if self.gameOver:
            self.board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                          ":white_large_square:", ":white_large_square:", ":white_large_square:",
                          ":white_large_square:", ":white_large_square:", ":white_large_square:"]
            self.turn = ""
            self.gameOver = False

            self.player1 = p1
            self.player2 = p2

            num = random.randint(1, 2)
            if num == 1:
                self.turn = self.player1
                await ctx.send(f"It is {self.player1.mention}'s turn.")
            elif num == 2:
                self.turn = self.player2
                await ctx.send(f"It is {self.player2.mention}'s turn.")
        else:
            await ctx.send("A game is already in progress! Finish it before starting a new one.")

    @commands.command()
    async def place(self, ctx, pos: int):
        if not self.gameOver:
            mark = ""
            if self.turn == ctx.author:
                if self.turn == self.player1:
                    mark = ":regional_indicator_x:"
                elif self.turn == self.player2:
                    mark = ":o2:"
                if 0 < pos < 10 and self.board[pos - 1] == ":white_large_square:":
                    self.board[pos - 1] = mark

                    # print the board
                    line = ""
                    for x in range(len(self.board)):
                        if x == 2 or x == 5 or x == 8:
                            line += " " + self.board[x]
                            await ctx.send(line)
                            line = ""
                        else:
                            line += " " + self.board[x]

                    self.check_winner()
                    if self.gameOver:
                        await ctx.send(mark + " wins!")
                    elif len([cell for cell in self.board if cell == ":white_large_square:"]) == 0:
                        self.gameOver = True
                        await ctx.send("It's a tie!")

                    # switch turns
                    if self.turn == self.player1:
                        self.turn = self.player2
                    elif self.turn == self.player2:
                        self.turn = self.player1
                else:
                    await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
            else:
                await ctx.send("It is not your turn.")
        else:
            await ctx.send(f"Please start a new game using the {ctx.prefix}tictactoe command.")

    def check_winner(self):
        for condition in self.winningConditions:
            if self.board[condition[0]] == self.board[condition[1]] == self.board[condition[2]] != ":white_large_square:":
                self.gameOver = True
                break

    @ttt.error
    async def ttt_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention 2 players for this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")
        elif isinstance(error, commands.CommandError):
            await ctx.send("An error occurred while processing the command. Please try again.")

    @place.error
    async def place_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter a position you would like to mark.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please make sure to enter an integer.")
        elif isinstance(error, commands.CommandError):
            await ctx.send("An error occurred while processing the command. Please try again.")

async def setup(bot):
  await bot.add_cog(TicTacToe(bot))
