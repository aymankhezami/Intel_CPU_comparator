import pandas as pd
import numpy as np
from dash import Dash, html, dcc, callback, Output, Input, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go


intel = pd.read_csv("intel_new_table.csv", sep=",")
df = intel.copy()

# Palette de couleurs
colors = ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99',
          '#e31a1c', '#fdbf6f', '#ff7f00', '#cab2d6', '#6a3d9a']



fig1 = px.histogram(
    df,
    x="brand",
    color="series",
    title="Distribution of Brands by Processor Generation",
    color_discrete_sequence=colors,
    height=600
)


fig1.update_xaxes(title="Brand")
fig1.update_yaxes(title="Frequency")

fig2 = px.histogram(
    df,
    x="nGeneration2",
    color="brand",
    title="Distribution of Brands by Processor Generation",
    color_discrete_sequence=colors,
    height=600
)
fig2.update_xaxes(title="Generation")
fig2.update_yaxes(title="Frequency")
fig2.update_traces(marker=dict(line=dict(color='white', width=3)))

fig3 = px.scatter(
    df,
    x="nGeneration2",
    y="nbr_cores",
    color="series",
    color_discrete_sequence=colors,
    title="Number of cores per generation for each series"
)

fig3.update_xaxes(title="Generation")
fig3.update_yaxes(title="Number of cores")


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
        ], width=2),

        dbc.Col([
            html.Label('Brand : '),
            dcc.Dropdown(
                options= intel["brand"].unique(),
                id="drop_down_brand"
            ),
        ], width=2),

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
        dbc.Col([dash_table.DataTable(data=intel.to_dict('records'), page_size=10,
                                      id='table',
                                      style_table={'overflowX': 'auto'},
                                      style_cell={
            # all three widths are needed
            'minWidth': '50px', 'width': '100%', 'maxWidth': '600px',
            'height':'30px',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
        })], width=12),
    ],style={'height':'100%','minHeight':'200px'}),
    html.Hr(),
    dbc.Row([
        dbc.Col([dcc.Graph(id='histogram_B', figure=fig1)], width=4),
        dbc.Col([dcc.Graph(id='histogram_G', figure=fig2)], width=4),
        dbc.Col([dcc.Graph(id='scatter_A', figure=fig3)], width=4),

    ]),



], fluid=True)


@callback(
    Output(component_id='table', component_property='data'),
    [Input(component_id='drop_down_gen', component_property='value'),
     Input(component_id='drop_down_brand', component_property='value'),
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
