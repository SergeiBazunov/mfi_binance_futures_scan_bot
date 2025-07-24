# MFI Binance Futures Scan Bot

Телеграм-бот, который каждые 5 минут сканирует все USDT-M perpetual фьючерсы на бирже Binance и отправляет сигнал, если индикатор **MFI (Money Flow Index)** с периодом 10 на закрытой 4-часовой свече опускается до 10 или ниже.

## Установка

```bash
# Клонируем репозиторий
git clone https://github.com/SergeiBazunov/mfi_binance_futures_scan_bot
cd mfi_binance_futures_scan_bot

# Откройте папку проекта
cd mfi_binance_futures_scan_bot

# Устанавливаем зависимости
poetry install
```

## Установка на сервер Ubuntu (VPS)

Ниже пример для чистой Ubuntu 20.04/22.04 под пользователем **ubuntu** (с правами sudo).

```bash
# 1. Обновляем систему
sudo apt update && sudo apt upgrade -y

# 2. Ставим необходимые пакеты
sudo apt install -y git python3 python3-venv pipx
pipx ensurepath           # добавит ~/.local/bin в PATH
source ~/.bashrc          # перезагрузим переменные среды

# 3. Устанавливаем Poetry через pipx
pipx install poetry       # появится команда poetry

# 4. Клонируем проект
git clone https://github.com/SergeiBazunov/mfi_binance_futures_scan_bot.git
cd mfi_binance_futures_scan_bot

# 5. Устанавливаем зависимости (без root-установки пакета)
poetry install --no-root

# 6. Настраиваем переменные окружения
cp env.example .env
nano .env                 # TELEGRAM_TOKEN=...  CHAT_ID=...

# 7. Пробный запуск
poetry run python main.py # Ctrl+C для остановки
```

### Автозапуск через systemd

Создайте сервис-файл (от root):

```bash
sudo nano /etc/systemd/system/mfi-bot.service
```

Вставьте:

```ini
[Unit]
Description=Binance MFI 4h scanner bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/mfi_binance_futures_scan_bot
ExecStart=/home/ubuntu/.local/bin/poetry run python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Активируем сервис:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now mfi-bot.service
```

Проверить логи:

```bash
journalctl -u mfi-bot -f
```

Бот теперь работает в фоне и автоматически перезапустится после перезагрузки VPS или при сбоях.

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