import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
import plotly.express as px
from roster import preprocess as preprocess_roster
from roster import plot_ethnic_grp_dist
from roster import plot_gender_dist
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from earnings.utils import load_earnings_data

def create_top_earners_chart(df, year):
    plt.figure(figsize=(15, 8))
    
    # Get top 10 earners
    top_10 = df.nlargest(10, 'TOTAL GROSS')
    
    # Define components and colors
    components = ['REGULAR', 'OVERTIME', 'DETAIL', 'QUINN_EDUCATION', 'INJURED', 'RETRO', 'OTHER']
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#9467bd', '#17becf', '#ff9896', '#d62728']
    
    # Prepare data for stacking
    y_pos = np.arange(10)
    left = np.zeros(10)
    
    # Create stacked bars
    for component, color in zip(components, colors):
        if component in df.columns:
            values = top_10[component].fillna(0).values  # Replace NaN with 0
            plt.barh(y_pos, values, left=left, label=component.title().replace('_', ' '), color=color)
            left += values
    
    # Customize plot
    plt.title(f'Top 10 Earners in Boston Police Department ({year})', pad=20)
    plt.xlabel('Total Earnings ($)')
    
    # Add employee names as y-axis labels
    names = top_10['NAME'].values
    plt.yticks(y_pos, names)
    
    # Format x-axis to show dollars
    plt.gca().xaxis.set_major_formatter(lambda x, p: f'${x:,.0f}')
    
    # Add total earnings as text at the end of each bar
    for idx, total in enumerate(top_10['TOTAL GROSS'].values):
        plt.text(total, idx, f'  ${total:,.0f}', va='center')
    
    # Adjust legend and layout
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Save the figure
    output_dir = Path(__file__).parent / 'EDA'
    output_dir.mkdir(exist_ok=True)
    plt.savefig(output_dir / f'top_earners_{year}.png', bbox_inches='tight', dpi=300)
    print(f"\nPlot saved as 'top_earners_{year}.png' in {output_dir}")

# Normalize roster_df name columns
def preprocess_and_merge(n, roster_df, police_df):
    roster_df['Last'] = roster_df['Last'].str.strip().str.upper()
    roster_df['First Name'] = roster_df['First Name'].str.strip().str.upper()

    # Get top earners' name columns
    top_n = police_df.nlargest(n, 'TOTAL GROSS').copy()

    # Split and normalize names
    top_n[['Last', 'First Name']] = top_n['NAME'].str.split(',', expand=True)
    top_n['Last'] = top_n['Last'].str.strip().str.upper()
    top_n['First Name'] = top_n['First Name'].str.strip().str.split().str[0].str.upper()

    # Merge on normalized names
    top_n_with_roster_df = pd.merge(
        top_n,
        roster_df,
        on=['Last', 'First Name'],
        how='inner' # keep the top 100 even if roster_df is NA?
    )

    # Drop duplicate matches
    top_n_with_roster_df = top_n_with_roster_df.drop_duplicates(subset=['Last', 'First Name'])

    return top_n_with_roster_df

def plot_income_ranking_with_demographics(df: pd.DataFrame, title: str = "Top 100 Earners by Income Ranking", filename: str = "top_100_income_ranking.html"):
    """
    Creates a scatter plot using Plotly showing income ranking vs gross income,
    with demographic info on hover.

    Args:
        df (pd.DataFrame): DataFrame containing columns 'TOTAL GROSS', 'NAME', 'Job Title',
                           'Sex_M', and 'Ethnic Grp Categorical'.
        title (str): Title of the chart.
        filename (str): Filename to save the HTML plot.
    """
    # Sort by TOTAL GROSS descending and add a rank column
    df = df.sort_values(by="TOTAL GROSS", ascending=False).reset_index(drop=True)
    df['Rank'] = df.index + 1

    # Format hover text
    df['Sex'] = df['Sex_M'].apply(lambda x: 'Male' if x else 'Female')
    df['Hover Info'] = (
        "Name: " + df['NAME'] + "<br>" +
        "Job Title: " + df['Job Title'].fillna("N/A") + "<br>" +
        "Sex: " + df['Sex'] + "<br>" +
        "Ethnic Group: " + df['Ethnic Grp Categorical'].fillna("N/A") + "<br>" +
        "Total Earnings: $" + df['TOTAL GROSS'].map("{:,.2f}".format)
    )

    # Create the plot
    fig = px.scatter(
        df,
        x="Rank",
        y="TOTAL GROSS",
        hover_name="NAME",
        hover_data={"Hover Info": True, "TOTAL GROSS": False, "Rank": False},
        labels={"TOTAL GROSS": "Total Gross Income", "Rank": "Income Rank"},
        title=title
    )

    fig.update_traces(marker=dict(size=8, color='blue'), hovertemplate=df['Hover Info'])
    fig.update_layout(
        xaxis=dict(tickmode='linear', dtick=10),
        yaxis_tickprefix="$",
        hoverlabel=dict(bgcolor="white", font_size=12),
        margin=dict(t=80, r=20, l=60, b=60),
        height=600,
        template='plotly_white'
    )

    # Save the plot
    output_path = Path(__file__).parent / "EDA"
    output_path.mkdir(exist_ok=True)
    fig.write_html(output_path / filename)
    fig.show()
    print(f"\nInteractive plot saved as '{filename}' in {output_path}")

if __name__ == "__main__":
    year = 2020 # use the year that corresponds with roster data
    
    try:
        # Load and filter data
        df = load_earnings_data(year)
        police_df = df[df['DEPARTMENT_NAME'].str.contains('POLICE', case=False, na=False)].copy()
        print('police df:', police_df.head())
        roster_df = preprocess_roster(pd.read_csv(f"../../data/roster/bpd-roster-2020.csv"))
        
        # Ensure all numeric columns are properly converted
        components = ['REGULAR', 'OVERTIME', 'DETAIL', 'QUINN_EDUCATION', 'INJURED', 'RETRO', 'OTHER', 'TOTAL GROSS']
        for col in components:
            if col in police_df.columns:
                police_df[col] = pd.to_numeric(police_df[col], errors='coerce').fillna(0)
        
        # Create visualization
        # create_top_earners_chart(police_df, year)
        
        # Print detailed breakdown for top 10
        print(f"\nDetailed Breakdown of Top 10 Earners ({year})")
        print("-" * 80)
        
        top_10 = police_df.nlargest(10, 'TOTAL GROSS')
        components = ['REGULAR', 'OVERTIME', 'DETAIL', 'QUINN_EDUCATION', 'INJURED', 'RETRO', 'OTHER']
        roster_components = ['Job Title', 'Sex_M', 'Ethnic Grp Categorical']
        
        # printing for top 10
        for idx, row in top_10.iterrows():
            full_name = row['NAME']
            last, first = full_name.split(',')
            last = last.strip().upper()
            first = first.strip().split(' ')[0].upper()
            
            # Normalize name columns in roster
            roster_df['Last'] = roster_df['Last'].str.strip().str.upper()
            roster_df['First Name'] = roster_df['First Name'].str.strip().str.upper()
            
            matching_roster_row = roster_df.loc[
                (roster_df['Last'] == last) & (roster_df['First Name'] == first)
            ]
            
            print(f"\n{row['NAME']} — Total Earnings: ${row['TOTAL GROSS']:,.2f}")
            
            if not matching_roster_row.empty:
                m = matching_roster_row.iloc[0]
                print("Diversity Background:")
                print(f"  Job Title         : {m['Job Title']}")
                print(f"  Sex               : {'Male' if m['Sex_M'] else 'Female'}")
                print(f"  Ethnic Group      : {m['Ethnic Grp Categorical']}")
            else:
                print("Diversity Background: No match found in roster.")
            
            print("Component Breakdown:")
            
            component_sum = 0
            for component in components:
                if component in police_df.columns and row[component] > 0:
                    percentage = (row[component] / row['TOTAL GROSS'] * 100)
                    print(f"  {component:<17}: ${row[component]:,.2f} ({percentage:.1f}%)")
                    component_sum += row[component]
            
            diff = row['TOTAL GROSS'] - component_sum
            print(f"\n  Sum of Components  : ${component_sum:,.2f}")
            print(f"  Difference from Total: ${diff:,.2f} ({(diff / row['TOTAL GROSS']) * 100:.1f}%)")


        ### data analysis for top 100
        top_100_with_roster_df = preprocess_and_merge(100, roster_df, police_df)
        print("length of top_100 with_roster_df:", len(top_100_with_roster_df))

        plot_gender_dist(top_100_with_roster_df, "top_100_gender_distribution") # from roster.py
        plot_ethnic_grp_dist(top_100_with_roster_df, "top_100_ethnic_group_distribution") # from roster.py
        plot_income_ranking_with_demographics(top_100_with_roster_df) # from earlier function
        
        
    except Exception as e:
        print(f"\nError processing year {year}: {str(e)}") 
        