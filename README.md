[<img src="https://img.shields.io/badge/Telegram-%40Me-orange">](https://t.me/Re_Diss)

[![Static Badge](https://img.shields.io/badge/Telegram-Bot%20Link-Link?style=for-the-badge&logo=Telegram&logoColor=white&logoSize=auto&color=blue)](https://t.me/TimeFarmCryptoBot?start=k0NH5BSlKpT4RaLR)

#### Подписывайтесь на наш [телеграм канал](https://t.me/scriptron). Там будут новости о новый ботах



> 🇪🇳 README in english available [here](README-EN.md)

## Функционал  
| Функционал                                              | Поддерживается |
|---------------------------------------------------------|:--------------:|
| Многопоточность                                         |       ✅        |
| Привязка прокси к сессии                                |       ✅        |
| Авто-клейм прибыли                                      |       ✅        |
| Выполнение заданий (кроме телеграм заданий)             |       ✅        |
| Поддержка tdata / pyrogram .session / telethon .session |       ✅        |


## [Настройки](https://github.com/Re-Diss/TimeFarmCryptoBot/blob/main/.env-example)
| Настройка               | Описание                                                                          |
|-------------------------|-----------------------------------------------------------------------------------|
| **API_ID / API_HASH**   | Данные платформы, с которой запускать сессию Telegram _(сток - Android)_          |
| **SLEEP_BETWEEN_CLAIM** | Задержка между **Claim** в секундах _(напр. [10, 15])_                            |
| **SLEEP_BETWEEN_TASK_CLAIM** | Задержка между **Клеймом вознаграждения за задание** в секундах _(напр. [5, 10])_ |
| **SLEEP_BETWEEN_FARMING** | Задержка между **Фармингом** в секундах _(напр. [10, 15])_                        |
| **USE_PROXY_FROM_FILE** | Использовать-ли прокси из файла `bot/config/proxies.txt` _(True / False)_         |


## Установка
Вы можете скачать [**Репозиторий**](https://github.com/Re-Diss/TimeFarmCryptoBot) клонированием на вашу систему и установкой необходимых зависимостей:
```shell
~ >>> git clone https://github.com/Re-Diss/TimeFarmCryptoBot.git
~ >>> cd TimeFarmCryptoBot

# Linux
~/TimeFarmCryptoBot >>> python3 -m venv venv
~/TimeFarmCryptoBot >>> source venv/bin/activate
~/TimeFarmCryptoBot >>> pip3 install -r requirements.txt
~/TimeFarmCryptoBot >>> cp .env-example .env
~/TimeFarmCryptoBot >>> nano .env  # Здесь вы обязательно должны указать ваши API_ID и API_HASH , остальное берется по умолчанию
~/TimeFarmCryptoBot >>> python3 main.py

# Windows
~/TimeFarmCryptoBot >>> python -m venv venv
~/TimeFarmCryptoBot >>> venv\Scripts\activate
~/TimeFarmCryptoBot >>> pip install -r requirements.txt
~/TimeFarmCryptoBot >>> copy .env-example .env
~/TimeFarmCryptoBot >>> # Указываете ваши API_ID и API_HASH, остальное берется по умолчанию
~/TimeFarmCryptoBot >>> python main.py
```

Также для быстрого запуска вы можете использовать аргументы, например:
```shell
~/TimeFarmCryptoBot >>> python3 main.py --action (1/2)
# Или
~/TimeFarmCryptoBot >>> python3 main.py -a (1/2)

# 1 - Создает сессию
# 2 - Запускает кликер
```
