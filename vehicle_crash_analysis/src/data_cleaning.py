# src/data_cleaning.py

import pandas as pd


def clean_data(dataframes):
    for key, df in dataframes.items():
        # Drop columns with all null values
        df.dropna(axis=1, how='all', inplace=True)

        # Dynamically fill NaN values based on column data types
        for column in df.columns:
            if df[column].dtype == 'object':  # For string columns
                df[column] = df[column].fillna('')
            else:  # For numeric columns
                df[column] = df[column].fillna(0)
    
    return dataframes
