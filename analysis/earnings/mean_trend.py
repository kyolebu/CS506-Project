import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from utils import load_earnings_data

def analyze_mean_earnings(year):
    """Analyze mean earnings for police department employees for a given year."""
    df = load_earnings_data(year)
    
    # Find the department column
    dept_col = 'DEPARTMENT_NAME'
    total_col = 'TOTAL GROSS'
    
    # Filter for police department
    police_df = df[df[dept_col].str.contains('POLICE', case=False, na=False)]
    
    # Calculate mean earnings
    mean_earnings = police_df[total_col].mean()
    
    print(f"\nYear {year} Summary:")
    print(f"Number of police employees: {len(police_df)}")
    print(f"Mean earnings: ${mean_earnings:,.2f}")
    print(f"Using department column: {dept_col}")
    print(f"Using total earnings column: {total_col}")
    
    return year, mean_earnings, len(police_df)

def main():
    # Analyze data for each year
    years = [2012, 2014, 2016, 2018, 2020, 2022, 2024]
    results = []
    
    for year in years:
        try:
            result = analyze_mean_earnings(year)
            results.append(result)
        except Exception as e:
            print(f"\nError processing year {year}:")
            print(str(e))
    
    # Create visualization
    if results:
        years, means, counts = zip(*results)
        
        plt.figure(figsize=(12, 6))
        plt.plot(years, means, marker='o', linestyle='-', linewidth=2, markersize=8)
        
        # Add value labels above each point
        for i, (year, mean, count) in enumerate(results):
            plt.annotate(f'${mean:,.0f}', 
                        (year, mean),
                        textcoords="offset points",
                        xytext=(0,10),
                        ha='center',
                        fontsize=9)
        
        plt.title('Mean Earnings Trend - Boston Police Department (2012-2024)', fontsize=12, pad=20)
        plt.xlabel('Year', fontsize=10)
        plt.ylabel('Mean Earnings ($)', fontsize=10)
        plt.grid(True, linestyle='--', alpha=0.7)
        
        # Format y-axis with dollar signs and commas
        plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
        
        # Save the plot in the EDA directory within earnings analysis
        output_dir = Path(__file__).parent / 'EDA'
        output_dir.mkdir(exist_ok=True)
        plt.savefig(output_dir / 'mean_earnings_trend.png', bbox_inches='tight', dpi=300)
        print(f"\nPlot saved as 'mean_earnings_trend.png' in {output_dir}")

if __name__ == "__main__":
    main()