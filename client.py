import os
import discord
from discord import Color
from discord.ext import commands
from dotenv import load_dotenv

from Anilist import searchAnilistAnime, mutate_query
from mal import searchMAL, searchById, updateMAL

# =================== COLORS =====================
RED = Color.red()
GREEN = Color.green()
# ================================================
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = commands.Bot(command_prefix='$')


def list_to_string(theList):
    return ', '.join(theList)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


# ======================================================================================== #
# ============================== Anilist Commands ======================================== #
# ======================================================================================== #

@client.command()
async def searchani(ctx, animeName, MediaType="ANIME", maxResult=30):
    """
    :param ctx: Just a context - worry about this parameter - it's used to display messages etc.
    :param animeName: THe anime Name you want to search
    :param MediaType: anime or manga, default is anime, use any of the following to change it to manga
                      ["m", "manga", "MANGA", "man"]
    :param maxResult: Max number of items you want to display
    :return: embedded message
    """
    if MediaType in ["m", "manga", "MANGA", "man"]:
        MediaType = "MANGA"
    else:
        MediaType = "ANIME"

    embedVar = discord.Embed(title=f"Search for: {animeName}", color=0x00ff00)
    result = searchAnilistAnime(animeName, MediaType, maxResult)
    for obj in result:
        stype = obj['type']  # Show Type - Anime, Manga
        ani_id = obj['id']  # AniList Id
        mal_id = obj['idMal']  # MyAnimeList ID
        genres = list_to_string(obj['genres'])
        empty = ""
        # embedVar.add_field(name=f"{obj['title']['romaji']} - ({obj['siteUrl']})",
        #                    value=f"Type: {stype}\n**AniList ID: ** {ani_id}   **MAL ID: **{mal_id}\nGenres: {genres}",
        #                    inline=False)
        embedVar.add_field(name=f"{obj['title']['romaji']}", value=f"Link: {obj['siteUrl']}", inline=False)
        embedVar.add_field(name="Type: ", value=f"{stype}", inline=True)
        embedVar.add_field(name="AniList ID: ", value=f"{ani_id}", inline=True)
        embedVar.add_field(name="MAL ID: ", value=f"{mal_id}", inline=True)
        embedVar.add_field(name="Genres: ", value=f"{genres}\n\n", inline=False)
        embedVar.add_field(name="__________", value=f"** **\n")

    embedVar.set_image(url=result[0]['coverImage']['medium'])
    await ctx.channel.send(embed=embedVar)


@client.command()
async def updateani(ctx, idMut, status="COMPLETED"):
    """
    :param ctx: context, for sending messages
    :param idMut: ID of the anime
    :param status: completed/planning/dropped - check if else below
    :return: sends and embed message with the status specified(after update) or an error message
    """
    if status == "COMPLETED":
        status = "COMPLETED"
    elif status in ["c", "curr", "current", "CURRENT"]:
        status = "CURRENT"
    elif status in ["p", "plan", "planning", "PLANNING"]:
        status = "PLANNING"
    elif status in ["d", "drop", "DROPPED"]:
        status = "DROPPED"
    else:
        embed_err = discord.Embed(title="Somthing went Wrong", color=RED)
        await ctx.channel.send(embed=embed_err)
        return
    print(status)
    resp = mutate_query(idMut, status)
    print(resp)
    embedVar = discord.Embed(title=f"Updated: {idMut}", color=0x00ff00)
    embedVar.add_field(name="Title",
                       value=f"English:{resp[1][0]['title']['english']}\nRomaji: {resp[1][0]['title']['romaji']}\n")

    embedVar.add_field(name=f"Status:", value=resp[0]['data']['SaveMediaListEntry']['status'])
    embedVar.set_image(url=resp[1][0]['coverImage']['medium'])
    await ctx.channel.send(embed=embedVar)


# ======================================================================================== #
# =================================== MAL Commands ======================================= #
# ======================================================================================== #

@client.command()
async def searchmal(ctx, animeName):
    embedVar = discord.Embed(title=f"Search for: {animeName}", color=0x00ff00)
    for obj in searchMAL(animeName):
        embedVar.add_field(name=f"{obj['node']['title']}", value=f"ID: {obj['node']['id']}", inline=False)
    await ctx.channel.send(embed=embedVar)


@client.command()
async def updatemal(ctx, idMut, status="completed"):
    animeName = searchById(idMut)["title"]
    if status == "completed":
        status = "completed"
    elif status in ["c", "curr", "current", "CURRENT", "w", "watch", "watching", "WATCHING"]:
        status = "watching"
    elif status in ["p", "plan", "planning", "PLANNING", "plantowatch", "plan_to_watch"]:
        status = "plan_to_watch"
    elif status in ["d", "drop", "DROPPED"]:
        status = "dropped"
    else:
        embed_err = discord.Embed(title="Somthing went Wrong", color=RED)
        await ctx.channel.send(embed=embed_err)
        return
    updateQuery = updateMAL(idMut, status)
    embedVar = discord.Embed(title=f"Updating: {idMut}", color=GREEN)
    embedVar.add_field(name=f"Title: ", value=f"{animeName}\n", inline=True)
    embedVar.add_field(name="Status: ", value=f"{updateQuery['status']}\n", inline=True)
    await ctx.channel.send(embed=embedVar)


client.run(TOKEN)
