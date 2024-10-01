# Library Importing
import discord
from discord.ext import commands
import modules.utils as utils
import re
import random

from colorama import init as coloramaINIT
from colorama import Fore
from colorama import Style
coloramaINIT()
#-----------------------------------------------------------

class RPG(commands.Cog):

	# Constructor
	def __init__(self, bot):
		self.bot = bot
	
	@commands.Cog.listener()
	async def on_ready(self):
		print(f"RPG cog listener is {Fore.GREEN}ready{Style.RESET_ALL}.")
		
	#-------------------------------------------------------

	# Dice roll command: rolls any number of any type of dice
	@commands.command(aliases = ['r'])
	async def roll(self, ctx, *, diceNotation: str):
		try:
			try:
				pattern = r'(\d+)d(\d+)([+-]?\d+)?([*]?\d+)?([/]?\d+)?'
				match = re.search(pattern, diceNotation)
				
				message = ""
				
				numDice = int(match.group(1))
				diceSize = int(match.group(2))
				rollMod = int(match.group(3) or 0)
				rollMultMatch = match.group(4)
				rollDivMatch = match.group(5)

				if rollMultMatch:
					rollMult = int(rollMultMatch[1:])
				else:
					rollMult = 1
				if rollDivMatch:
					rollDiv = int(rollDivMatch[1:])
				else:
					rollDiv = 1
			except:
				await ctx.reply("Notação inválida. Exemplo de uso correto: 3d10+2*2. Modificadores e multiplicadores são opcionais.")
				return

			# Error handling
			if numDice < 1:
				await ctx.reply("Por favor, role no mínimo um dado.")
				return
			if numDice > 1000000:
				await ctx.reply("O limite de dados em uma única rolagem é 1 milhão.")
				return
			if diceSize < 1:
				await ctx.reply("Por favor, role um dado com no mínimo um lado.")
				return
			if diceSize > 1000000:
				await ctx.reply("O limite do tamanho dos dados é 1 milhão de lados.")
				return
			
			# Dice rolling
			rolls = [random.randint(1, diceSize) for i in range(numDice)]
			rollSum = sum(rolls)

			message += f"{ctx.author.mention} rola {numDice}d{diceSize}, resultando em: "
			
			# Output message handling
			if 1 < len(rolls) <= 10:
				message += f"{' + '.join(map(str, rolls))} = **{rollSum}**"
			else:
				message += f"**{rollSum}**"

			if rollMod:
				message += f"\nAdicionando seu modificador de "
				if rollMod > 0:
					message += f"+{rollMod}"
				else:
					message += f"{rollMod}"
				message += f", o resultado é: **{rollSum + rollMod}**"

			if rollMult != 1:
				message += f"\nMultiplicando o resultado por {rollMult}, o resultado final é: **{(rollSum + rollMod) * rollMult}**"

			if rollDiv != 1:
				message += f"\nDividindo o resultado por {rollDiv}, o resultado final é: **{(rollSum + rollMod) * rollMult / rollDiv}**"

			await ctx.reply(message)
		except Exception as e:
			await ctx.reply(f"Um erro ocorreu: {e}")
	
async def setup(bot):
	await bot.add_cog(RPG(bot))
	print("RPG module has finished loading.\n")
