import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg') 

descriptions = ['Mouse Sighting', 'Rat Sighting']

chunksize = 1000
combined = pd.DataFrame()

for chunk in pd.read_csv('A5/filtered_nyc311.csv', chunksize=chunksize, header=None):
    df = chunk[[5, 6, 7]]
    df.columns = ['complaint_type', 'description', 'location']
    df = df[df['complaint_type'].str.contains('Rodent', na=False)]  
    df = df[df['description'].isin(descriptions)]
    df = df[['location']] 
    combined = pd.concat([combined, df], ignore_index=True)

combined.reset_index(drop=True, inplace=True) 

counts = combined['location'].value_counts()
percentages = counts / counts.sum() * 100

counts = percentages[percentages >= 1.2]
counts['Other'] = percentages[percentages < 1.2].sum()
counts.index = counts.index.str.replace('Other \(Explain Below\)', 'Not a Location Listed', regex=True)

plt.figure(figsize=(10, 7))
plt.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=90)
plt.title('Rodent Sighting Complaints by Location')
plt.savefig('A5/rodent_locations.png')
