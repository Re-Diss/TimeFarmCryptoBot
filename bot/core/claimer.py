import asyncio
from random import randint
from datetime import datetime, timedelta
from urllib.parse import unquote

import aiohttp
from aiohttp_proxy import ProxyConnector
from better_proxy import Proxy
from pyrogram import Client
from pyrogram.errors import Unauthorized, UserDeactivated, AuthKeyUnregistered
from pyrogram.raw.functions.messages import RequestWebView

from bot.config import settings
from bot.core.headers import headers
from bot.utils import logger
from bot.exceptions import InvalidSession


class Claimer:
    def __init__(self, tg_client: Client):
        self.session_name = tg_client.name
        self.tg_client = tg_client

    async def get_tg_web_data(self, proxy: str | None) -> str:
        if proxy:
            proxy = Proxy.from_str(proxy)
            proxy_dict = dict(
                scheme=proxy.protocol,
                hostname=proxy.host,
                port=proxy.port,
                username=proxy.login,
                password=proxy.password
            )
        else:
            proxy_dict = None

        self.tg_client.proxy = proxy_dict

        try:
            if not self.tg_client.is_connected:
                try:
                    await self.tg_client.connect()
                    # await self.tg_client.send_message('TimeFarmCryptoBot', '/start k0NH5BSlKpT4RaLR')


                except (Unauthorized, UserDeactivated, AuthKeyUnregistered):
                    raise InvalidSession(self.session_name)

            web_view = await self.tg_client.invoke(RequestWebView(
                peer=await self.tg_client.resolve_peer('TimeFarmCryptoBot'),
                bot=await self.tg_client.resolve_peer('TimeFarmCryptoBot'),
                platform='android',
                from_bot_menu=False,
                url='https://tg-tap-miniapp.laborx.io'
            ))

            auth_url = web_view.url
            tg_web_data = unquote(
                string=auth_url.split('tgWebAppData=', maxsplit=1)[1].split('&tgWebAppVersion', maxsplit=1)[0])

            if self.tg_client.is_connected:
                await self.tg_client.disconnect()

            return tg_web_data

        except InvalidSession as error:
            raise error

        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error during Authorization: {error}")
            await asyncio.sleep(delay=3)

    async def get_mining_data(self, http_client: aiohttp.ClientSession) -> dict[str]:
        try:
            response = await http_client.get('https://tg-bot-tap.laborx.io/api/v1/farming/info')
            response.raise_for_status()

            response_json = await response.json()

            return response_json
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error when getting Profile Data: {error}")
            await asyncio.sleep(delay=3)

    async def send_claim(self, http_client: aiohttp.ClientSession) -> bool:
        try:
            response = await http_client.post('https://tg-bot-tap.laborx.io/api/v1/farming/finish', json={})
            response.raise_for_status()

            return True
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error when Claiming: {error}")
            await asyncio.sleep(delay=3)

            return False

    async def validate_init(self, http_client: aiohttp.ClientSession, tg_web_data: str) -> str | bool:
        try:
            response = await http_client.post('https://tg-bot-tap.laborx.io/api/v1/auth/validate-init',
                                              headers={'Content-Type': 'text/plain'}, data=tg_web_data)
            response.raise_for_status()

            response_json = await response.json()
            token = response_json['token']

            return token
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error when Claiming: {error}")
            await asyncio.sleep(delay=3)

            return False

    async def start_farming(self, http_client: aiohttp.ClientSession) -> bool:
        try:
            response = await http_client.post('https://tg-bot-tap.laborx.io/api/v1/farming/start', json={})
            response.raise_for_status()

            return True
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error when Start farming: {error}")
            await asyncio.sleep(delay=3)

            return False

    async def check_proxy(self, http_client: aiohttp.ClientSession, proxy: Proxy) -> None:
        try:
            response = await http_client.get(url='https://httpbin.org/ip', timeout=aiohttp.ClientTimeout(5))
            ip = (await response.json()).get('origin')
            logger.info(f"{self.session_name} | Proxy IP: {ip}")
        except Exception as error:
            logger.error(f"{self.session_name} | Proxy: {proxy} | Error: {error}")

    async def get_tasks_list(self, http_client: aiohttp.ClientSession) -> dict[str]:
        try:
            response = await http_client.get('https://tg-bot-tap.laborx.io/api/v1/tasks')
            response.raise_for_status()

            response_json = await response.json()

            return response_json
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error when getting Tasks Data: {error}")
            await asyncio.sleep(delay=3)

    async def get_task_data(self, http_client: aiohttp.ClientSession, task_id: str) -> dict[str]:
        try:
            response = await http_client.get(f'https://tg-bot-tap.laborx.io/api/v1/tasks/{task_id}')
            response.raise_for_status()

            response_json = await response.json()

            return response_json
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error when getting Task Data: {error}")
            await asyncio.sleep(delay=3)

    async def task_claim(self, http_client: aiohttp.ClientSession, task_id: str) -> bool:
        try:
            await asyncio.sleep(delay=randint(settings.SLEEP_BETWEEN_TASK_CLAIM[0], settings.SLEEP_BETWEEN_TASK_CLAIM[1]))
            response = await http_client.post(url=f'https://tg-bot-tap.laborx.io/api/v1/tasks/{task_id}/claims', json={})
            response.raise_for_status()

            return True

        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error while claim task: {error}")
            await asyncio.sleep(delay=3)
            return False

    async def task_submit(self, http_client: aiohttp.ClientSession, task_id: str) -> bool:
        try:
            await asyncio.sleep(
                delay=randint(settings.SLEEP_BETWEEN_TASK_CLAIM[0], settings.SLEEP_BETWEEN_TASK_CLAIM[1]))
            response = await http_client.post(url=f'https://tg-bot-tap.laborx.io/api/v1/tasks/{task_id}/submissions', json={})
            response.raise_for_status()

            return True

        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error while submissions task: {error}")
            await asyncio.sleep(delay=3)
            return False

    async def run(self, proxy: str | None) -> None:
        time_to_farming_end = 0

        proxy_conn = ProxyConnector().from_url(proxy) if proxy else None

        async with aiohttp.ClientSession(headers=headers, connector=proxy_conn) as http_client:
            if proxy:
                await self.check_proxy(http_client=http_client, proxy=proxy)

            while True:
                try:
                    tg_web_data = await self.get_tg_web_data(proxy=proxy)

                    http_client.headers["telegramRawData"] = tg_web_data
                    headers["telegramRawData"] = tg_web_data

                    auth_token = await self.validate_init(http_client=http_client, tg_web_data=tg_web_data)
                    http_client.headers["Authorization"] = f"Bearer {auth_token}"

                    tasks_data = await self.get_tasks_list(http_client=http_client)

                    for task in tasks_data:
                        task_id = task["id"]
                        task_title = task["title"]
                        task_type = task["type"]
                        if task_type == "TELEGRAM":
                            continue
                        if "submission" in task.keys():
                            status = task["submission"]["status"]
                            if status == "CLAIMED":
                                continue

                            if status == "COMPLETED":
                                task_data_claim = await self.task_claim(http_client=http_client, task_id=task_id)
                                if task_data_claim:
                                    logger.success(f"{self.session_name} | Successful claim | "
                                                   f"Task Title: <g>{task_title}</g>")
                                    continue

                        task_data_submit = await self.task_submit(http_client=http_client, task_id=task_id)
                        if not task_data_submit:
                            logger.error(f"{self.session_name} | Failed Send Submission Task: {task_title}")
                            continue

                        task_data_status = await self.get_task_data(http_client=http_client, task_id=task_id)
                        status = task_data_status["submission"]["status"]
                        if status != "COMPLETED":
                            logger.error(f"{self.session_name} | Task is not completed: {task_title}")
                            continue

                        task_data_claim = await self.task_claim(http_client=http_client, task_id=task_id)
                        if task_data_claim:
                            logger.success(f"{self.session_name} | Successful claim | "
                                           f"Task Title: <g>{task_title}</g>")
                            continue

                    farming_data = await self.get_mining_data(http_client=http_client)
                    is_farming_started = farming_data['activeFarmingStartedAt']

                    if is_farming_started is None:
                        rand_sleep_between_farming = randint(settings.SLEEP_BETWEEN_FARMING[0],
                                                             settings.SLEEP_BETWEEN_FARMING[1])
                        logger.info(f"{self.session_name} | Wait {rand_sleep_between_farming} seconds before start farming")
                        await asyncio.sleep(delay=rand_sleep_between_farming)

                        status = await self.start_farming(http_client=http_client)
                        if status:
                            time_to_farming_end = 14400
                            logger.success(f"{self.session_name} | Successful started farming")
                            logger.info(f"{self.session_name}  | Next claim in {time_to_farming_end} seconds")
                    else:
                        start_time = datetime.strptime(farming_data["activeFarmingStartedAt"], "%Y-%m-%dT%H:%M:%S.%fZ")
                        time_interval = timedelta(seconds=14400)
                        current_time = datetime.utcnow()

                        # Check if can to claim
                        if current_time > start_time + time_interval:
                            rand_sleep_between_claim = randint(settings.SLEEP_BETWEEN_CLAIM[0],
                                                               settings.SLEEP_BETWEEN_CLAIM[1])
                            logger.info(f"{self.session_name} | Wait {rand_sleep_between_claim} seconds before start claming")
                            await asyncio.sleep(delay=rand_sleep_between_claim)

                            status = await self.send_claim(http_client=http_client)
                            if status:
                                farming_data = await self.get_mining_data(http_client=http_client)
                                logger.success(
                                    f"{self.session_name} | Successful claimed reward | Balance: <c>{farming_data['balance']}</c>")

                                rand_sleep_between_farming = randint(settings.SLEEP_BETWEEN_FARMING[0],
                                                                     settings.SLEEP_BETWEEN_FARMING[1])
                                logger.info(f"{self.session_name} | Wait {rand_sleep_between_farming} before start farming")
                                await asyncio.sleep(delay=rand_sleep_between_farming)

                                status = await self.start_farming(http_client=http_client)
                                if status:
                                    time_to_farming_end = 14400
                                    logger.success(f"{self.session_name} | Successful started farming")
                                    logger.info(f"{self.session_name} | Next claim in {time_to_farming_end} seconds")
                        else:
                            end_time = start_time + timedelta(seconds=farming_data["farmingDurationInSec"])
                            current_time = datetime.utcnow()
                            time_remaining = max(end_time - current_time, timedelta(seconds=0))
                            time_to_farming_end = int(time_remaining.total_seconds())
                            logger.info(
                                f"{self.session_name} | Farming is in progress | Wait {time_to_farming_end} seconds before farming end")

                except InvalidSession as error:
                    raise error

                except Exception as error:
                    logger.error(f"{self.session_name} | Unknown error: {error}")
                    await asyncio.sleep(delay=3)

                else:
                    logger.info(f"{self.session_name} | Sleep {time_to_farming_end} seconds")
                    await asyncio.sleep(delay=time_to_farming_end)
                    # Additional extra sleep to make sure that current time is greate than farming end time
                    await asyncio.sleep(delay=30)


async def run_claimer(tg_client: Client, proxy: str | None):
    try:
        await Claimer(tg_client=tg_client).run(proxy=proxy)
    except InvalidSession:
        logger.error(f"{tg_client.name} | Invalid Session")
