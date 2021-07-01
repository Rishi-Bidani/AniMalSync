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
        }
    }
}
'''


def searchAnilistAnime(animeName):
    variables = {
        'search': animeName,
        'page': 1,
        'perPage': 30
    }
    response = requests.post(url, json={'query': query, 'variables': variables})
    result = json.loads(response.text)
    return result["data"]["Page"]["media"]


# print(searchAnilist("naruto"))
