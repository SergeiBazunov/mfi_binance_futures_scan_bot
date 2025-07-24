from binance import AsyncClient
from typing import List


async def get_usdt_perpetual_symbols(client: AsyncClient) -> List[str]:
    """Возвращает список символов USDT-M PERPETUAL, доступных для торговли."""
    exchange_info = await client.futures_exchange_info()
    symbols = [
        s["symbol"]
        for s in exchange_info["symbols"]
        if s["quoteAsset"] == "USDT" and s["contractType"] == "PERPETUAL" and s["status"] == "TRADING"
    ]
    return symbols


async def fetch_klines(
    client: AsyncClient,
    symbol: str,
    limit: int = 120,
):
    """Получает последние 4-часовые свечи для символа.

    Возвращает список кортежей в формате Binance API.
    """
    return await client.futures_klines(symbol=symbol, interval=AsyncClient.KLINE_INTERVAL_4HOUR, limit=limit) 