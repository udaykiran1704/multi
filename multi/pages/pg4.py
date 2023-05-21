
import dash
import plotly.express as px
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output


# To create meta tag for each page, define the title, image, and description.

dash.register_page(__name__,
                   path='/Attendance',  # '/' is home page and it represents the url
                   name='Attendance',  # name of page, commonly used as name of link
)

# Load data
data = pd.read_csv('student_performance.csv')

# Assign 1 for Present and 0 for Absent in the Attendance column
data['Attendance'] = data['Attendence'].apply(lambda x: 1 if x == 'Present' else 0)

# Categorize attendance as Present or Absent based on the new Attendance column
data['Attendance Status'] = data['Attendance'].apply(lambda x: 'Present' if x == 1 else 'Absent')

fig = px.histogram(data, x="Gender", color='Attendance Status',
                   category_orders={'Attendance Status': ['Present', 'Absent']},
                   barmode='group', height=400)

# Define the layout
layout = html.Div(children=[
    html.H1(children='Student Performance'),

    html.Div(children='''
        Attendance by Gender
    '''),

    dcc.Graph(
        id='attendance-graph',
        figure=fig
    ),


])

