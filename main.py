import asyncio
import logging
from datetime import datetime
from typing import Dict, List

import pandas as pd
from binance import AsyncClient
import httpx
from dotenv import load_dotenv

from indicators import money_flow_index
from telegram import send_message
from binance_client import get_usdt_perpetual_symbols, fetch_klines

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


async def process_symbol(
    client: AsyncClient,
    http_session: httpx.AsyncClient,
    symbol: str,
    last_signals: Dict[str, int],
    period: int = 10,
) -> None:
    """Обрабатывает один символ: считает MFI и отправляет сигнал при необходимости."""
    try:
        klines = await fetch_klines(client, symbol, limit=period * 3)  # с запасом свечей для расчёта
    except Exception as e:
        logger.warning("Не удалось получить свечи %s: %s", symbol, e)
        return

    if len(klines) < period + 2:
        return  # данных мало

    # Binance kline: [0 open_time, 1 open, 2 high, 3 low, 4 close, 5 volume, 6 close_time, ...]
    df = pd.DataFrame(
        klines,
        columns=[
            "open_time",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "close_time",
            "quote_asset_volume",
            "number_of_trades",
            "taker_buy_base",
            "taker_buy_quote",
            "ignore",
        ],
    )
    df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)

    # Последняя свеча может быть незакрытой, используем вторую снизу
    latest_closed_idx = -2
    closed_df = df.iloc[: latest_closed_idx + 1]  # включая последнюю закрытую свечу

    mfi_series = money_flow_index(
        closed_df["high"], closed_df["low"], closed_df["close"], closed_df["volume"], period=period
    )
    latest_mfi = mfi_series.iloc[-1]
    if pd.isna(latest_mfi):
        return

    latest_close_time = int(closed_df["close_time"].iloc[-1])
    if latest_mfi <= 10 and last_signals.get(symbol) != latest_close_time:
        close_price = closed_df["close"].iloc[-1]
        message = (
            f"{symbol}\n"
            f"MFI 4h: {latest_mfi:.2f}\n"
            f"Price: {close_price:.2f}$"
        )
        try:
            await send_message(message, session=http_session)
            last_signals[symbol] = latest_close_time
            logger.info("Отправлен сигнал по %s | MFI=%.2f", symbol, latest_mfi)
        except Exception as e:
            logger.error("Ошибка отправки сигнала Telegram: %s", e)


async def main() -> None:
    client = await AsyncClient.create()
    symbols: List[str] = await get_usdt_perpetual_symbols(client)
    logger.info("Найдено %d USDT-M perpetual символов", len(symbols))

    last_signals: Dict[str, int] = {}

    async with httpx.AsyncClient(http2=True, timeout=15) as http_session:
        while True:
            tasks = [process_symbol(client, http_session, s, last_signals) for s in symbols]
            await asyncio.gather(*tasks, return_exceptions=True)
            logger.info("Цикл сканирования завершён, ожидание 5 минут…")
            await asyncio.sleep(300)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Завершение работы по Ctrl+C") 