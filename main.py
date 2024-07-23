from dotenv import load_dotenv
from urllib.parse import urlsplit
import os
import requests
import argparse
from requests.exceptions import HTTPError


def compress_link(token, user_input):
    method = 'https://api.vk.ru/method/utils.getShortLink'
    params = {'access_token': token,
         'v': 5.199,
         'url': user_input,
         'private': 0}
    response = requests.get(method, params=params)
    response.raise_for_status()
    response_content = response.json()
    if 'error' in response_content:
        raise HTTPError('Проверьте ваш URL')
    else:
        return response_content['response']['short_url']


def click_stats(token, key):
    method = 'https://api.vk.ru/method/utils.getLinkStats'
    params = {
        'key': key,
        'access_token': token,
        'interval': 'forever',
        'extended': 0,
        'v': 5.199
    }
    response = requests.get(method, params=params)
    response.raise_for_status()
    response_content = response.json()
    if 'error' in response_content:
        raise HTTPError
    else:
        return response_content['response']['stats'][0]['views']


def verify_link(token, key):
    method = 'https://api.vk.ru/method/utils.getLinkStats'
    verify_link = False
    params = {
        'key': key,
        'access_token': token,
        'interval': 'forever',
        'extended': 0,
        'v': 5.199
    }
    response = requests.get(method, params=params)
    if 'error' not in response.text:
        verify_link = True
    return verify_link

if __name__ == '__main__':
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument('url', type=str, help='URL for receiving a shortened link or the number of clicks on it')
    args = parser.parse_args()
    url_structure = urlsplit(args.url)
    key = url_structure.path[1:]
    token = os.environ['VK_SERVER_KEY']
    if verify_link(token, key):
        print('Количество кликов по этой ссылке: {}'.format(click_stats(token, key)))
    else:
        short_link = compress_link(token, args.url)
        print('Сокращенная ссылка: {}'.format(short_link))

    