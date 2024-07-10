import pandas as pd

import dash
from dash import dcc, callback, Input, Output, dash_table
import dash_bootstrap_components as dbc

import plotly.express as px

dash.register_page(__name__,
                   path="/",
                   name="Overview",
                   title="Unicorn Companies Overview"
                   )

df = pd.read_csv("unicorns.csv")
df['Valuation ($B)'] = df['Valuation ($B)'].replace('[\$,]', '', regex=True).astype(float)

# Layout definition
layout = dbc.Container([
    dbc.Row(
        [
            dbc.Col(
                dcc.Graph(id='valuation-by-country'),
                width=6
            ),
            dbc.Col(
                dcc.Graph(id='valuation-by-industry'),
                width=6
            )
        ]
    ),
    dbc.Row(
        [
            dbc.Col(
                dcc.Graph(id='valuation-distribution'),
                width=6
            ),
            dbc.Col(
                dcc.Graph(id='valuation-over-time'),
                width=6
            )
        ]
    ),
    dbc.Row(
        dbc.Col(
            dash_table.DataTable(
                id='data-table',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'),
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left'}
            ),
            width=12
        )
    )
])

# Define callback to update plots for page 1
@callback(
    Output('valuation-by-country', 'figure'),
    Output('valuation-by-industry', 'figure'),
    Output('valuation-distribution', 'figure'),
    Output('valuation-over-time', 'figure'),
    [Input('valuation-by-country', 'id'),
     Input('valuation-by-industry', 'id'),
     Input('valuation-distribution', 'id'),
     Input('valuation-over-time', 'id')]
)

def update_graphs(dummy_input_country, dummy_input_industry, dummy_input_dist, dummy_input_time):
    # Valuation by Country
    valuation_by_country = df.groupby('Country')['Valuation ($B)'].sum().reset_index()
    country_bar = px.bar(valuation_by_country, x='Country', y='Valuation ($B)', title='Total Valuation by Country')

    # Valuation by Industry
    valuation_by_industry = df.groupby('Industry')['Valuation ($B)'].sum().reset_index()
    industry_bar = px.bar(valuation_by_industry, x='Industry', y='Valuation ($B)',
                      title='Valuation Distribution by Industry')

    # Valuation Distribution
    valuation_violin = px.violin(df, y='Valuation ($B)', box=True, title='Valuation Distribution of Unicorns')

    # Valuation Over Time
    df['Date Joined'] = pd.to_datetime(df['Date Joined'])
    valuation_over_time = df.sort_values('Date Joined').groupby('Date Joined')['Valuation ($B)'].sum().cumsum().reset_index()
    time_line = px.line(valuation_over_time, x='Date Joined', y='Valuation ($B)', title='Total Valuation Over Time')

    # Update layout for better readability
    time_line.update_yaxes(tickprefix="$", tickformat=",.2f")
    time_line.update_xaxes(tickangle=45)
    time_line.update_layout(
        title='Total Valuation Over Time',
        xaxis_title='Date Joined',
        yaxis_title='Total Valuation ($B)',
        margin=dict(l=20, r=20, t=50, b=50),
        paper_bgcolor='rgba(255,255,255,0.8)',
        plot_bgcolor='rgba(255,255,255,0.8)',
        font=dict(color='black'),
    )

    return country_bar, industry_bar, valuation_violin, time_line


if __name__ == '__main__':
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.layout = layout
    app.run_server(debug=True)