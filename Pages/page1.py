import pandas as pd

import dash
from dash import dcc, callback
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc

import plotly.express as px

dash.register_page(__name__,
                   path="/MoreInfo",
                   name="Industry Valuations",
                   title="Unicorn Valuations"
                   )

# Load data
df = pd.read_csv("unicorns.csv")

layout = dbc.Container([
    dbc.Row(
        dbc.Col(
            dcc.Dropdown(
                id='industry-dropdown',
                options=[{'label': industry, 'value': industry} for industry in df['Industry'].unique()],
                value=df['Industry'].unique()[0],
                clearable=False,
                style={'width': '50%'}
            ),
            width=12
        )
    ),
    dbc.Row(
        dbc.Col(
            dcc.Graph(id='valuation-histogram'),
            width=12
        )
    )
])

# Define callback to update plots for page 2
@callback(
    Output('valuation-histogram', 'figure'),
    [Input('industry-dropdown', 'value')]
)

def update_histogram(selected_industry):
    filtered_df = df[df['Industry'] == selected_industry]

    # Create histogram for company valuations by selected industry using Plotly Express
    valuation_histogram = px.histogram(filtered_df, x='Valuation ($B)', nbins=10,
                                       title=f'Histogram of Valuations for {selected_industry}')

    # Update layout to add labels and adjust title
    valuation_histogram.update_xaxes(title='Valuation ($B)')
    valuation_histogram.update_yaxes(title='Frequency')
    valuation_histogram.update_layout(title=f'Histogram of Valuations for {selected_industry}',
                                      margin=dict(l=20, r=20, t=50, b=50),  # Adjust margins
                                      paper_bgcolor='rgba(255,255,255,0.8)',  
                                      plot_bgcolor='rgba(255,255,255,0.8)',  
                                      font=dict(color='black'),  
                                      height=600,  
                                      width=1000,  
                                      )

    # Rotate x-axis labels for better visibility
    valuation_histogram.update_xaxes(tickangle=45)

    # Update legend position and orientation
    valuation_histogram.update_layout(legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1))

    return valuation_histogram
