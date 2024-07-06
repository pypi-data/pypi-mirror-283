
import pandas as pd

from src.correlation_analysis import CorrelationAnalysis
from src.dips import Dips
from src.increases import Increases
from src.moving_average import MovingAverage
from src.outliers_iqr import OutliersIQR
from src.pct_change import PercentageChange
from src.summary_statistics import SummaryStatistics
from src.trend_analysis import TrendAnalysis


class DataFrameAnalyzer:
    def __init__(self, df):
        self.df = df
        self.summary_stats = SummaryStatistics(df)
        self.pct_change = PercentageChange(df)
        self.outliers_iqr = OutliersIQR(df)
        self.dips = Dips(df)
        self.trend_analysis = TrendAnalysis(df)
        self.moving_average = MovingAverage(df)
        self.correlation_analysis = CorrelationAnalysis(df)
        self.increases = Increases(df)

    def analyze(self):
        output = []
        output.append("\nSummary Statistics:")
        output.append(str(self.summary_stats.calculate()))

        output.append("\nMonth-to-Month Percentage Changes:")
        output.append(str(self.pct_change.calculate()))

        output.append("\nOutliers Detection IQR:")
        output.append(str(self.outliers_iqr.detect()))

        output.append("\nCalculating Dips:")
        output.append(str(self.dips.calculate()))

        output.append("\nTrend Analysis (Linear Regression):")
        for column, (slope, intercept) in self.trend_analysis.analyze().items():
            output.append(f"Column: {column}, Slope: {slope}, Intercept: {intercept}")

        output.append("\nMoving Average (3 months window):")
        output.append(str(self.moving_average.calculate()))

        output.append("\nCalculating Increases:")
        output.append(str(self.increases.calculate()))

        output.append("\nCorrelation Analysis:")
        output.append(str(self.correlation_analysis.calculate()))

        output.append("\nFinal DataFrame:")
        output.append(str(self.df))

        return "\n".join(output)


if __name__ == "__main__":
    data = {
        "month": [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ],
        "stock_price": [
            50.0,
            51.5,
            49.8,
            52.0,
            53.2,
            54.0,
            55.0,
            56.0,
            57.5,
            59.0,
            60.0,
            61.0,
        ],
    }

    df = pd.DataFrame(data)
    a = DataFrameAnalyzer(df)
    print(a.analyze())
