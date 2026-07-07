import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin


class PropertyCleaner(BaseEstimator, TransformerMixin):
    """Encapsulates cleaning (Steps 6-7) and feature engineering."""

    NONE_FILL_COLS = [
        'PoolQC', 'AddFeatures', 'Alley', 'BoundaryFeatures', 'QualFireplace',
        'BasementType', 'BasementFinish', 'BasementQual', 'BasementCond',
        'BsmntVisibility', 'BsmntFinQual1', 'BsmntFinish',
        'BsmntMaintenance', 'BsmntFinRat1'
    ]

    DROP_COLS = [
        'Street', 'Amenities', 'Condition2',
        'RoofMatl', 'Heating', 'AddFeatures', 'PoolQC'
    ]

    def fit(self, X, y=None):
        self.frontage_medians_ = X.groupby('Neighborhood')['PropertyFrontage'].median()
        self.global_frontage_median_ = X['PropertyFrontage'].median()
        self.electrical_mode_ = X['Electrical'].mode()[0]
        return self

    def transform(self, X):
        df = X.copy()

        for col in self.NONE_FILL_COLS:
            if col in df.columns:
                df[col] = df[col].fillna('None')

        df['ExteriorCladdingType'] = df['ExteriorCladdingType'].fillna('None')
        df['ExteriorCladdingArea'] = df['ExteriorCladdingArea'].fillna(0)
        df['BasementYrBlt'] = df['BasementYrBlt'].fillna(0)

        df['PropertyFrontage'] = df.apply(
            lambda row:
            self.frontage_medians_.get(
                row['Neighborhood'],
                self.global_frontage_median_
            )
            if pd.isna(row['PropertyFrontage'])
            else row['PropertyFrontage'],
            axis=1
        )

        df['Electrical'] = df['Electrical'].fillna(self.electrical_mode_)

        df['TotalSF'] = (
            df['BsmntSqFtage']
            + df['1stFlrSF']
            + df['2ndFlrSF']
        )

        df['TotalBath'] = (
            df['Bath1']
            + 0.5 * df['Bath2']
            + df['BsmtFullBath']
            + 0.5 * df['BsmtHalfBath']
        )

        df['HouseAge'] = df['SaleYr'] - df['YearBuilt']

        df['RemodAge'] = (
            df['SaleYr'] - df['YearRemodAdd']
        ).clip(lower=0)

        df['TotalPorchSF'] = (
            df['OpenPorchSF']
            + df['EnclosedPorch']
            + df['3SsnPorch']
            + df['ScreenPorch']
            + df['WoodDeckSF']
        )

        df['HasPool'] = (df['PoolArea'] > 0).astype(int)
        df['HasFireplace'] = (df['CntFireplaces'] > 0).astype(int)

        df = df.drop(
            columns=[c for c in self.DROP_COLS if c in df.columns]
        )

        return df