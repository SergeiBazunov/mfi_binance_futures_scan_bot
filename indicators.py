import pandas as pd
import numpy as np


def money_flow_index(high: pd.Series, low: pd.Series, close: pd.Series, volume: pd.Series, period: int = 10) -> pd.Series:
    """Возвращает серию значений MFI.

    Parameters
    ----------
    high, low, close, volume : pd.Series
        Серии биржевых данных одной длины.
    period : int
        Период расчёта индикатора.
    """
    typical_price = (high + low + close) / 3
    money_flow = typical_price * volume

    # Определяем положительный и отрицательный денежный поток
    price_diff = typical_price.diff()
    positive_flow = np.where(price_diff > 0, money_flow, 0.0)
    negative_flow = np.where(price_diff < 0, money_flow, 0.0)

    positive_mf = pd.Series(positive_flow, index=high.index).rolling(window=period).sum()
    negative_mf = pd.Series(negative_flow, index=high.index).rolling(window=period).sum()

    # Избежать деления на ноль
    money_ratio = positive_mf / negative_mf.replace(0, np.nan)
    mfi = 100 - (100 / (1 + money_ratio))
    return mfi 