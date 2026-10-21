import pandas as pd
import numpy as np

def compute_dataset_stats(df, target_col=None):
    """
    Computes comprehensive dataset statistics using Pandas:
    - min: df[col].min()
    - max: df[col].max()
    - avg / mean: df[col].mean()
    - standard deviation: df[col].std()
    - median: df[col].median()
    - 25% (Q1): df[col].quantile(0.25)
    - 75% (Q3): df[col].quantile(0.75)
    - count: df[col].count()
    - missing values: df[col].isnull().sum()
    - categorical stats: unique, mode, top frequency
    """
    if df is None or df.empty:
        return {}

    num_cols = list(df.select_dtypes(include=[np.number]).columns)
    cat_cols = list(df.select_dtypes(exclude=[np.number]).columns)

    numeric_stats = []
    for col in num_cols:
        series = df[col].dropna()
        if not series.empty:
            count = int(series.count())
            min_val = float(series.min())
            max_val = float(series.max())
            avg_val = float(series.mean())
            std_val = float(series.std()) if count > 1 else 0.0
            median_val = float(series.median())
            q25_val = float(series.quantile(0.25))
            q75_val = float(series.quantile(0.75))
            missing = int(df[col].isnull().sum())

            numeric_stats.append({
                'column': col,
                'count': count,
                'min': round(min_val, 2),
                'max': round(max_val, 2),
                'avg': round(avg_val, 2),
                'std': round(std_val, 2),
                'median': round(median_val, 2),
                'q25': round(q25_val, 2),
                'q75': round(q75_val, 2),
                'missing': missing,
            })

    categorical_stats = []
    for col in cat_cols:
        series = df[col].dropna()
        if not series.empty:
            top_val = str(series.mode()[0]) if not series.empty else "N/A"
            top_freq = int(series.value_counts().iloc[0]) if not series.empty else 0
            categorical_stats.append({
                'column': col,
                'count': int(series.count()),
                'unique': int(series.nunique()),
                'top_value': top_val,
                'top_freq': top_freq,
                'missing': int(df[col].isnull().sum()),
            })

    target_info = None
    if target_col and target_col in df.columns:
        target_series = df[target_col].dropna()
        is_num = pd.api.types.is_numeric_dtype(target_series)
        if is_num:
            target_info = {
                'name': target_col,
                'type': 'Numeric',
                'min': round(float(target_series.min()), 2),
                'max': round(float(target_series.max()), 2),
                'avg': round(float(target_series.mean()), 2),
                'std': round(float(target_series.std()), 2) if target_series.count() > 1 else 0.0,
                'median': round(float(target_series.median()), 2),
            }
        else:
            vc = target_series.value_counts().head(8).to_dict()
            target_info = {
                'name': target_col,
                'type': 'Categorical',
                'unique': int(target_series.nunique()),
                'distribution': [{'label': str(k), 'count': int(v)} for k, v in vc.items()]
            }

    return {
        'overview': {
            'total_rows': int(len(df)),
            'total_columns': int(df.shape[1]),
            'numeric_count': len(num_cols),
            'categorical_count': len(cat_cols),
        },
        'numeric_stats': numeric_stats,
        'categorical_stats': categorical_stats,
        'target_info': target_info,
    }
