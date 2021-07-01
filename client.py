import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

from Anilist import searchAnilistAnime

client = commands.Bot(command_prefix='$')


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.command()
async def searchAnilist(ctx, animeName):
    embedVar = discord.Embed(title=f"Search for: {animeName}", color=0x00ff00)
    for obj in searchAnilistAnime(animeName):
        embedVar.add_field(name=f"{obj['title']['romaji']}", value=f"ID: {obj['id']}", inline=False)
    await ctx.channel.send(embed=embedVar)


client.run(TOKEN)