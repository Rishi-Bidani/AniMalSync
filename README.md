# AniMalSync

This is a discord bot for updating and managing your Anilist and MyAnimeList account


## Setup
For setting up the project you will need to create a `.env` file with the following information

```env
# .env
DISCORD_TOKEN=discordTokenGoesHere
MAL_TOKEN=MALTokenGOesHere

# Anilist Credentials
ANILIST_ID=AnilistDeveloperAppID
ANILIST_SECRET=AnilistSecret

ANILIST_TOKEN=AnilistTokenHere
```

To get the MAL token
```python
from malupdate import Anime, User
print(User.login("Username", "Password")) # This will return a token
```

To Get Anilist Token
```text
Copy paste the following url in the browser
https://anilist.co/api/v2/oauth/authorize?client_id={clientID}&response_type=token
replacing the {clientID} with your ID, replace the {} as well
It will ask you to log in and then provide you with the token to use.
For me I copied the token from the url directly, it asked me to authorise the app and didn't reach anything else
```

## Commands

```gitignore
$searchanilist name maxResult

# name = What you want to search AnimeName or MangaName

# maxResult = max number of items displayed
```

```gitignore
$searchmal name
# name = what u want to search
```

