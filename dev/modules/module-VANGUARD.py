import discord
from discord.ext import commands

from . import vanguard_dataclasses
from . import utils

from colorama import init as coloramaINIT
from colorama import Fore
from colorama import Style
coloramaINIT()
#-----------------------------------------------------------

class Vanguard(commands.Cog):
	# Constructor
	def __init__(self, bot):
		self.bot = bot
		self.vanguards = {}
				
	@commands.Cog.listener()
	async def on_ready(self):

		print(f"Vanguard cog listener is {Fore.GREEN}ready{Style.RESET_ALL}.")

	#-------------------------------------------------------

	async def createVanguardThread(self, ctx: commands.Context) -> discord.Thread:
		try:
			thread = await ctx.channel.create_thread(
				name=f"Vanguard - {ctx.author.display_name}",
				type=discord.ChannelType.public_thread,
				auto_archive_duration=60,
				reason=f"Partida iniciada por {ctx.author.display_name}"
			)

			await thread.add_user(ctx.author)

			self.vanguards[ctx.author.id] = thread.id

			return thread
		except Exception as e:
			await ctx.reply(f"Ocorreu um erro ao criar a partida: {e}")

	@commands.command()
	async def vanguard(self, ctx):
		if not isinstance(ctx.channel, discord.TextChannel):
			await ctx.reply("Este comando só pode ser usado em um canal de texto padrão!")
			return

		if ctx.author.id in self.vanguards:
			await ctx.reply(f"Você já está em uma partida de Vanguard! Retorne para <#{self.vanguards.get(ctx.author.id)}>, ou feche-a com o comando '{utils.getPrefix(ctx)}exit' antes de iniciar outra!")
			return

		await ctx.reply("Estou criando uma Thread com sua partida de Vanguard!")
		thread = await self.createVanguardThread(ctx)
		await thread.send(f"Bem vindo ao Vanguard, {ctx.author.mention}!")

	@commands.command()
	async def exit(self, ctx):
		threadID = self.vanguards.get(ctx.author.id)

		if threadID is None:
			await ctx.reply("Você não está em uma partida de Vanguard!")
			return

		thread = self.bot.get_channel(threadID)

		if isinstance(thread, discord.Thread) and thread.owner_id == self.bot.user.id:
			try:
				await thread.delete()
				del self.vanguards[ctx.author.id]
				await ctx.send(f"Partida finalizada, {ctx.author.mention}!")
			except Exception as e:
				await ctx.reply(f"Ocorreu um erro ao tentar finalizar a partida: {e}")
		else:
			await ctx.reply("Você não pode sair dessa Thread, ela não foi criada por mim!")

async def setup(bot):
	await bot.add_cog(Vanguard(bot))
	print("Vanguard module has finished loading.\n")