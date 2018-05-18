import aiohttp
import asyncio
import async_timeout
import json


class KitsuClient():
    def __init__(self, client_id, client_secret, session=None):
        self.session = session or aiohttp.ClientSession()
        self.base_url = 'https://kitsu.io/api/edge/'
        self.client_id = client_id
        self.secret = client_secret
        self.headers = {
            'Accept': 'application/vnd.api+json',
            'Content-Type': 'application/json'
        }

    async def _fetch(self, url, params={}):
        with async_timeout.timeout(10):
            async with self.session.get(url=url, headers=self.headers, params=params) as request:
                try:
                    response = await request.text()
                    response = json.loads(response)
                except(asyncio.TimeoutError, aiohttp.ClientResponseError):
                    pass  # raise client error

            if request.status == 200 and response['data'] != None:
                if len(response['data']) == 1:
                    return response['data'][0]
                else:
                    return response['data']
            elif request.status == 404:
                pass  # raise NotFoundException
            elif request.status > 500:
                pass  # raise clientError
            else:
                pass  # raise clientError

    async def get_users(self, user_id=None, username=None):
        """"""
        params = {}
        if user_id:
            params['filter[id]'] = user_id
        if username:
            params['filter[name]'] = username

        user = await self._fetch('{0}users/'.format(self.base_url), params=params)
        f = await self._fetch('{0}users/{1}/favorites'.format(self.base_url, user['id']))
        characters = []
        anime = []
        manga = []
        for d in f:
            item = await self._fetch('{}/item'.format(d['links']['self']))
            item['attributes']['id'] = item['id']
            if item['type'] == 'characters':
                characters.append(item['attributes'])
            elif item['type'] == 'anime':
                anime.append(item['attributes'])
            elif item['type'] == 'manga':
                manga.append(item['attributes'])
        user['relationships']['favorites']['characters'] = characters
        user['relationships']['favorites']['anime'] = anime
        user['relationships']['favorites']['manga'] = manga
        return user