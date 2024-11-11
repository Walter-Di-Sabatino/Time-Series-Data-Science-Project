# ETL.py
import pandas as pd

def ETL(df):

    # Rimuove i duplicati direttamente sul DataFrame originale
    df.drop_duplicates(inplace=True)

    cols_to_zero = ['CARRIER_DELAY', 'WEATHER_DELAY', 'NAS_DELAY', 'SECURITY_DELAY', 'LATE_AIRCRAFT_DELAY']

    # Filtra ed elimina le righe dove DEP_DELAY > 0 e ci sono NaN nelle colonne specificate
    df = df[~((df['DEP_DELAY'] > 0) & (df[cols_to_zero].isna().any(axis=1)))]

    # Imposta a zero i valori delle colonne specificate se DEP_DELAY <= 0
    df.loc[df['DEP_DELAY'] <= 0, cols_to_zero] = 0

    df.FL_DATE = pd.to_datetime(df.FL_DATE)

    df["FL_MON"] = df.FL_DATE.apply(lambda x: x.month)
    df["FL_DAY"] = df.FL_DATE.apply(lambda x: x.day)
    df["FL_YEAR"] = df.FL_DATE.apply(lambda x: x.year)
    df["FL_DOW"] = df.FL_DATE.apply(lambda x: x.dayofweek)
    
    df.drop(columns=['FL_DATE','Unnamed: 27'], inplace=True)
    
    return df
