import pandas as pd


class IndicatorEngine:

    def _series(self, prices):
        return pd.Series(prices)

    def rsi(self, prices, period: int = 14):

        if len(prices) < period:
            return None

        series = self._series(prices)

        delta = series.diff()

        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.rolling(period).mean()
        avg_loss = loss.rolling(period).mean()

        rs = avg_gain / avg_loss

        rsi = 100 - (100 / (1 + rs))

        return float(rsi.iloc[-1])

    def ma(self, prices, window: int = 20):

        if len(prices) < window:
            return None

        series = self._series(prices)

        return float(
            series
            .rolling(window)
            .mean()
            .iloc[-1]
        )

    def volatility(self, prices):

        if len(prices) < 2:
            return None

        series = self._series(prices)

        returns = series.pct_change()

        return float(returns.std())
    def ema(self, prices, span: int = 20):

        if len(prices) < span:
            return None

        series = self._series(prices)

        ema = series.ewm(span=span, adjust=False).mean()

        return float(ema.iloc[-1])
    def bollinger(self, prices, window: int = 20, num_std: int = 2):

        if len(prices) < window:
            return None

        series = self._series(prices)

        ma = series.rolling(window).mean()
        std = series.rolling(window).std()

        upper = ma + num_std * std
        lower = ma - num_std * std

        return {
            "middle": float(ma.iloc[-1]),
            "upper": float(upper.iloc[-1]),
            "lower": float(lower.iloc[-1])
        }
    def macd(self, prices):

        if len(prices) < 26:
            return None

        series = self._series(prices)

        ema12 = series.ewm(span=12, adjust=False).mean()
        ema26 = series.ewm(span=26, adjust=False).mean()

        macd = ema12 - ema26
        signal = macd.ewm(span=9, adjust=False).mean()

        return {
            "macd": float(macd.iloc[-1]),
            "signal": float(signal.iloc[-1])
        }
    def compute(self, name, prices):

        func = getattr(self, name, None)

        if not func:
            return None

        return func(prices)