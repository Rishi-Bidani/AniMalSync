import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

from Anilist import searchAnilistAnime
from mal import searchMAL

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = commands.Bot(command_prefix='$')


def list_to_string(theList):
    return ', '.join(theList)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.command()
async def searchanilist(ctx, animeName, maxResult=30):
    embedVar = discord.Embed(title=f"Search for: {animeName}", color=0x00ff00)
    result = searchAnilistAnime(animeName, maxResult)
    for obj in result:
        embedVar.add_field(name=f"{obj['title']['romaji']} - ({obj['siteUrl']})",
                           value=f"Type: {obj['type']}\nGenres: {list_to_string(obj['genres'])}",
                           inline=False)

    embedVar.set_image(url=result[0]['coverImage']['medium'])
    await ctx.channel.send(embed=embedVar)


@client.command()
async def searchmal(ctx, animeName):
    embedVar = discord.Embed(title=f"Search for: {animeName}", color=0x00ff00)
    for obj in searchMAL(animeName):
        embedVar.add_field(name=f"{obj['node']['title']}", value=f"ID: {obj['node']['id']}", inline=False)
    await ctx.channel.send(embed=embedVar)


client.run(TOKEN)
