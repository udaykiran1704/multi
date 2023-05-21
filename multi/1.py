import dash
from dash import  dcc
from dash import html
import pandas as pd
import plotly.graph_objs as go

# Read the dataset
df = pd.read_csv("student_performance.csv")

# Create the Dash app
app = dash.Dash(__name__)

# Calculate analysis metrics
failure_df = df[df["Result "] == "Fail"]
all_clear_df = df[df["Result "] == "Pass"]
distinction_df = df[df["Result "] == "Distinction"]

failure_count = len(failure_df)
all_clear_count = len(all_clear_df)
distinction_count = len(distinction_df)

# Define the layout
app.layout = html.Div(
    [
        html.H1("Student Performance Analysis", style={"textAlign": "center"}),
        
        # Failure Analysis
        html.Div(
            [
                html.H2("Failure Analysis"),
                html.Table(
                    [
                        html.Tr([html.Th("Total Students Failed"), html.Th("Percentage")]),
                        html.Tr([html.Td(failure_count), html.Td(f"{(failure_count / len(df)) * 100:.2f}%")]),
                    ],
                    style={"margin": "auto"},
                ),
                html.H3("Failed Students"),
                dcc.DataTable(
                    id="failure-table",
                    columns=[{"name": i, "id": i} for i in failure_df.columns],
                    data=failure_df.to_dict("records"),
                    style_cell={'textAlign': 'center'},
                    style_header={
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'fontWeight': 'bold'
                    },
                    style_data_conditional=[
                        {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'}
                    ],
                ),
            ],
            className="four columns",
        ),
        
        # All Clear Analysis
        html.Div(
            [
                html.H2("All Clear Analysis"),
                html.Table(
                    [
                        html.Tr([html.Th("Total Students All Clear"), html.Th("Percentage")]),
                        html.Tr([html.Td(all_clear_count), html.Td(f"{(all_clear_count / len(df)) * 100:.2f}%")]),
                    ],
                    style={"margin": "auto"},
                ),
                html.H3("All Clear Students"),
                dcc.DataTable(
                    id="all-clear-table",
                    columns=[{"name": i, "id": i} for i in all_clear_df.columns],
                    data=all_clear_df.to_dict("records"),
                    style_cell={'textAlign': 'center'},
                    style_header={
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'fontWeight': 'bold'
                    },
                    style_data_conditional=[
                        {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'}
                    ],
                ),
            ],
            className="four columns",
        ),
        
        # Distinction Analysis
        html.Div(
            [
                html.H2("Distinction Analysis"),
                html.Table(
                    [
                        html.Tr([html.Th("Total Students with Distinction"), html.Th("Percentage")]),
                        html.Tr([html.Td(distinction_count), html.Td(f"{(distinction_count / len(df)) * 100:.2f}%")]),
                    ],
                    style={"margin": "auto"},
                ),
                html.H3("Students with Distinction"),
                dcc.DataTable(
                    id="distinction-table",
                    columns=[{"name": i, "id": i} for i in distinction_df.columns],
                    data=distinction_df.to_dict("records"),
                    style_cell={'textAlign': 'center'},
                    style_header={
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'fontWeight': 'bold'
                    },
                    style_data_conditional=[
                        {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'}
                    ],
                ),
            ],
            className="four columns",
        ),
    ],
    className="row",
)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
