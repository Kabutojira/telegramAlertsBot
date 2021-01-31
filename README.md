# $GME price change alert
Check every 5 minutes Gamestop price changes and send Telegram alerts

## How to launch

install dependencyes with pip

```
pip install --user talib pandas yfinance numpy python-telegram-bot
```

Get your telegram bot token from https://telegram.me/botfather 

add your bot to your group


Launch bot

```
./fdaemon.py 'TELEGRAM_TOKEN'
```
