import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Select
from bokeh.layouts import column, row
from bokeh.io import curdoc


data = pd.read_csv('final.csv')
data['zip'] = data['zip'].astype(str)
data['month'] = data['month'].astype(str)

zips = sorted(data['zip'].unique())
zip1 = Select(title="Select a first zip code", value=zips[0], options=zips)
zip2 = Select(title="Select a second zip code", value=zips[1], options=zips)

all = ColumnDataSource(data=dict(month=[], response_time=[]))
selection1 = ColumnDataSource(data=dict(month=[], response_time=[]))
selection2 = ColumnDataSource(data=dict(month=[], response_time=[]))

def update():
    zip_sel1 = zip1.value
    zip_sel2 = zip2.value
    all_data = data.groupby('month')['response_time'].mean().reset_index()
    all.data = dict(month=all_data['month'], response_time=all_data['response_time'])
    data_zip1 = data[data['zip'] == zip_sel1].groupby('month')['response_time'].mean().reset_index()
    data_zip2 = data[data['zip'] == zip_sel2].groupby('month')['response_time'].mean().reset_index()
    selection1.data = dict(month=data_zip1['month'], response_time=data_zip1['response_time'])
    selection2.data = dict(month=data_zip2['month'], response_time=data_zip2['response_time'])

plot = figure(title="Response time in 2020 per month", x_axis_label='Month', y_axis_label='Response time in hours', height=600, width=900)
plot.line(x='month', y='response_time', source=all, color='blue', legend_label='All 2020')
plot.line(x='month', y='response_time', source=selection1, color='green', legend_label='Zip code 1')
plot.line(x='month', y='response_time', source=selection2, color='red', legend_label='Zip code 2')
plot.legend.location = "top_right"

update()

zip1.on_change('value', lambda attr, old, new: update())
zip2.on_change('value', lambda attr, old, new: update())
    
layout = column(row(zip1, zip2), plot)
curdoc().clear()
curdoc().add_root(layout)
curdoc().title = "nyc_dash"
