"""Stochastic Oscillator - KDJ indicator."""
import pandas as pd


class KDJ:
    """Stochastic Oscillator - KDJ indicator."""

    def __init__(self, n=9, m1=3, m2=3):
        """Initialize KDJ indicator with default parameters."""
        self.n = n
        self.m1 = m1
        self.m2 = m2
        self.high_list = []
        self.low_list = []
        self.rsv_list = []
        self.k_list = []
        self.d_list = []
        self.j_list = []

    def calcKDJ(self, high, low, close):
        """Calculate the KDJ values for the given high, low, and close prices."""
        self.high_list.append(high)
        self.low_list.append(low)

        if len(self.high_list) < self.n:
            return 50, 50, 50

        if len(self.high_list) > self.n:
            del self.high_list[0]
            del self.low_list[0]

        highest_high = max(self.high_list[-self.n :])
        lowest_low = min(self.low_list[-self.n :])
        rsv = (close - lowest_low) / (highest_high - lowest_low) * 100 if (highest_high - lowest_low) != 0 else 50

        self.rsv_list.append(rsv)

        if len(self.rsv_list) < self.m1:
            return 50, 50, 50

        if len(self.rsv_list) > self.m1:
            del self.rsv_list[0]

        k = (self.k_list[-1] * (self.m1 - 1) + rsv) / self.m1 if len(self.k_list) > 0 else 50
        d = (self.d_list[-1] * (self.m2 - 1) + k) / self.m2 if len(self.d_list) > 0 else 50
        j = 3 * k - 2 * d

        self.k_list.append(k)
        self.d_list.append(d)
        self.j_list.append(j)

        return round(k, 2), round(d, 2), round(j, 2)

    def apply_to_df(self, df, suffix=''):
        """Apply KDJ calculation to a DataFrame and return it with K, D, J columns added."""
        df[['K' + suffix, 'D' + suffix, 'J' + suffix]] = df.apply(
            lambda x: pd.Series(self.calcKDJ(x['high'], x['low'], x['close'])), axis=1
        )
        return df


if __name__ == '__main__':
    # 读取CSV文件并转换为DataFrame
    df = pd.read_csv(r'E:\SC000_SAR.csv', index_col='DateTime')
    kdj = KDJ(43, 9, 3)
    data = kdj.apply_to_df(df)
