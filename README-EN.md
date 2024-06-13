[<img src="https://img.shields.io/badge/Telegram-%40Me-orange">](https://t.me/Re_Diss)

[![Static Badge](https://img.shields.io/badge/Telegram-Bot%20Link-Link?style=for-the-badge&logo=Telegram&logoColor=white&logoSize=auto&color=blue)](https://t.me/TimeFarmCryptoBot?start=k0NH5BSlKpT4RaLR)


> 🇷🇺 README на русском доступен [здесь](README.md)

## Functionality
| Functional                                            | Supported |
|-------------------------------------------------------|:---------:|
| Multithreading                                        |     ✅     |
| Binding a proxy to a session                          |     ✅     |
| Auto-claiming of the revenue                          |     ✅     |
| Auto-completion of tasks                              |   soon    |
| Support tdata / pyrogram .session / telethon .session |     ✅     |

## [Settings](https://github.com/Re-Diss/TimeFarmCryptoBot/blob/main/.env-example)
| Settings                | Description                                                                |
|-------------------------|----------------------------------------------------------------------------|
| **API_ID / API_HASH**   | Platform data from which to launch a Telegram session (stock - Android)    |
| **SLEEP_BETWEEN_CLAIM** | Delay between **Claim** in seconds _(eg [10,15])_                          |
| **SLEEP_BETWEEN_FARMING** | Delay between **Farming** in seconds _(eg [10,15])_                        |
| **USE_PROXY_FROM_FILE** | Whether to use proxy from the `bot/config/proxies.txt` file (True / False) |

## Installation
You can download [**Repository**](https://github.com/Re-Diss/TimeFarmCryptoBot) by cloning it to your system and installing the necessary dependencies:
```shell
~ >>> git clone https://github.com/Re-Diss/TimeFarmCryptoBot.git
~ >>> cd TimeFarmCryptoBot

#Linux
~/TimeFarmCryptoBot >>> python3 -m venv venv
~/TimeFarmCryptoBot >>> source venv/bin/activate
~/TimeFarmCryptoBot >>> pip3 install -r requirements.txt
~/TimeFarmCryptoBot >>> cp .env-example .env
~/TimeFarmCryptoBot >>> nano .env # Here you must specify your API_ID and API_HASH , the rest is taken by default
~/TimeFarmCryptoBot >>> python3 main.py

#Windows
~/TimeFarmCryptoBot >>> python -m venv venv
~/TimeFarmCryptoBot >>> venv\Scripts\activate
~/TimeFarmCryptoBot >>> pip install -r requirements.txt
~/TimeFarmCryptoBot >>> copy .env-example .env
~/TimeFarmCryptoBot >>> # Specify your API_ID and API_HASH, the rest is taken by default
~/TimeFarmCryptoBot >>> python main.py
```

Also for quick launch you can use arguments, for example:
```shell
~/TimeFarmCryptoBot >>> python3 main.py --action (1/2)
# Or
~/TimeFarmCryptoBot >>> python3 main.py -a (1/2)

#1 - Create session
#2 - Run clicker
```
