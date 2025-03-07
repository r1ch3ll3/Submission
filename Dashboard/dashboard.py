import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import dash
from dash import dcc, html
import plotly.express as px
from dash.dependencies import Input, Output

sns.set(style='dark')

# Load dataset
day_df = pd.read_csv("day.csv")
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Initialize Dash app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Dashboard Penyewaan Sepeda"),
    
    dcc.Dropdown(
        id='weather_filter',
        options=[{'label': str(w), 'value': w} for w in sorted(day_df['weathersit'].unique())],
        value=1,
        clearable=False,
        style={'width': '50%'}
    ),
    
    dcc.Graph(id='rental_trend'),
])

# Callback for updating graph
@app.callback(
    Output('rental_trend', 'figure'),
    [Input('weather_filter', 'value')]
)
def update_graph(weather):
    filtered_df = day_df[day_df['weathersit'] == weather]
    fig = px.line(filtered_df, x='dteday', y='cnt', title='Tren Penyewaan Sepeda', labels={'cnt': 'Total Penyewa'})
    return fig

# Run server
if __name__ == '__main__':
    app.run_server(debug=True)