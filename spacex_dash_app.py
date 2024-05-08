# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the spacex data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Calculate min and max payload values
min_payload = spacex_df['Payload Mass (kg)'].min()
max_payload = spacex_df['Payload Mass (kg)'].max()
# Create a dash application
app = dash.Dash(__name__)

# Get unique launch sites
launch_sites = spacex_df['Launch Site'].unique()

# Create options for dropdown menu
dropdown_options = [{'label': 'All Sites', 'value': 'ALL'}] + [{'label': site, 'value': site} for site in launch_sites]

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

    # TASK 1: Add a dropdown list to enable Launch Site selection
    html.Div([
        dcc.Dropdown(
            id='site-dropdown',
            options=dropdown_options,
            value='ALL',
            placeholder="Select a Launch Site",
            searchable=True
        )
    ], style={'width': '50%', 'margin': 'auto'}),

    html.Br(),

    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    # If a specific launch site was selected, show the Success vs. Failed counts for the site
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),

    # TASK 3: Add a slider to select payload range
    html.Div([
        dcc.RangeSlider(
            id='payload-slider',
            min=0,
            max=10000,
            step=1000,
            marks={0: '0', 10000: '10000'},
            value=[min_payload, max_payload]
        )
    ], style={'width': '50%', 'margin': 'auto'}),

    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2: Add a callback function to render success-pie-chart based on selected site dropdown
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value')]
)
def render_success_pie_chart(selected_site):
    if selected_site == 'ALL':
        # Count success and failure for all sites
        success_count = spacex_df[spacex_df['class'] == 1].shape[0]
        failure_count = spacex_df[spacex_df['class'] == 0].shape[0]
        # Create pie chart
        pie_chart_data = {
            'Success': success_count,
            'Failure': failure_count
        }
        fig = px.pie(values=list(pie_chart_data.values()), names=list(pie_chart_data.keys()), title='Total Success vs. Failure Counts')
        return fig
    else:
        # Count success and failure for the selected site
        selected_site_data = spacex_df[spacex_df['Launch Site'] == selected_site]
        success_count = selected_site_data[selected_site_data['class'] == 1].shape[0]
        failure_count = selected_site_data[selected_site_data['class'] == 0].shape[0]
        # Create pie chart
        pie_chart_data = {
            'Success': success_count,
            'Failure': failure_count
        }
        fig = px.pie(values=list(pie_chart_data.values()), names=list(pie_chart_data.keys()), title=f'Success vs. Failure Counts for {selected_site}')
        return fig

# TASK 3: Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

# TASK 4: Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), 
     Input(component_id="payload-slider", component_property="value")]
)
def render_success_payload_scatter_chart(selected_site, payload_range):
    # Filter dataframe based on selected site
    if selected_site == 'ALL':
        filtered_df = spacex_df
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
    
    # Filter dataframe based on selected payload range
    filtered_df = filtered_df[(filtered_df['Payload Mass (kg)'] >= payload_range[0]) & 
                              (filtered_df['Payload Mass (kg)'] <= payload_range[1])]
    
    # Create scatter plot
    fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category', 
                     title='Payload vs. Launch Outcome', 
                     labels={'Payload Mass (kg)': 'Payload Mass (kg)', 'class': 'Launch Outcome'},
                     color_discrete_sequence=px.colors.qualitative.Set1)
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()

