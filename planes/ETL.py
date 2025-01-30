import pandas as pd

def ETL(df):
    drop_columns = [
        'Unnamed: 27', 'CARRIER_DELAY', 'WEATHER_DELAY',
        'NAS_DELAY', 'SECURITY_DELAY','LATE_AIRCRAFT_DELAY'
    ] 
    
    df.drop_duplicates(inplace=True)

    # Processa colonne relative alla data
    df = process_date_columns(df)
    
    # Calcola rapporto tra tempi reali e pianificati
    df['ACT_TO_CRS_RATIO'] = df['ACTUAL_ELAPSED_TIME'] / df['CRS_ELAPSED_TIME']
    
    # Aggiunge motivo di cancellazione
    df = add_cancellation_reason(df)
    
    # Rimuove colonne inutili
    df = df.drop(columns=drop_columns)

    df.fillna(0, inplace=True)

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

    df = df.drop(columns=['CANCELLATION_CODE'])

    return df
