import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, dash_table, no_update
import pandas as pd
import io
import base64


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

dash.register_page(__name__,
                   path='/Failure',  # represents the url text
                   name='Failure Analysis',  # name of page, commonly used as name of link
                   title='Analysis'  # epresents the title of browser's tab
)

# page 2 data


layout = html.Div(
    [
        html.Div(
            [
                html.H3("Student Scores", style={"textAlign":"center"}),
                dcc.Upload(
                    id='upload-data',
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select Files')
                    ]),
                    style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px'
                    },
                    # Allow multiple files to be uploaded
                    multiple=False
                ),
                dash_table.DataTable(
                    id="table",
                    page_size=5,
                    sort_action="native",
                ),
            ],
            style={"margin": 50},
            className="five columns"
        ),
        html.Div(id="output-graph", className="six columns"),
    ],
    className="row"
)

@callback(
    Output('table', 'data'),
    Input('upload-data', 'contents'),
    Input('upload-data', 'filename')
)
def update_table(contents, filename):
    if contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        try:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        except Exception as e:
            print(e)
            return []

        # Add an ID column to the DataFrame
        df["id"] = df.index

        # Define the columns to display in the table
        columns = df.columns.tolist()

        return df.to_dict("records")

    else:
        return []

# Define the callback function for updating the graph
@callback(
    Output("output-graph", "children"), 
    Input("table", "data"), 
    Input("table", "active_cell")
)
def cell_clicked(data, active_cell):
    if active_cell is None:
        return no_update

    row = active_cell["row_id"]
    roll_no = data[row]["PRN"]
    col = active_cell["column_id"]
    y = col if col in ["HPC", "DL", "SDN", "BI"] else None

    fig = px.bar(data_frame=data, x="Nameofthestudent", y=y, color=col,
                 text=col, labels={"Nameofthestudent": "Student Name", y: col},
                 title=f"{col} scores of Roll No. {roll_no}")

    fig.update_traces(texttemplate='%{text:.2s}', textposition='auto')

    return dcc.Graph(figure=fig)

# Load data
data = pd.read_csv('student_performance.csv')

# Create a new column to indicate number of subjects failed
data['Subjects Failed'] = data[['HPC', 'DL', 'SDN', 'BI']].apply(lambda row: sum(row < 12), axis=1)

# Define function to categorize students based on number of subjects failed
def categorize_students(num_subjects_failed):
    if num_subjects_failed == 1:
        return 'Fail in one subject'
    elif num_subjects_failed == 2:
        return 'Fail in two subjects'
    elif num_subjects_failed == 3:
        return 'Fail in three subjects'
    elif num_subjects_failed == 4:
        return 'Fail in four subjects'
    else:
        return 'All clear'

# Apply the categorization function to the 'Subjects Failed' column
data['Result'] = data['Subjects Failed'].apply(categorize_students)

# Group the data by the 'Result' column and count the number of students in each group
result_counts = data.groupby('Result').size().reset_index(name='Counts')

# Create a bar graph visualization using Plotly Express
fig = px.bar(result_counts, x='Result', y='Counts')

# Define a function to filter the data based on the selected category
def filter_data(selected_category):
    filtered_data = data[data['Result'] == selected_category]
    return filtered_data[['Nameofthestudent', 'HPC', 'DL', 'SDN', 'BI']]


# Define the layout of the application
layout = html.Div(children=[
    html.H1(children='Student Performance'),

    html.Div(children='''
        Bar graph of student performance based on number of subjects failed.
    '''),

    dcc.Graph(
        id='student-performance-graph',
        figure=fig,
        clickData={'points': [{'x': 'All clear'}]}  # Set default value to prevent error on page load
    ),

    html.Hr(),

    html.Div(id='selected-category-data')
])

# Define a callback function to update the DataTable based on the selected category
@callback(
    dash.dependencies.Output('selected-category-data', 'children'),
    [dash.dependencies.Input('student-performance-graph', 'clickData')])
def update_table(clickData):
    if clickData is not None:
        selected_category = clickData['points'][0]['x']
        filtered_data = filter_data(selected_category)
        table = html.Table([
            html.Thead(html.Tr([html.Th(col) for col in filtered_data.columns])),
            html.Tbody([
                html.Tr([html.Td(filtered_data.iloc[i][col]) for col in filtered_data.columns]) 
                for i in range(len(filtered_data))
            ])
        ])
        return table
    else:
        return html.Div()

