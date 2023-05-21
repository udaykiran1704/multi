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
                   path='/',  # '/' is home page and it represents the url
                   name='Overall',  # name of page, commonly used as name of link
                   title='Index',  # title that appears on browser's tab
                   
)

# page 1 data
df = pd.read_csv('student_performance.csv')

# Initialize the Flask app
server = Flask(__name__)

# Initialize the Dash app
app = dash.Dash(__name__, server=server)


# Define the app layout
layout = html.Div([
    dcc.Dropdown(
        id='student-dropdown',
        options=[{'label': student, 'value': student} for student in df['Nameofthestudent']],
        value=df['Nameofthestudent'].iloc[0]
    ),
    dcc.Graph(id='live-bar-graph', animate=True),
    dcc.Graph(id='passed-bar-graph', animate=True),
    dcc.Graph(id='failed-bar-graph', animate=True),
    dcc.Graph(id='passing-percentages-graph', animate=True),
    dcc.Interval(id='interval-component', interval=2000, n_intervals=0)
])


# Define the update function for bar graph
@callback(dash.dependencies.Output('live-bar-graph', 'figure'),
              [dash.dependencies.Input('interval-component', 'n_intervals'),
               dash.dependencies.Input('student-dropdown', 'value')])
def update_bar_graph(n, selected_student):
    student_data = df[df['Nameofthestudent'] == selected_student]
    colors = ['rgba(31, 119, 180, 0.8)', 'rgba(255, 127, 14, 0.8)', 'rgba(44, 160, 44, 0.8)', 'rgba(214, 39, 40, 0.8)']
    data = []
    for i, subject in enumerate(['HPC', 'DL', 'SDN', 'BI']):
        data.append(go.Bar(
            x=[subject],
            y=[student_data[subject].values[0]],
            name=subject,
            marker=dict(color=colors[i])
        ))
    layout = go.Layout(title=f'Scores of  in All Subjects', xaxis={'title': 'Subjects'}, yaxis={'title': 'Scores'})
    return {'data': data, 'layout': layout}


# Define the update function for passed students bar graph
@callback(dash.dependencies.Output('passed-bar-graph', 'figure'),
              [dash.dependencies.Input('interval-component', 'n_intervals')])
def update_passed_bar_graph(n):
    passed_students = df[(df['HPC'] >= 12) & (df['DL'] >= 12) & (df['SDN'] >= 12) & (df['BI'] >= 12)]
    data = [go.Bar(
        x=passed_students['Nameofthestudent'],
        y=passed_students[df.columns[2:6]].sum(axis=1),
        name='Total marks'
    )]
    layout = go.Layout(title='All Clear')
    return {'data': data, 'layout': layout}


# Define the update function for failed students bar graph
@callback(dash.dependencies.Output('failed-bar-graph', 'figure'),
              [dash.dependencies.Input('interval-component', 'n_intervals')])
def update_failed_bar_graph(n):
    failed_students = df[(df['HPC'] < 12) | (df['DL'] < 12) | (df['SDN'] < 12) | (df['BI'] < 12)]
    total_failed_subjects = (failed_students[df.columns[2:6]] < 12).sum(axis=1)
    failed_subject_count = {
        0: 'All Clear',
        1: '1 Subject',
        2: '2 Subjects',
        3: '3 Subjects',
        4: '4 Subjects',
        5: '5 Subjects'
    }
    failed_subject_count_labels = [failed_subject_count[count] for count in total_failed_subjects]
    data = [go.Bar(
        x=failed_students['Nameofthestudent'],
        y=total_failed_subjects,
        text=failed_subject_count_labels,
        name='Number of Failed Subjects',
        textposition='auto'
    )]
    layout = go.Layout(title='Failed Students')
    return {'data': data, 'layout': layout}


# Define the update function for passing percentages graph
@callback(dash.dependencies.Output('passing-percentages-graph', 'figure'),
              [dash.dependencies.Input('interval-component', 'n_intervals')])
def update_passing_percentages_graph(n):
    pass_counts = []
    for column in df.columns[2:6]:
        pass_counts.append(df[df[column] >= 12][column].count())

    data = [go.Bar(
        x=df.columns[2:6],
        y=[count / len(df) * 100 for count in pass_counts],
        name='Passing Percentage'
    )]
    layout = go.Layout(title='Passing Percentages in All Subjects', xaxis={'title': 'Subjects'}, yaxis={'title': 'Passing Percentage (%)'})
    return {'data': data, 'layout': layout}


