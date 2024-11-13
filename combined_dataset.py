import pandas as pd
import numpy as np

# Carica i dataset
dataset_x = [pd.read_csv(f'dataset/{x}.csv') for x in range(2009, 2019)]  # esempio per anni dal 2009 al 2017

# Parametri
y = 5  # numero minimo di righe per ogni giorno
min_rows, max_possible_rows = 5000, 6000

final_data = []
for df in dataset_x:
    print(len(df))
    max_rows = np.random.randint(min_rows, max_possible_rows)
    grouped = df.groupby('FL_DATE')

    selected_rows = []
    for _, group in grouped:
        sampled=[]
        if len(group) < y:
            sampled = group

        else:
            while len(sampled) < y:
                # Assumiamo che 'group' sia un DataFrame, y e max_rows siano già definiti
                n_samples = np.random.randint(y, max_rows // 365)  # Genera un numero di campioni tra y e max_rows / 365

                # Eseguiamo il campionamento con il numero di campioni determinato dinamicamente
                sampled = pd.concat([group.sample(n=n_samples, replace=True, random_state=np.random.randint(0, max_rows//365))])
            
        selected_rows.append(sampled)
    
    selected_data = pd.concat(selected_rows)

    if len(selected_data) < max_rows:
        # Aggiungi righe extra dal dataset originale per raggiungere max_rows
        remaining_rows = max_rows - len(selected_data)
        remaining_data = df.drop(selected_data.index).sample(n=remaining_rows, random_state=42)
        selected_data = pd.concat([selected_data, remaining_data])

    final_data.append(selected_data)

# Combina tutti i dati selezionati
final_combined_data = pd.concat(final_data, ignore_index=True)
final_combined_data.to_csv('dataset.csv', index=False)
