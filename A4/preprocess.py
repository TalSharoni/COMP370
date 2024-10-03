import pandas as pd
import warnings
warnings.filterwarnings("ignore")

chunksize = 1000
combined = pd.DataFrame()

for chunk in pd.read_csv('filtered_nyc311.csv', chunksize=chunksize, header=None):
    df = chunk[chunk[19] == 'Closed']
    df.dropna(subset=[2, 9], inplace=True) 

    df[1] = pd.to_datetime(df[1])
    df[2] = pd.to_datetime(df[2])

    df['response_time'] = (df[2] - df[1]).dt.total_seconds() / 3600
    df = df[df['response_time'] >= 0]
    df['month'] = df[2].dt.strftime('%m')
    df['zip'] = df[8].astype(str).str.replace('.0', '', regex=False)
    mAvr = df.groupby(['month', 'zip'])['response_time'].mean().reset_index()
    combined = pd.concat([combined, mAvr], ignore_index=True)

mAvr = combined.groupby(['month', 'zip'])['response_time'].mean().reset_index()
mAvr.dropna(subset=['zip'], inplace=True)
mAvr.to_csv('final.csv', index=False)