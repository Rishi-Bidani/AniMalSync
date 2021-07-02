from malupdate import Anime, User
from dotenv import load_dotenv
import os

load_dotenv()
MAL_TOKEN = os.getenv('MAL_TOKEN')

# print(User.login("Gateterr", "not my real password")) # This will return a token


def searchMAL(animeName):
    result = Anime.search(MAL_TOKEN, animeName, ['title', 'genres'])
    return result["data"]


# for i in searchMAL("naruto"):
#     print(i["node"])

