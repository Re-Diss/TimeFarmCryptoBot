from bot.core.agents import generate_random_user_agent

headers = {
        'Accept': '*/*',
        'Content-Type': 'application/json',
        'Accept-Language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
        'Connection': 'keep-alive',
        'Origin': 'https://tg-tap-miniapp.laborx.io',
        'Referer': 'https://tg-tap-miniapp.laborx.io/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': generate_random_user_agent(),
        'Sec-Ch-Ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'Sec-Ch-Ua-Mobile': '?1',
        'Sec-Ch-Ua-Platform': '"Android"',
}
