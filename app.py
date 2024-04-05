import dash
from dash import dcc, html, Input,Output,State
import seaborn as sns
import plotly.express as px
from dash.exceptions import PreventUpdate
import io
import base64
import pandas as pd



# Load the my_df dataset from the csv in the folder
# Try reading the CSV file with different encodings
my_df = pd.read_csv('ProcessedTweets.csv', encoding='latin1')


model_pipeline=None

month_list = ["April", "May", "June"]
month_dropdown = html.Div(className="dropdown_div",children=[html.P("Select Month: "),dcc.Dropdown(id='mth_dropdown',options=month_list, value=None,style=dict(width=150,marginLeft=2))])
# radio_items=dcc.RadioItems(id='cat_radio_items_id',options=categorical_columns, value=None,inline=True)

sentiment_slider = html.Div(className="slider_sentiment", children=[dcc.RangeSlider(
        id='my-range-slider',
        min=-1,
        max=1,
        step=0.1,
        marks={i: str(i) for i in range(-1, 2)},
        value=[-1, 1]  # Initial values for the range slider
    ),
    html.Div(id='slider-output')])

app = dash.Dash(__name__)
server = app.server



#### layout
app.layout = html.Div(className="parent_container", children=[
    #row one holds the inputs
    html.Div(id="row1", children=[
        month_dropdown,
        sentiment_slider,

    ]),

    #row 2 holds the two graphs and their interactive components
    html.Div(id="row2", children=[
        #graph 1: scatter of hdi index vs life expectancy
        html.Div(className="row2_child1", children=[
            # continent_dropdown,
            html.Div(dcc.Graph(id='graph1'),style=dict(width="100%"))
        ]),
        #graph 2: histogram of GNI
        html.Div(className="row2_child2", children=[
            html.Div(dcc.Graph(id='graph2'),style=dict(width="100%"))
        ])
    ]),
])




### Define callback function for graph 1, the hdi versus life expectancy
@app.callback(Output('graph1', 'figure'), Input('ctry_dropdown', 'value'))
def update_graph1(target_variable):
    title = ""
    if target_variable is None:
        # If no continent selected, show all continents, HDI vs life expectancy
        fig = px.scatter(x=my_df['Human Development Index (HDI)'], y=my_df['Life expectancy at birth'])
        fig.update_xaxes(title_text='Human Development Index (HDI)')
        fig.update_yaxes(title_text='Life expectancy at birth')

        title = "All Countries: HDI Index vs. Life Expectancy"
    else:
        
        # Filter the DataFrame to include only the countries from the selected continent
        # filtered_df = my_df[my_df['Country'].isin(countries_displayed)]
        # Plot HDI vs life expectancy for the selected continent
        fig = px.scatter(x=my_df['Sentiment'], y=my_df['RawTweet'])
        fig.update_xaxes(title_text='Human Development Index (HDI)')
        fig.update_yaxes(title_text='Life expectancy at birth')
        title = f"{target_variable}: HDI Index vs. Life Expectancy"
        
    #customizing the title/graph
    custom_fig_title = dict(text=title, x=0.5,font=dict(family='Arial',size=20,color='Black')) #fig.update_layout(title=customize.custom_fig_title)
    fig.layout = dict(title=custom_fig_title,
                    margin=dict(l=20,r=40,t=50,b=50,pad=0),
                    plot_bgcolor="white", #Sets the background color of the plotting area in-between x and y axes.
                    paper_bgcolor='rgba(192, 242, 204, 0.8)', #Sets the background color of the paper where the graph is drawn.
                    modebar=dict(orientation='v', activecolor='gray',bgcolor="white", color="#ededed"),
                    hovermode=False, # one of ( "x" | "y" | "closest" | False | "x unified" | "y unified" )
                    )

    return fig

# # callback and update for graph two, the histogram with the bucket slider
# @app.callback(Output('graph2', 'figure'), Input('bucket_slider', 'value'))
# def update_graph2(num_buckets):
#     title = "GNI by Groups"
#     if num_buckets is None:
#         filtered_df = my_df.sort_values(by='Gross national income (GNI) per capita')

        
#         fig = px.histogram(filtered_df, x='Gross national income (GNI) per capita', nbins=8)
#         fig.update_layout(xaxis_title='Gross National Income (GNI) per Capita', yaxis_title='Number of countries')
#     else:
#         #sort the gni
#         # filtered_df = my_df.sort_values(by='Gross national income (GNI) per capita')
#         filtered_df = my_df.sort_values(by='Gross national income (GNI) per capita')

        
#         fig = px.histogram(filtered_df, x='Gross national income (GNI) per capita', nbins=num_buckets)
#         fig.update_layout(xaxis_title='Gross National Income (GNI) per Capita', yaxis_title='Number of countries')
    
#     custom_fig_title = dict(text=title, x=0.5,font=dict(family='Arial',size=20,color='Black')) #fig.update_layout(title=customize.custom_fig_title)
#     fig.layout = dict(title=custom_fig_title,
#                     margin=dict(l=20,r=40,t=50,b=50,pad=0),
#                     plot_bgcolor="white", #Sets the background color of the plotting area in-between x and y axes.
#                     paper_bgcolor='rgba(192, 242, 204, 0.8)', #Sets the background color of the paper where the graph is drawn.
#                     modebar=dict(orientation='v', activecolor='gray',bgcolor="white", color="#ededed"),
#                     hovermode=False, # one of ( "x" | "y" | "closest" | False | "x unified" | "y unified" )
#                     )    
#     return fig

# #update graph3 with the filters 
# @app.callback(Output('graph3', 'figure'), Input('radio_itm', 'value'))
# def update_graph3(filter_num):
#     if filter_num == None or filter_num == "All":
#          fig = px.scatter(my_df, 
#                      x='Expected years of schooling', 
#                      y='Life expectancy at birth',
#                      size='Gross national income (GNI) per capita',
#                      hover_data=['Country'],
#                      title=f'Expected Years of Schooling vs. Life Expectancy for Countries with Expected Years of Schooling {filter_num} or Less',
#                      labels={'Expected years of schooling': 'Expected Years of Schooling', 
#                              'Life expectancy at birth': 'Life Expectancy at Birth'}
#                  )
#     else:
#         sorted_df = my_df.sort_values(by='Gross national income (GNI) per capita', ascending=False)
#         fig = px.scatter(sorted_df.head(filter_num), 
#                     x='Expected years of schooling', 
#                     y='Life expectancy at birth',
#                     size='Gross national income (GNI) per capita',
#                     hover_data=['Country'],
#                     title=f'Expected Years of Schooling vs. Life Expectancy for Countries with Expected Years of Schooling {filter_num} or Less',
#                     labels={'Expected years of schooling': 'Expected Years of Schooling', 
#                             'Life expectancy at birth': 'Life Expectancy at Birth'}
#                 )
#     title = "Expected years of Schooling vs Life Expectancy, GNI as size"
#     custom_fig_title = dict(text=title, x=0.5,font=dict(family='Arial',size=20,color='Black')) #fig.update_layout(title=customize.custom_fig_title)
#     fig.layout = dict(title=custom_fig_title,
#                     margin=dict(l=20,r=40,t=50,b=50,pad=0),
#                     plot_bgcolor="white", #Sets the background color of the plotting area in-between x and y axes.
#                     paper_bgcolor='rgba(192, 242, 204, 0.8)', #Sets the background color of the paper where the graph is drawn.
#                     modebar=dict(orientation='v', activecolor='gray',bgcolor="white", color="#ededed"),
#                     hovermode=False, # one of ( "x" | "y" | "closest" | False | "x unified" | "y unified" )
#                     )
#     return fig

# #update graph4
# @app.callback(Output('graph4', 'figure'), Input('criteria_dropdown', 'value'))
# def update_graph4(criteria):
#     print("column: ", criteria)
#     if criteria is None:
#         PreventUpdate
#     else:
#         sorted_df = my_df.sort_values(by=criteria, ascending=False).head(10) 
#         sorted_df = sorted_df.sort_values(by=criteria, ascending=True)
#         fig = px.bar(sorted_df,
#              x=criteria,  
#              y='Country', # Categories for the bars
#              orientation='h',
             
#             )
#         title="Top Ten Countries"
#         custom_fig_title = dict(text=title, x=0.5,font=dict(family='Arial',size=20,color='Black')) #fig.update_layout(title=customize.custom_fig_title)
#         fig.layout = dict(title=custom_fig_title,
#                     margin=dict(l=20,r=40,t=50,b=50,pad=0),
#                     plot_bgcolor="white", #Sets the background color of the plotting area in-between x and y axes.
#                     paper_bgcolor='rgba(192, 242, 204, 0.8)', #Sets the background color of the paper where the graph is drawn.
#                     modebar=dict(orientation='v', activecolor='gray',bgcolor="white", color="#ededed"),
#                     hovermode=False, # one of ( "x" | "y" | "closest" | False | "x unified" | "y unified" )
#                     )
#     return fig




if __name__ == '__main__':
    app.run_server(debug=False)