import os
import httpx
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


async def send_message(text: str, chat_id: str | None = None, token: str | None = None, session: httpx.AsyncClient | None = None) -> None:
    """Отправляет сообщение в Telegram.

    Parameters
    ----------
    text : str
        Текст сообщения.
    chat_id : str | None
        ID чата. Если не указан, берётся из переменной окружения CHAT_ID.
    token : str | None
        Токен бота. Если не указан, берётся из переменной окружения TELEGRAM_TOKEN.
    session : httpx.AsyncClient | None
        Сессия httpx. Можно передать, чтобы переиспользовать соединения.
    """
    token = token or TELEGRAM_TOKEN
    chat_id = chat_id or CHAT_ID

    if not token or not chat_id:
        raise ValueError("TELEGRAM_TOKEN и/или CHAT_ID не заданы в окружении")

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}

    if session is not None:
        response = await session.post(url, data=payload, timeout=10)
        response.raise_for_status()
    else:
        async with httpx.AsyncClient(http2=True) as client:
            response = await client.post(url, data=payload, timeout=10)
            response.raise_for_status() 