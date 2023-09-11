import pandas as pd
import numpy as np
from dash import Dash, html, dcc, callback, Output, Input, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px


intel = pd.read_csv("intel_new_table.csv", sep=",")

external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = dbc.Container([

    dbc.Row([html.H1(children=" Ma premiére application fonctionnel de dash")]),


    dbc.Row([
        dbc.Col([
            html.Label('Génération : '),
            dcc.Dropdown(
                options=[
                    {'label': gen, 'value': gen}
                    for gen in intel["nGeneration"].unique()
                ],
                id="drop_down_gen"
            ),
        ], width=4),

        dbc.Col([
            html.Label('Brand : '),
            dcc.Dropdown(
                options=intel["brand"].unique(),
                id="drop_down_brand"
            ),
        ], width=3),

        dbc.Col([
            html.Label('Number of cores : '),
            dcc.Slider(
                min=4,
                max=18,
                step=2,
                value=8,
                id="slider_nbrs_cores"
            )],
            width=3),

    ]),
    html.Hr(),



    dbc.Row([
        dbc.Col([dash_table.DataTable(data=intel.to_dict('records'), page_size=12,
                                      id="table",
                                      style_table={'overflowX': 'auto'},
                                      style_cell={
            # all three widths are needed
            'minWidth': '100px', 'width': '100%', 'maxWidth': '600px',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
        })], width=8),
    ]),

], fluid=True)


@callback(
    Output(component_id='table', component_property='data'),
    [Input(component_id='drop_down_gen', component_property='value'),
    Input(component_id='drop_down_brand',component_property='value'),
    Input(component_id='slider_nbrs_cores', component_property='value'),
    ]
)
def update_table(gen, brand, cores):
    df_filtered = intel  # Commencez avec le DataFrame complet

    if gen is not None:
        df_filtered = df_filtered[df_filtered["nGeneration"] == gen]

    if brand is not None:
        df_filtered = df_filtered[df_filtered["brand"] == brand]

    if cores is not None:
        df_filtered = df_filtered[df_filtered["nbr_cores"] == cores]


    return df_filtered.to_dict('records')



if __name__ == "__main__":
    app.run(debug=True)
