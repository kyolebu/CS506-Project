import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px
from dash.dependencies import Input, Output

# List of years
years = range(2011, 2025)

# Initialize an empty list to store department averages for each year
department_averages_all_years = []

# Iterate over the years and analyze department averages
for year in years:
    try:
        # Load data for the year
        df = pd.read_csv(f"../../data/earnings-reformatted/employee-earnings-report-{year}.csv")
    except FileNotFoundError:
        print(f"File for {year} not found, skipping.")
        continue
    
    # Clean: remove $ and commas
    df.replace({r'[\$,]': '', r'\s+': ''}, regex=True, inplace=True)

    # Make sure numeric columns are numbers
    numeric_cols = ['REGULAR', 'RETRO', 'OTHER', 'OVERTIME', 'INJURED', 'DETAILS', 'QUINN', 'TOTAL EARNINGS']
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
    
    # Fill missing values with 0 for relevant columns
    df.fillna({'OVERTIME': 0, 'TOTAL EARNINGS': 0}, inplace=True)

    # Calculate overtime as % of total earnings
    df = df[df['TOTAL EARNINGS'] > 0]
    df['Overtime_Percentage'] = (df['OVERTIME'] / df['TOTAL EARNINGS']) * 100

    # Group by department and compute the mean overtime percentage
    department_avg = df.groupby('DEPARTMENT NAME')['Overtime_Percentage'].mean().reset_index()

    # Append department averages for the current year to the list
    department_averages_all_years.append(department_avg)

# Concatenate department averages across all years into a single DataFrame
all_years_department_avg = pd.concat(department_averages_all_years)

# Group by department name and compute the overall average overtime percentage
department_avg_all_years = all_years_department_avg.groupby('DEPARTMENT NAME')['Overtime_Percentage'].mean().reset_index()

# Sort by average overtime percentage in descending order
department_avg_all_years = department_avg_all_years.sort_values('Overtime_Percentage', ascending=False)

# Dash app setup
app = dash.Dash(__name__)

# Layout with slider and graph
app.layout = html.Div([
    html.H1("Department Overtime Percentage Analysis"),
    
    # Slider to select overtime percentage range
    dcc.RangeSlider(
        id='overtime-slider',
        min=0,
        max=100,
        step=1,
        marks={i: f'{i}%' for i in range(0, 101, 10)},
        value=[0, 100],  # Initial range
    ),
    
    # Graph to display department overtime percentage
    dcc.Graph(id='department-graph'),
])

# Callback to update the graph based on slider values
@app.callback(
    Output('department-graph', 'figure'),
    [Input('overtime-slider', 'value')]
)
def update_graph(overtime_range):
    min_overtime, max_overtime = overtime_range
    
    # Filter departments by overtime percentage range
    filtered_df = department_avg_all_years[(department_avg_all_years['Overtime_Percentage'] >= min_overtime) & 
                                           (department_avg_all_years['Overtime_Percentage'] <= max_overtime)]
    
    # Create the bar plot for filtered data
    fig = px.bar(filtered_df, 
                 x='DEPARTMENT NAME', 
                 y='Overtime_Percentage', 
                 title=f"Departments by Average Overtime Percentage ({min_overtime}% - {max_overtime}%)",
                 color='Overtime_Percentage', 
                 color_continuous_scale='Viridis',
                 labels={'Overtime_Percentage': 'Overtime Percentage (%)', 'DEPARTMENT NAME': 'Department Name'},
                 height=600)

    # Update layout for better visibility
    fig.update_layout(xaxis_tickangle=-45)
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
