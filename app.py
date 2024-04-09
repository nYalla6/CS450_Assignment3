import dash
from dash import dcc
from dash import html
from dash import Input, Output
import pandas as pd
import plotly.express as px


app = dash.Dash(__name__)
tweets_df = pd.read_csv('ProcessedTweets.csv')

# Define the layout of the app
app.layout = html.Div([
    html.Div(id="row1", children=[
        html.P("Month:"),
        dcc.Dropdown(id='month-dropdown',
                    options=[{'label': month, 'value': month} for month in sorted(tweets_df['Month'].unique())],
                    placeholder="Select a month"),
        html.P("Sentiment Score:"),
        dcc.RangeSlider(id='sentiment-slider',
                        min=tweets_df['Sentiment'].min(),
                        max=tweets_df['Sentiment'].max(),
                        value=[tweets_df['Sentiment'].min(), tweets_df['Sentiment'].max()],
                        marks={-1: '-1', 0: '0', 1: '1'}),
        html.P("Subjectivity Score:"),
        dcc.RangeSlider(id='subjectivity-slider',
                        min=tweets_df['Subjectivity'].min(),
                        max=tweets_df['Subjectivity'].max(),
                        value=[tweets_df['Subjectivity'].min(), tweets_df['Subjectivity'].max()],
                        marks={0: '0', 0.5: '0.5', 1: '1'}),
    ]),
    
    dcc.Graph(id='scatter-plot'),
    #html table, defined when data is selected
    html.Table(id='tweet-table', style={'margin': 'auto', 'textAlign': 'center'})
])

### Step 2: Define Callbacks to Update Components

# Callback to update scatter plot based on filters
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('month-dropdown', 'value'),
     Input('sentiment-slider', 'value'),
     Input('subjectivity-slider', 'value')])
def update_scatter_plot(selected_month, sentiment_range, subjectivity_range):
    filtered_df = tweets_df
    
    if selected_month:
        filtered_df = filtered_df[filtered_df['Month'] == selected_month]
        
    filtered_df = filtered_df[
        (filtered_df['Sentiment'] >= sentiment_range[0]) & (filtered_df['Sentiment'] <= sentiment_range[1]) &
        (filtered_df['Subjectivity'] >= subjectivity_range[0]) & (filtered_df['Subjectivity'] <= subjectivity_range[1])
    ]
    
    scatter_fig = px.scatter(filtered_df, x='Dimension 1', y='Dimension 2', color_discrete_sequence = ['gray'])
    scatter_fig.update_layout(
        xaxis=dict(title=None),  # Remove x axis label
        yaxis=dict(title=None)   # Remove y axis label
    )
    return scatter_fig

# Callback to update tweet display table based on selected points
@app.callback(
    Output('tweet-table', 'children'),
    [Input('scatter-plot', 'selectedData')])
def display_selected_tweets(selected_data):
    if selected_data is not None:
        # Extract indices of selected points
        selected_indices = [point['pointIndex'] for point in selected_data['points']]
        
        # Filter tweets based on selected indices
        selected_tweets = tweets_df.iloc[selected_indices]['RawTweet']
        
        # Create HTML table rows for selected tweets
        table_rows = [
            html.Tr(
                html.Td(tweet, style={
                    'textAlign': 'center',
                    'border': '1px solid #dddddd',  # Define border style for cells
                    'padding': '8px'
                })
            )
            for tweet in selected_tweets
        ]
        
        # Define table header row with centered column headers
        header_row = html.Tr([
            html.Th('RawTweet', style={
                'textAlign': 'center',
                'backgroundColor': '#f2f2f2',
                'padding': '8px',
                'border': '1px solid #dddddd'
            })
        ])
        
        return [header_row] + table_rows
    else:
        return []
### Step 3: Run the Dash Application

if __name__ == '__main__':
    app.run_server(debug=True)
