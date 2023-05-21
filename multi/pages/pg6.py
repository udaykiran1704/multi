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



# To create meta tag for each page, define the title, image, and description.
dash.register_page(__name__,
                   path='/Comparison',  # '/' is home page and it represents the url
                   name='Comparision Analysis',  # name of page, commonly used as name of link
                   title='Index',  # title that appears on browser's tab
                   
)

# page 1 data
# Read the CSV file
df = pd.read_csv('student_performance.csv')


# Define the app layout
layout = html.Div(
    [
        dcc.Dropdown(
            id='student-dropdown',
            options=[{'label': student, 'value': student} for student in df['Nameofthestudent']],
            value=[],
            multi=True
        ),
        html.Div(id='graphs-container', className='container')
    ],
    style={'width': '100%', 'max-width': '1200px', 'margin': '0 auto'}
)

# Define the update function for bar graph
@callback(dash.dependencies.Output('graphs-container', 'children'),
              [dash.dependencies.Input('student-dropdown', 'value')])
def update_bar_graph(selected_students):
    if len(selected_students) < 2:
        # If less than two students are selected, show an empty figure
        return []

    data = []
    colors = ['rgba(31, 119, 180, 0.8)', 'rgba(255, 127, 14, 0.8)', 'rgba(44, 160, 44, 0.8)', 'rgba(214, 39, 40, 0.8)']

    for i, subject in enumerate(['HPC', 'DL', 'SDN', 'BI']):
        subject_data = []

        for student in selected_students:
            student_data = df[df['Nameofthestudent'] == student]
            subject_data.append(student_data[subject].values[0])

        data.append(go.Bar(
            x=selected_students,
            y=subject_data,
            name=subject,
            marker=dict(color=colors[i])
        ))

    layout = go.Layout(title='Scores of Students in All Subjects', xaxis={'title': 'Students'},
                       yaxis={'title': 'Scores'}, barmode='group')

    graph = dcc.Graph(
        id='live-bar-graph',
        figure={'data': data, 'layout': layout}
    )

    return [graph]


