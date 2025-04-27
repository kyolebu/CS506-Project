import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from utils import load_earnings_data

def analyze_earnings_distribution(year):
    """Analyze earnings distribution for a given year and return the data"""
    # Load data
    df = load_earnings_data(year)
    
    # Filter for police department employees
    df = df[df['DEPARTMENT_NAME'].str.contains('POLICE', case=False, na=False)]
    
    # Calculate statistics on all data
    mean_earnings = df['TOTAL GROSS'].mean()
    median_earnings = df['TOTAL GROSS'].median()
    min_earnings = df['TOTAL GROSS'].min()
    max_earnings = df['TOTAL GROSS'].max()
    std_earnings = df['TOTAL GROSS'].std()
    
    # Print summary statistics
    print(f"\nEarnings Distribution Summary ({year})")
    print("-" * 50)
    print(f"Total Employees: {len(df):,}")
    print(f"Mean Earnings: ${mean_earnings:,.2f}")
    print(f"Median Earnings: ${median_earnings:,.2f}")
    print(f"Min Earnings: ${min_earnings:,.2f}")
    print(f"Max Earnings: ${max_earnings:,.2f}")
    print(f"Standard Deviation: ${std_earnings:,.2f}")
    
    return df['TOTAL GROSS'].dropna(), mean_earnings, median_earnings

if __name__ == "__main__":
    # Create figure with two subplots side by side
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
    
    # Process and plot 2012 data
    earnings_2012, mean_2012, median_2012 = analyze_earnings_distribution(2012)
    ax1.hist(earnings_2012, bins=50, color='skyblue', edgecolor='black')
    ax1.axvline(mean_2012, color='red', linestyle='--', label=f'Mean: ${mean_2012:,.0f}')
    ax1.axvline(median_2012, color='green', linestyle='--', label=f'Median: ${median_2012:,.0f}')
    ax1.set_title('Distribution of Total Earnings - Police Department (2012)')
    ax1.set_xlabel('Total Earnings ($)')
    ax1.set_ylabel('Number of Employees')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Process and plot 2024 data
    earnings_2024, mean_2024, median_2024 = analyze_earnings_distribution(2024)
    ax2.hist(earnings_2024, bins=50, color='skyblue', edgecolor='black')
    ax2.axvline(mean_2024, color='red', linestyle='--', label=f'Mean: ${mean_2024:,.0f}')
    ax2.axvline(median_2024, color='green', linestyle='--', label=f'Median: ${median_2024:,.0f}')
    ax2.set_title('Distribution of Total Earnings - Police Department (2024)')
    ax2.set_xlabel('Total Earnings ($)')
    ax2.set_ylabel('Number of Employees')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    # Add overall title
    plt.suptitle('Distribution of Total Earnings - Police Department (2012 vs 2024)', 
                 fontsize=16, y=1.05)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the figure
    output_path = Path('EDA')
    output_path.mkdir(exist_ok=True)
    plt.savefig(output_path / 'earnings_distribution_comparison.png', 
                dpi=300, 
                bbox_inches='tight')
    plt.close() 