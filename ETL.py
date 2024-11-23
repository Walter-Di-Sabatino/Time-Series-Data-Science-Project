import pandas as pd

def ETL(df):
    """Funzione principale ETL che richiama le sottofunzioni."""
    drop_columns = [
        'Unnamed: 27', 'CARRIER_DELAY', 'WEATHER_DELAY',
        'NAS_DELAY', 'SECURITY_DELAY','LATE_AIRCRAFT_DELAY'
    ] 
    
    df.drop_duplicates(inplace=True)

    # Gestisce voli deviati
    df = handle_diverted_flights(df)

    # Processa colonne relative alla data
    df = process_date_columns(df)
    
    # Calcola rapporto tra tempi reali e pianificati
    df['ACT_TO_CRS_RATIO'] = df['ACTUAL_ELAPSED_TIME'] / df['CRS_ELAPSED_TIME']
    
    # Aggiunge motivo di cancellazione
    df = add_cancellation_reason(df)
    
    # Rimuove colonne inutili
    df = clean_and_drop_columns(df, drop_columns)

    df.fillna(0, inplace=True)

    return df

# Sottofunzioni

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

def add_cancellation_reason(df):
    """Aggiunge la colonna per il motivo di cancellazione, gestendo esplicitamente i NaN."""
    cancellation_map = {
        'A': 'Airline/Carrier',
        'B': 'Weather',
        'C': 'National Air System',
        'D': 'Security'
    }
    
    # Gestione dei NaN
    df['C_REASON'] = df['CANCELLATION_CODE'].map(cancellation_map)
    df['C_REASON'] = df['C_REASON'].fillna('Not cancelled')

    df = clean_and_drop_columns(df, ['CANCELLATION_CODE'])
    return df

def clean_and_drop_columns(df, drop_columns):
    """Elimina le colonne inutili dal DataFrame."""
    df.drop(columns=drop_columns, inplace=True)
    return df

def handle_diverted_flights(df):
    """Gestisce i voli deviati impostando a zero le colonne specificate per voli deviati e senza motivo di cancellazione."""
    # Imposta a 0 i valori per i voli deviati
    df.loc[df['DIVERTED'] == 1, ['ARR_DELAY','AIR_TIME','ACTUAL_ELAPSED_TIME',
                                 'ACT_TO_CRS_RATIO','CANCELLED', ]] = 0
    return df
