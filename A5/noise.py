import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg') 

noise_types = ['Noise', 'Noise - Commercial', 'Noise - Helicopter', 'Noise - House of Worship', 'Noise - Park', 'Noise - Residential', 'Noise - Street/Sidewalk', 'Noise - Vehicle']

chunksize = 1000
combined = pd.DataFrame()

for chunk in pd.read_csv('A5/filtered_nyc311.csv', chunksize=chunksize, header=None):
    df = chunk[[5, 1]]
    df.columns = ['complaint_type', 'date']
    df = df[df['complaint_type'].isin(noise_types)]
    combined = pd.concat([combined, df], ignore_index=True)

combined.reset_index(drop=True, inplace=True)  

combined['date'] = pd.to_datetime(combined['date'], format='%m/%d/%Y %I:%M:%S %p')
combined['month'] = combined['date'].dt.to_period('M')

data = combined.groupby(['month', 'complaint_type']).size().reset_index(name='count')

total = data.groupby('month')['count'].sum().reset_index(name='total_count')
data = data.merge(total, on='month')
data['normalized'] = data['count'] / data['total_count']

total = data.pivot(index='month', columns='complaint_type', values='count').fillna(0)
normalized = data.pivot(index='month', columns='complaint_type', values='normalized').fillna(0)

total.index = total.index.start_time
normalized.index = normalized.index.start_time

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 12), sharex=True)

for column in total.columns:
    ax1.plot(total.index, total[column], label=column)

for column in normalized.columns:
    ax2.plot(normalized.index, normalized[column], label=column)

ax1.set_title('Total Noise Complaint Counts')
ax1.set_ylabel('Count')
ax1.legend(title='Complaint Type')
ax2.set_title('Normalized Noise Complaint Counts')
ax2.set_ylabel('Frequency')
ax2.legend(title='Complaint Type')

plt.xlabel('Month')
plt.savefig('A5/noise_complaints.png')