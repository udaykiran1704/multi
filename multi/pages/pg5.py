import dash
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
from dash import dcc
from dash import html
from dash import dcc, html
from dash.dependencies import Input, Output
import numpy as np

# To create meta tag for each page, define the title, image, and description.

dash.register_page(__name__,
                   path='/Placement',  # '/' is home page and it represents the url
                   name='Placement',  # name of page, commonly used as name of link
)


# Load data
data = pd.read_csv('student_performance.csv')

# Assign 1 for placed and 0 for unplaced in the Placement column
data['Placement'] = data['Placement'].apply(lambda x: 1 if x == 'placed' else 0)

# Categorize placement as placed or unplaced based on the new Placement column
data['Placement Status'] = data['Placement'].apply(lambda x: 'placed' if x == 1 else 'unplaced')

fig = px.histogram(data, x="Gender", color='Placement Status', 
                   category_orders={'Placement Status':['placed', 'unplaced']},
                   barmode='group', height=400)


# Define the layout
layout = html.Div(children=[
    html.H1(children='Student Performance'),

    html.Div(children='''
        Placement by Gender
    '''),

    dcc.Graph(
        id='placement-graph',
        figure=fig 
    )    
])

