import requests
import json
import traceback
import time
from dotenv import load_dotenv
import os

load_dotenv()
ANICLIENT = os.getenv('ANILIST_ID')
ANISECRET = os.getenv('ANILIST_SECRET')
ANI_TOKEN = os.getenv('ANILIST_TOKEN')

# Copy paste the following url in the browser
# https://anilist.co/api/v2/oauth/authorize?client_id={clientID}&response_type=token
# replacing the {clientID}
# with your client ID.It will ask you to log in and then provide you with the token to use.

url = 'https://graphql.anilist.co'
query = '''
query ($id: Int, $page: Int, $perPage: Int, $search: String) {
    Page (page: $page, perPage: $perPage) {
        pageInfo {
            total
            currentPage
            lastPage
            hasNextPage
            perPage
        }
        media (id: $id, search: $search) {
            id
            title {
                english
                romaji
            }
            coverImage {
                medium
            }
            genres
            siteUrl
            type
        }
    }
}
'''

mutation_query = '''
mutation ($id: Int, $mediaId: Int, $status: MediaListStatus) {
    SaveMediaListEntry (id: $id, mediaId: $mediaId, status: $status) {
        id
        status
    }
}
'''


def searchAnilistAnime(animeName, maxResult=30):
    variables = {
        'search': animeName,
        'page': 1,
        'perPage': maxResult,
    }
    response = requests.post(url, json={'query': query, 'variables': variables})
    result = json.loads(response.text)
    return result["data"]["Page"]["media"]


def mutate_query(id, status="COMPLETED"):
    variables = {
        'mediaId': id,
        'status': status
    }
    response = requests.post(url, json={'query': mutation_query, 'variables': variables}, headers={'Authorization': ANI_TOKEN})
    result = json.loads(response.text)
    print(result)


# print(searchAnilistAnime("naruto"))

mutate_query(112608)
