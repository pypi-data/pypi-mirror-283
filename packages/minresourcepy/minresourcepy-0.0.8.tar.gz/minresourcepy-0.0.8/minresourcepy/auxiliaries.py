import pandas as pd
import numpy as np

def weights_cdf(df, weights):
    weights = np.array(df[weights])
    sumweights = np.sum(weights)
    df['weight_cdf'] = np.cumsum(weights) / sumweights
    return df

def is_numeric_column(df, column_name):
    numeric_values = pd.to_numeric(df[column_name], errors='coerce')
    non_numeric_values = numeric_values.isnull().any()
    return not non_numeric_values