import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
from roster import preprocess as preprocess_roster
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
        create_top_earners_chart(police_df, year)
        
        # Print detailed breakdown for top 10
        print(f"\nDetailed Breakdown of Top 10 Earners ({year})")
        print("-" * 80)
        
        top_10 = police_df.nlargest(10, 'TOTAL GROSS')
        components = ['REGULAR', 'OVERTIME', 'DETAIL', 'QUINN_EDUCATION', 'INJURED', 'RETRO', 'OTHER']
        roster_components = ['Job Title', 'Sex_M', 'Ethnic Grp Categorical']
        
        for idx, row in top_10.iterrows():
            full_name = row['NAME']
            last, first = full_name.split(',')
            first = first.split(' ')[0] # get rid of middle initial
            matching_roster_row = roster_df.loc[(roster_df['Last'] == last) & (roster_df['First Name'] == first)]
            print(f"\n{row['NAME']} - Total: ${row['TOTAL GROSS']:,.2f}")
            if not matching_roster_row.empty:
              print("Diversity Background: ")
              for rc in roster_components:
                  if rc == 'Sex_M':
                      sex = "Male" if matching_roster_row[rc].bool() else "Female"
                      print(f"Sex: {sex}")
                  else:
                      print(f"{rc}: {matching_roster_row[rc]}")
            else:
                print("No Matching Diversity Background: ")
            print()
            print("Component Breakdown:")
            
            # Calculate sum of components (replacing NaN with 0)
            component_sum = sum(row[component] if pd.notnull(row[component]) else 0 
                              for component in components if component in police_df.columns)
            
            # Print each component
            for component in components:
                if component in police_df.columns and row[component] > 0:
                    percentage = (row[component] / row['TOTAL GROSS'] * 100)
                    print(f"  {component}: ${row[component]:,.2f} ({percentage:.1f}%)")
            
            # Print verification of totals
            print(f"\nSum of Components: ${component_sum:,.2f}")
            difference = row['TOTAL GROSS'] - component_sum
            print(f"Difference from Total Gross: ${difference:,.2f} ({(difference/row['TOTAL GROSS']*100):.1f}%)")
        
    except Exception as e:
        print(f"\nError processing year {year}: {str(e)}") 