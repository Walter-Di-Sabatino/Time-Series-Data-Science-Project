import pandas as pd
import holidays

def ETL(df):
    """Funzione principale ETL che richiama le sottofunzioni."""
    cols_to_zero = ['CARRIER_DELAY', 'WEATHER_DELAY', 'NAS_DELAY', 'SECURITY_DELAY','LATE_AIRCRAFT_DELAY']
    time_columns = ['CRS_DEP_TIME', 'DEP_TIME', 'WHEELS_OFF', 'WHEELS_ON', 'CRS_ARR_TIME', 'ARR_TIME']
    drop_columns = ['FL_DATE', 'Unnamed: 27', 'CANCELLATION_CODE'] + time_columns  + cols_to_zero

    df.drop_duplicates(inplace=True)

    # Rimuove duplicati e righe non valide
    # df = remove_invalid_rows(df, cols_to_zero)
    
    # Gestisce voli deviati
    df = handle_diverted_flights(df)

    # Processa colonne relative alla data
    df = process_date_columns(df)
    
    # Processa colonne temporali
    df = process_time_columns(df, time_columns)
    
    # Calcola rapporto tra tempi reali e pianificati
    df['ACT_TO_CRS_RATIO'] = df['ACTUAL_ELAPSED_TIME'] / df['CRS_ELAPSED_TIME']
    
    # Aggiunge motivo di cancellazione
    df = add_cancellation_reason(df)
    
    # Aggiunge colonna per festività
    # df = add_holiday_column(df)


    # Rimuove colonne inutili
    df = clean_and_drop_columns(df, drop_columns)
    
    

    df.fillna(0, inplace=True)

    return df

# Sottofunzioni

def remove_invalid_rows(df, cols_to_zero):
    """Rimuove duplicati e filtra righe con valori non validi."""
    df = df[~((df['DEP_DELAY'] > 0) & (df[cols_to_zero].isna().any(axis=1)))]
    df.loc[df['DEP_DELAY'] <= 0, cols_to_zero] = 0
    return df

def process_date_columns(df):
    """Crea colonne relative alla data."""
    df['FL_DATE'] = pd.to_datetime(df['FL_DATE'])
    df = df.assign(
        FL_MON=df['FL_DATE'].dt.month,
        FL_DAY=df['FL_DATE'].dt.day,
        FL_YEAR=df['FL_DATE'].dt.year,
        FL_DOW=df['FL_DATE'].dt.dayofweek
    )
    return df

def parse_time_column(column):
    """Estrae ore e minuti da una colonna di orari."""
    times = pd.to_numeric(column, errors='coerce').fillna(0).astype(int).astype(str).str.zfill(4)
    return times.str[:2].astype(int), times.str[2:].astype(int)

def process_time_columns(df, time_columns):
    """Estrae ore e minuti per le colonne temporali."""
    for col in time_columns:
        hours, minutes = parse_time_column(df[col])
        df[f'{col}_HOUR'], df[f'{col}_MIN'] = hours, minutes
    return df

import numpy as np

def add_cancellation_reason(df):
    """Aggiunge la colonna per il motivo di cancellazione, gestendo esplicitamente i NaN."""
    cancellation_map = {
        'A': 'Airline/Carrier',
        'B': 'Weather',
        'C': 'National Air System',
        'D': 'Security'
    }
    
    # Gestione dei NaN
    df['CANCELLATION_REASON'] = df['CANCELLATION_CODE'].map(cancellation_map)
    df['CANCELLATION_REASON'] = df['CANCELLATION_REASON'].fillna('Not cancelled')

    
    return df

def add_holiday_column(df):
    """Aggiunge una colonna che indica se la data è una festività."""
    us_holidays = holidays.US(years=df["FL_YEAR"].unique())
    df['IS_HOLIDAY'] = df['FL_DATE'].isin(us_holidays).astype(int)
    return df

def clean_and_drop_columns(df, drop_columns):
    """Elimina le colonne inutili dal DataFrame."""
    df.drop(columns=drop_columns, inplace=True)
    return df

def handle_diverted_flights(df):
    """Gestisce i voli deviati impostando a zero le colonne specificate per voli deviati e senza motivo di cancellazione."""
    # Imposta a 0 i valori per i voli deviati
    df.loc[df['DIVERTED'] == 1, ['ARR_DELAY','AIR_TIME','ACTUAL_ELAPSED_TIME','ACT_TO_CRS_RATIO','CANCELLED', 
                                 'CARRIER_DELAY', 'WEATHER_DELAY', 'NAS_DELAY', 'SECURITY_DELAY', 
                                 'LATE_AIRCRAFT_DELAY']] = 0
    return df
