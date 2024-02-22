"""Parabolic Stop and Reverse (SAR) indicator."""


class SAR:
    """Parabolic Stop and Reverse (SAR) indicator."""

    def __init__(self, max_af=0.2, af_step=0.02):
        """Initialize SAR indicator with default parameters."""
        self.max_af = max_af
        self.af = af_step
        self.af_step = af_step
        self.high_price_trend = []
        self.low_price_trend = []

        # Lists to track results
        self.psar_list = []
        self.af_list = []
        self.high_list = []
        self.low_list = []
        self.trend_list = []
        self.next_psar_list = []
        self.last_high = 0
        self.last_low = 0

    def calcPSAR(self, high, low):
        """Calculate the Parabolic Stop and Reverse (SAR) value for the given high and low prices."""
        if len(self.psar_list) > 0:
            psar = self._calcPSAR(high, low)
            psar = self._updateCurrentVals(psar, high, low)
        else:
            psar = self._initPSARVals(high, low)

        self.last_high = high
        self.last_low = low

        return psar

    def _initPSARVals(self, high, low):
        """Initialize the SAR values for the first calculation."""
        self.trend = 0
        psar = high
        self.high_price_trend.append(high)
        self.low_price_trend.append(low)
        self.psar_list.append(psar)
        self.af_list.append(self.af)
        self.high_list.append(high)
        self.low_list.append(low)
        self.trend_list.append(self.trend)
        self.next_psar_list.append(high)

        return psar

    def _calcPSAR(self, high, low):
        """Calculate the SAR value based on the current trend."""
        self.high_price_trend.append(high)
        self.low_price_trend.append(low)

        self.af = min(self.af + self.af_step, self.max_af)

        prev_psar = self.psar_list[-1]
        if self.trend == 1:  # Up
            psar = prev_psar + self.af * (self.last_high - prev_psar)
            next_psar = psar + self.af * (high - psar)
        else:
            psar = prev_psar - self.af * (prev_psar - self.last_low)
            next_psar = psar - self.af * (psar - low)

        self.next_psar_list.append(next_psar)

        return psar

    def _updateCurrentVals(self, psar, high, low):
        """Update the SAR values based on the current trend."""
        psar = self._trendReversal(psar, high, low)

        self.psar_list.append(psar)
        self.af_list.append(self.af)
        self.high_list.append(high)
        self.low_list.append(low)
        self.trend_list.append(self.trend)

        return psar

    def _trendReversal(self, psar, high, low):
        """Check for trend reversals and update SAR values accordingly."""
        reversal = False
        if self.trend == 1 and psar > low:
            self.trend = 0
            psar = max(self.high_price_trend)
            reversal = True
            next_psar = psar - self.af_step * (psar - low)
        elif self.trend == 0 and psar < high:
            self.trend = 1
            psar = min(self.low_price_trend)
            reversal = True
            next_psar = psar + self.af_step * (high - psar)

        if reversal:
            self.af = self.af_step
            self.high_price_trend.clear()
            self.low_price_trend.clear()
            self.high_price_trend.append(high)
            self.low_price_trend.append(low)
            self.next_psar_list[-1] = next_psar

        return psar


if __name__ == '__main__':
    import pandas as pd

    # 读取CSV文件并转换为DataFrame
    df = pd.read_csv(r'E:\SC000_SAR.csv', index_col='DateTime')
    indic = SAR(0.2, 0.2)
    df['PSAR'] = df.apply(lambda x: indic.calcPSAR(x['High'], x['Low']), axis=1)
