import requests
import json

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
        }
    }
}
'''


def searchAnilistAnime(animeName, maxResult=30):
    variables = {
        'search': animeName,
        'page': 1,
        'perPage': maxResult
    }
    response = requests.post(url, json={'query': query, 'variables': variables})
    result = json.loads(response.text)
    return result["data"]["Page"]["media"]


# print(searchAnilistAnime("naruto"))