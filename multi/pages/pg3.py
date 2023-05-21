import dash
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
from dash import dcc
from dash import html
from dash import dcc, html, callback
from dash.dependencies import Input, Output
from dash import dash_table

dash.register_page(__name__,
                   path='/Distinction',
                   name='Distinction Analysis',
                   title='New heatmaps',
                   description='Learn all about the heatmap.'
)

# Load data
data = pd.read_csv('student_performance.csv')

# Create a new column to indicate CGPA
data['CGPA'] = data['Percentage'] / 9.5

# Define function to categorize students based on CGPA
def categorize_students(cgpa):
    if cgpa > 7.75:
        return 'First Class with Distinction'
    elif cgpa > 6.75:
        return 'First Class'
    elif cgpa > 6.25:
        return 'Higher Second Class'
    elif cgpa > 5.5:
        return 'Second Class'
    elif cgpa > 0:
        return 'All Clear'
    else:
        return 'Fail'

# Apply the categorization function to the 'CGPA' column
data['Result'] = data['CGPA'].apply(categorize_students)

# Group data by the 'Result' column and count the number of students in each category
result_counts = data.groupby('Result').size()

# Create a bar graph with the result counts
fig = go.Figure(data=[go.Bar(x=result_counts.index, y=result_counts.values, 
                             marker_color=['#00bfff', '#0066ff', '#1a75ff', '#4d94ff', '#b3d9ff', '#ff6666'])])

# Set the layout of the graph
fig.update_layout(title='Distribution of Student Results',
                  xaxis_title='Result Category',
                  yaxis_title='Number of Students')


# Get the top 5 students by CGPA
topper_list = data.sort_values(by='CGPA', ascending=False).head(5)[["Nameofthestudent", "CGPA", "Result"]]

# Create the layout for the app
layout = html.Div(children=[
    html.H1(children='Distribution of Student Results'),
    dcc.Graph(
        id='result-bar-graph',
        figure=fig
    ),
    html.H3(children='Click a bar to see the data for that category:'),
    dash_table.DataTable(
        id='data-table',
        columns=[{"name": "Nameofthestudent", "id": "Nameofthestudent"},
                 {"name": "Percentage", "id": "Percentage"},
                 {"name": "CGPA", "id": "CGPA"},
                 {"name": "Result", "id": "Result"}],
        data=[],
        style_cell={'textAlign': 'center'},
        style_data_conditional=[{
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'
        }],
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        }
    ),
    # Display the top 5 students by CGPA in a DataTable
     html.H3(children='Top Five Students by CGPA:'),
     dash_table.DataTable(
         id='top-five-table',
        columns=[{"name": "Nameofthestudent", "id": "Nameofthestudent"},
             {"name": "CGPA", "id": "CGPA"},
             {"name": "Result", "id": "Result"}],
             data=topper_list.to_dict('records'),
            style_cell={'textAlign': 'center'},
            style_data_conditional=[{
               'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
             }],
            style_header={
             'backgroundColor': 'rgb(230, 230, 230)',
             'fontWeight': 'bold'
    }
)

])

# Define callback to update data table when a bar is clicked
@callback(
    Output('data-table', 'data'),
    Input('result-bar-graph', 'clickData'))
def update_data_table(clickData):
    if clickData is not None:
        selected_result = clickData['points'][0]['x']
        filtered_data = data.loc[data['Result'] == selected_result]
        return filtered_data[["Nameofthestudent", "Percentage", "CGPA", "Result"]].to_dict('records')
    else:
        return []

