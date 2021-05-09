import aiohttp

#BASE_URL = 'https://www.osrsbotdetector.com/dev'
BASE_URL = 'http://127.0.0.1:5000'

async def get_slayer_labels(token):

    url = f'{BASE_URL}/discord/slayer/get_slayer_labels/{token}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            if r.status == 200:
                data = await r.json()
    try:
        return data
    except:
        return None

async def get_slayer_locations(token, label_name):

    url = f'{BASE_URL}/discord/slayer/get_slayer_location/{token}/{label_name}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            if r.status == 200:
                data = await r.json()
    try:
        return data
    except:
        return None
