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

# Find the real min and max overtime percentages
min_overtime = department_avg_all_years['Overtime_Percentage'].min()
max_overtime = department_avg_all_years['Overtime_Percentage'].max()

# Also calculate total overtime earned per department across all years
department_totals_all_years = pd.concat(department_averages_all_years)  # we already have the yearly data

# Now we need the TOTAL dollars, so go back to the original earnings data per year
# Re-read the yearly files and accumulate overtime by department
department_total_overtime_list = []

for year in years:
    try:
        df = pd.read_csv(f"../../data/earnings-reformatted/employee-earnings-report-{year}.csv")
    except FileNotFoundError:
        continue
    
    df.replace({r'[\$,]': '', r'\s+': ''}, regex=True, inplace=True)
    numeric_cols = ['REGULAR', 'RETRO', 'OTHER', 'OVERTIME', 'INJURED', 'DETAILS', 'QUINN', 'TOTAL EARNINGS']
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
    
    df.fillna({'OVERTIME': 0, 'TOTAL EARNINGS': 0}, inplace=True)
    
    dept_overtime = df.groupby('DEPARTMENT NAME')['OVERTIME'].sum().reset_index()
    department_total_overtime_list.append(dept_overtime)

# Concatenate total overtime earnings across all years
department_total_overtime_all_years = pd.concat(department_total_overtime_list)

# Group again to get the total overtime per department
department_total_overtime = department_total_overtime_all_years.groupby('DEPARTMENT NAME')['OVERTIME'].sum().reset_index()

# Sort descending
department_total_overtime = department_total_overtime.sort_values('OVERTIME', ascending=False)

min_total_ot = department_total_overtime['OVERTIME'].min()
max_total_ot = department_total_overtime['OVERTIME'].max()
step = (max_total_ot - min_total_ot) / 200

# Dash app setup
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Department Overtime Analysis"),

    dcc.Dropdown(
        id='metric-dropdown',
        options=[
            {'label': 'Average Overtime Percentage', 'value': 'avg'},
            {'label': 'Total Overtime Earned ($)', 'value': 'total'},
        ],
        value='avg',
        clearable=False,
        style={'width': '50%', 'margin-bottom': '20px'}
    ),
    
    # Percentage slider (Initially shown)
    html.Div(
        dcc.RangeSlider(
            id='overtime-percentage-slider',
            min=min_overtime,
            max=max_overtime,
            step=0.5,
            marks={int(i): f'{int(i)}%' for i in range(int(min_overtime), int(max_overtime)+1, 5)},
            value=[min_overtime, max_overtime],
        ),
        id='percentage-slider-container',  # ID for the wrapper
    ),

    # Total Overtime ($) slider (Initially hidden)
    html.Div(
        dcc.RangeSlider(
            id='overtime-total-slider',
            min=min_total_ot,
            max=max_total_ot,
            step=step,
            marks=None,
            value=[min_total_ot, max_total_ot],
        ),
        id='total-slider-container',  # ID for the wrapper
        style={'display': 'none'}  # Initially hide this slider
    ),

    dcc.Graph(id='department-graph'),
])

# Callback now updates two outputs
@app.callback(
    [Output('percentage-slider-container', 'style'),
     Output('total-slider-container', 'style')],
    [Input('metric-dropdown', 'value')]
)
def toggle_sliders(selected_metric):
    if selected_metric == 'avg':
        # Show the percentage slider, hide the total overtime slider
        return {'display': 'block'}, {'display': 'none'}
    elif selected_metric == 'total':
        # Show the total overtime slider, hide the percentage slider
        return {'display': 'none'}, {'display': 'block'}

@app.callback(
    Output('department-graph', 'figure'),
    [Input('metric-dropdown', 'value'),
     Input('overtime-percentage-slider', 'value'),
     Input('overtime-total-slider', 'value')]
)
def update_graph(selected_metric, overtime_percentage_range, overtime_total_range):
    if selected_metric == 'avg':
        min_overtime, max_overtime = overtime_percentage_range
        filtered_df = department_avg_all_years[
            (department_avg_all_years['Overtime_Percentage'] >= min_overtime) & 
            (department_avg_all_years['Overtime_Percentage'] <= max_overtime)
        ]
        fig = px.bar(filtered_df, 
                     x='DEPARTMENT NAME', 
                     y='Overtime_Percentage', 
                     title=f"Departments by Average Overtime Percentage ({min_overtime:.1f}% - {max_overtime:.1f}%)",
                     color='Overtime_Percentage', 
                     color_continuous_scale='Viridis',
                     labels={'Overtime_Percentage': 'Overtime Percentage (%)', 'DEPARTMENT NAME': 'Department Name'},
                     height=600)
        fig.update_layout(xaxis_tickangle=-45)
        
    elif selected_metric == 'total':
        min_total, max_total = overtime_total_range
        filtered_df = department_total_overtime[
            (department_total_overtime['OVERTIME'] >= min_total) & 
            (department_total_overtime['OVERTIME'] <= max_total)
        ]
        fig = px.bar(filtered_df, 
                     x='DEPARTMENT NAME', 
                     y='OVERTIME', 
                     title=f"Departments by Total Overtime Earned (${min_total:,.0f} - ${max_total:,.0f})",
                     color='OVERTIME', 
                     color_continuous_scale='Cividis',
                     labels={'OVERTIME': 'Total Overtime ($)', 'DEPARTMENT NAME': 'Department Name'},
                     height=600)
        fig.update_layout(xaxis_tickangle=-45)
        
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
