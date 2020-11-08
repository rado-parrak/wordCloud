import requests

def callGeneea(input):
    url = 'https://api.geneea.com/v3/analysis'
    headers = {
        'content-type': 'application/json',
        'Authorization': 'user_key d5d28d05b3272eb5ffb61ae5de9d044d'
    }
    return requests.post(url, json=input, headers=headers).json()