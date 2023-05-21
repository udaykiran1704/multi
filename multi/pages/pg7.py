import dash
import pandas as pd
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go
from dash import dcc
from dash import html
from flask import Flask
import numpy as np
import plotly.express as px




# To create meta tag for each page, define the title, image, and description.
dash.register_page(__name__,
                   path='/Predictive',  # '/' is home page and it represents the url
                   name='Prediction',  # name of page, commonly used as name of link
                   title='Index',  # title that appears on browser's tab
                   
)

# page 1 data

# Load data
data = pd.read_csv('ALL.csv')

# Define conditions and corresponding values
conditions = [
    (data.iloc[:, 1] >= 56) & (data.iloc[:, 2] >= 56) & (data.iloc[:, 3] >= 56),
    (data.iloc[:, 4] >= 56) & (data.iloc[:, 5] >= 56),
    (data.iloc[:, 4] >= 56) & (data.iloc[:, 5] >= 56) & (data.iloc[:, 6] >= 56),
    (data.iloc[:, 4] >= 56) & (data.iloc[:, 5] >= 56) & (data.iloc[:, 7] >= 56),
    (data.iloc[:, 12] >= 56) & (data.iloc[:, 13] >= 56) & (data.iloc[:, 14] >= 56),
    (data.iloc[:, 15] >= 56) & (data.iloc[:, 16] >= 56) & (data.iloc[:, 17] >= 56),
    (data.iloc[:, 18] >= 56) & (data.iloc[:, 19] >= 56),
    (data.iloc[:, 20] >= 56) & (data.iloc[:, 21] >= 56),
    (data.iloc[:, 22] >= 56) & (data.iloc[:, 23] >= 56) & (data.iloc[:, 24] >= 56) & (data.iloc[:, 25] >= 56),
    (data.iloc[:, 7] >= 56) & (data.iloc[:, 8] >= 56) & (data.iloc[:, 9] >= 56) & (data.iloc[:, 10] >= 56) & (data.iloc[:, 11] >= 56)
]
values = [
    'DATA SCIENCE', 'DATA ANALYST', 'BUSINESS ANALYST', 'BACKEND DEVELOPER', 'EMBEDDED ENGINEER',
    'NETWORK ENGINEER', 'FRONTEND DEVELOPER', 'SOFTWARE TESTING', 'SOFTWARE ENGINEER', 'SOFTWARE DEVELOPER'
]

# Create a new column 'Career' based on conditions and values
data['Career'] = np.select(conditions, values, default='OTHER FIELD')

# Store the values of satisfied conditions as a string in a new column 'Satisfied_Conditions'
data['Satisfied_Conditions'] = data.apply(lambda x: ', '.join([value for condition, value in zip(conditions, values) if condition[x.name]]), axis=1)
data.loc[data['Satisfied_Conditions'] == '', 'Satisfied_Conditions'] = 'NON TECHNICAL'

# Create a pie chart using Plotly Express
fig = px.pie(data, names='Career', category_orders={'Career': values + ['OTHER FIELD']})



# Define the layout of the application
layout = html.Div(children=[
    html.H1('Career Distribution'),
    dcc.Graph(
        id='career-pie-chart',
        figure=fig
    ),
    html.H2('Selected Career Names and Conditions:'),
    html.Table(id='selected-names-table')
])

# Define callback function to update the table based on the selected pie values
@callback(
    Output('selected-names-table', 'children'),
    Input('career-pie-chart', 'clickData')
)
def update_table(clickData):
    if clickData is None:
        return []

    selected_career = clickData['points'][0]['label']
    filtered_data = data[data['Career'] == selected_career]
    selected_names = filtered_data['Name'].values
    selected_conditions = filtered_data['Satisfied_Conditions'].values

    rows = []
    for name, conditions in zip(selected_names, selected_conditions):
        row = html.Tr([html.Td(name), html.Td(conditions)])
        rows.append(row)

    table = html.Table([
        html.Thead(html.Tr([html.Th('Selected Names'), html.Th('Satisfied Conditions')])),
        html.Tbody(rows)
    ])

    return table
