# MFI Binance Futures Scan Bot

Телеграм-бот, который каждые 5 минут сканирует все USDT-M perpetual фьючерсы на бирже Binance и отправляет сигнал, если индикатор **MFI (Money Flow Index)** с периодом 10 на закрытой 4-часовой свече опускается до 10 или ниже.

## Установка

```bash
# Клонируем репозиторий
git clone <repo-url>
cd mfi_binance_futures_scan_bot

# Устанавливаем Poetry
pip install poetry

# Устанавливаем зависимости
poetry install
```

## Конфигурация

Создайте файл `.env` (или скопируйте `env.example`) и заполните:

```
TELEGRAM_TOKEN=ваш_токен_бота
CHAT_ID=id_чата
```

## Запуск

```bash
poetry run python main.py
```

Бот будет каждые 5 минут проверять рынок и присылать сообщения вида:

```
BTCUSDT
MFI 4h: 9.75
Price: 50234.21$
``` 