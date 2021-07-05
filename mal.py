from malupdate import Anime, User
from dotenv import load_dotenv
import requests
import os

load_dotenv()
MAL_TOKEN = os.getenv('MAL_TOKEN')
REQUEST_HEADERS = {
    "Host": "api.myanimelist.net",
    "Accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded",
    "X-MAL-Client-ID": "6114d00ca681b7701d1e15fe11a4987e",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
}


# print(User.login("Username", "not my real password")) # This will return a token

class myMalUpdate(Anime):
    def searchById(ACCESS_TOKEN, nameFromId):
        URL = f"https://api.myanimelist.net/v2/anime/{nameFromId}?fields=title"
        headers = REQUEST_HEADERS
        headers["Authorization"] = "Bearer {}".format(ACCESS_TOKEN)
        searchResults = requests.get(URL, headers=headers).json()
        return searchResults


def searchMAL(animeName):
    result = Anime.search(MAL_TOKEN, animeName, ['title', 'genres'])
    return result["data"]


def searchById(animeId):
    result = myMalUpdate.searchById(MAL_TOKEN, animeId)
    return result


def updateMAL(idMut, status):
    result = User.updateList(MAL_TOKEN, idMut, {'status': status})
    return result

# for i in searchMAL("naruto"):
#     print(i["node"])

# print(updateMAL(4884, "completed"))
# searchById(4884)