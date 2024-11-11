import pandas as pd
import holidays

def ETL(df):
    # Rimuove i duplicati direttamente sul DataFrame originale
    df.drop_duplicates(inplace=True)

    cols_to_zero = ['CARRIER_DELAY', 'WEATHER_DELAY', 'NAS_DELAY', 'SECURITY_DELAY', 'LATE_AIRCRAFT_DELAY']

    # Filtra ed elimina le righe dove DEP_DELAY > 0 e ci sono NaN nelle colonne specificate
    df = df[~((df['DEP_DELAY'] > 0) & (df[cols_to_zero].isna().any(axis=1)))]

    # Imposta a zero i valori delle colonne specificate se DEP_DELAY <= 0
    df.loc[df['DEP_DELAY'] <= 0, cols_to_zero] = 0

    df.loc[:, 'FL_DATE'] = pd.to_datetime(df['FL_DATE'])

    df.loc[:, 'FL_MON'] = df['FL_DATE'].apply(lambda x: x.month)
    df.loc[:, 'FL_DAY'] = df['FL_DATE'].apply(lambda x: x.day)
    df.loc[:, 'FL_YEAR'] = df['FL_DATE'].apply(lambda x: x.year)
    df.loc[:, 'FL_DOW'] = df['FL_DATE'].apply(lambda x: x.dayofweek)

    df['CANCELLATION_REASON'] = df['CANCELLATION_CODE'].replace({
        'A': 'Airline/Carrier',
        'B': 'Weather',
        'C': 'National Air System',
        'D': 'Security'
    })

    # Create a list of US holidays per year
    us_holidays = holidays.US(years=df["FL_YEAR"].unique().tolist())

    # Create the IS_HOLIDAY column
    df['IS_HOLIDAY'] = df['FL_DATE'].apply(lambda x: 1 if x in us_holidays else 0)

    df.drop(columns=['FL_DATE', 'Unnamed: 27', 'CANCELLATION_CODE'], inplace=True)
    
    return df
