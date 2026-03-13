import pandas as pd


class IndicatorEngine:

    def rsi(self, prices, period: int = 14):

        if len(prices) < period:
            return None

        series = pd.Series(prices)

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

        return float(
            pd.Series(prices)
            .rolling(window)
            .mean()
            .iloc[-1]
        )

    def volatility(self, prices):

        if len(prices) < 2:
            return None

        returns = pd.Series(prices).pct_change()

        return float(returns.std())