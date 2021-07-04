import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()
ANICLIENT = os.getenv('ANILIST_ID')
ANISECRET = os.getenv('ANILIST_SECRET')
ANI_TOKEN = os.getenv('ANILIST_TOKEN')

url = 'https://graphql.anilist.co'
query = '''
query ($id: Int, $page: Int, $perPage: Int, $search: String, $MediaType: MediaType) {
    Page (page: $page, perPage: $perPage) {
        pageInfo {
            total
            currentPage
            lastPage
            hasNextPage
            perPage
        }
        media (id: $id, search: $search, type: $MediaType) {
            id
            idMal
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

# search_by_id_query = '''
# query($id: Int) {
#     media(id: $id){
#         title {
#             english
#             romaji
#         }
#         sit
#     }
# }
# '''


def searchAnilistAnime(animeName, MediaType="ANIME", maxResult=30):
    variables = {
        'search': animeName,
        'page': 1,
        'perPage': maxResult,
        'MediaType': MediaType
    }
    response = requests.post(url, json={'query': query, 'variables': variables})
    result = json.loads(response.text)
    return result["data"]["Page"]["media"]


def mutate_query(idMut, status):
    variables = {
        'mediaId': idMut,
        'status': status
    }
    searchVar = {
        'id': idMut
    }
    response = requests.post(url, json={'query': mutation_query, 'variables': variables}, headers={'Authorization': ANI_TOKEN})
    result = json.loads(response.text)
    show_details_request = requests.post(url, json={'query': query, 'variables': searchVar})
    show_details = json.loads(show_details_request.text)
    # print(show_details["data"]["Page"]['media'])
    return result, show_details["data"]["Page"]['media']


# print(searchAnilistAnime("naruto"))

# mutate_query(4884)
