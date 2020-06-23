# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.offline import download_plotlyjs, init_notebook_mode,  plot
from plotly.graph_objs import *
init_notebook_mode()
import plotly.graph_objects as go

#################### Basic attributes

colors = ['rgb(67,67,67)', 'rgb(115,115,115)', 'rgb(49,130,189)', 'rgb(189,189,189)']


#################### new cases data
dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d').date()

df_new_cases= pd.read_csv('owid-covid-data.csv', parse_dates=['date'], date_parser=dateparse)
df_new_cases= df_new_cases[["location","date","total_cases","new_cases"]]
df_new_cases= df_new_cases[df_new_cases["location"].str.contains("Germany", case=False, na=False)]
#removing seconds from Date
df_new_cases['date'] = pd.to_datetime(df_new_cases['date']).dt.date

#################### reading oxford covid policy tracker data

#parsing date reformatting
dateparse = lambda x: pd.datetime.strptime(x, '%Y%m%d').date()
#selected columns
df= pd.read_csv('OxCGRT_latest.csv',parse_dates=['Date'], date_parser=dateparse)
df= df[["CountryName","Date","C1_School closing","C2_Workplace closing","C3_Cancel public events","C4_Restrictions on gatherings",
    "C5_Close public transport","C6_Stay at home requirements","C7_Restrictions on internal movement"]]
#filtering Germany only
df= df[df["CountryName"].str.contains("Germany", case=False, na=False)]

#removing seconds from Date
df['Date'] = pd.to_datetime(df['Date']).dt.date

#data start date and end date
start_date = df['Date'].iloc[0]
total_days = df.shape[0]
end_date = df['Date'].iloc[total_days-1]

#extracting only dates for policy tracker
df_new_cases = df_new_cases.loc[(df_new_cases['date']>=start_date) & (df_new_cases['date']<=end_date)]

 
#################### merging new cases with covid policy tracker data
df['new_cases'] = df_new_cases['new_cases'].values



#################### normalizing data
#cols_to_norm = ["C1_School closing","C2_Workplace closing","C3_Cancel public events","C4_Restrictions on gatherings",
#    "C5_Close public transport","C6_Stay at home requirements","C7_Restrictions on internal movement"]
#df[cols_to_norm] = df[cols_to_norm].apply(lambda x: (x - x.min()) / (x.max() - x.min()))

##################### Line chart

# plotly setup and traces
fig = go.Figure()



fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df['new_cases'],
    mode='lines',
    marker=dict(color='blue'),
    name="new_cases"
    ))

########################### first lockdown for C1-C7 and date imposed
for j, colName in enumerate(df.columns[2:9]):
    print(colName)
#     print(j,colName)
    for i, row in df.iterrows():
    
        df_column_val = df.loc[i, colName]
        if df_column_val>0:
            #first lockdown data
            date= df.loc[i, 'Date']
            print("Date imposed: ", date)
            print("lockdown: ",df_column_val)
            
            ################################ drawing verticle line on lockdown date
            
            fig.add_trace(go.Scatter(x=[date, date],
                          y=[0,6000],
                          mode="lines",
                          marker=dict(size=12,line=dict(width=0.8),
                                      colors[j]),
                          name=colName
                            ))
            
            break

        


# # Add range slider
# fig.update_layout(
#     width=800,
#     xaxis=dict(
#         rangeselector=dict(
#             buttons=list([
#                 dict(count=1,
#                       label="1m",
#                       step="month",
#                       stepmode="backward"),
#                 dict(count=6,
#                       label="6m",
#                       step="month",
#                       stepmode="backward"),
#                 dict(count=1,
#                       label="YTD",
#                       step="year",
#                       stepmode="todate"),
#                 dict(count=1,
#                       label="1y",
#                       step="year",
#                       stepmode="backward"),
#                 dict(step="all")
#             ])
#         ),
#         rangeslider=dict(
#             visible=True
#         ),
#         type="date"
#     )
# )

# # format and show figure
# fig.show()




##################### Line chart method 1



# trace0 = Scatter(
#         x=df['Date'],
#         y=df['new_cases'],
#         mode='lines',
#         marker=dict(color='blue')
# )
# data = [trace0]
# layout = Layout(
#     showlegend=False,
#     height=600,
#     width=600,
# )


# fig = dict( data=data, layout=layout )



# plot(fig)  


##################### old code



# # set up plotly figure
# fig = go.Figure()

# # Add title and axis names
# data1 = go.Scatter(
#         x=df['Date'],
#         y=df['C2_Workplace closing'],
#         mode='markers',
#         marker=dict(color='blue')
#     )


# data2 = go.Scatter(
#         x=df['Date'],
#         y=df['C1_School closing'],
#         mode='markers',
#         marker=dict(color='green')
#     )


# # Horizontal line shape
# shapes=[dict(
#         type='line',
#         x0 = df['C1_School closing'].loc[i],
#         y0 = i + 1,
#         x1 = df['C1_School closing'].loc[i],
#         y1 = i + 1,
#         line = dict(
#             color = 'grey',
#             width = 2
#         )
#     ) for i in range(len(df['C1_School closing']))]

# layout = go.Layout(
#     #shapes = shapes,
#     title='Lollipop Chart'
# )

# # Plot the chart
# go.Figure([data1, data2])

