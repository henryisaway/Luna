import discord
from discord.ext import commands
import modules.utils as utils
import random

from colorama import init as coloramaINIT
from colorama import Fore
from colorama import Style
coloramaINIT()
#-----------------------------------------------------------

class Misc(commands.Cog):

    # Constructor
    def __init__(self, bot):
        self.bot = bot
                
    @commands.Cog.listener()
    async def on_ready(self):

        print(f"Misc cog listener is {Fore.GREEN}ready{Style.RESET_ALL}.")
    
    #-------------------------------------------------------
    
    # Penis command: shows user's dick size
    @commands.command(aliases = ['tamanho'])
    async def penis(self, ctx):
        try:
            finalSize = ""
            finalBallsAmount = ""
            finalHeadsAmount = ""
            # Gerar tamanho do pinto
            sizeRNG = random.randint(1, 100)
            if sizeRNG <= 40:
                for _ in range(int(sizeRNG/5)):
                    finalSize += "="
            elif sizeRNG <= 70:
                for _ in range(int(sizeRNG/4)):
                    finalSize += "="
            elif sizeRNG <= 85:
                for _ in range(int(sizeRNG/3)):
                    finalSize += "="
            elif sizeRNG <= 93:
                for _ in range(int(sizeRNG/2)):
                    finalSize += "="
            elif sizeRNG > 93:
                for _ in range(int(sizeRNG)):
                    finalSize += "="

            # Gerar quantidade de bolas
            ballsRNG = random.randint(1, 100)
            if ballsRNG <= 90:
                finalBallsAmount = "8"
            elif ballsRNG <= 97:
                finalBallsAmount = "88"
            else:
                finalBallsAmount = "888"

            # Gerar quantidade de cabeças
            headsRNG = random.randint(1, 100)
            if headsRNG <= 90:
                finalHeadsAmount = "D"
            elif headsRNG <= 97:
                finalHeadsAmount = "DD"
            else:
                finalHeadsAmount = "DDD"

            message = finalBallsAmount + finalSize + finalHeadsAmount
            await ctx.reply(message)
        except Exception as e:
            await ctx.reply(f"Um erro ocorreu: {e}")
    
async def setup(bot):
    await bot.add_cog(Misc(bot))
    print("Miscellaneous module has finished loading.\n")
