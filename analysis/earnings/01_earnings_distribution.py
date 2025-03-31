import matplotlib.pyplot as plt
from pathlib import Path
from utils import load_earnings_data

if __name__ == "__main__":
    # Load data
    df = load_earnings_data(2023)
    
    # Create figure
    plt.figure(figsize=(12, 6))
    
    # Plot histogram of total earnings
    plt.hist(df['TOTAL GROSS'], bins=50, color='skyblue', edgecolor='black')
    plt.title('Distribution of Total Earnings (2023)')
    plt.xlabel('Total Earnings ($)')
    plt.ylabel('Number of Employees')
    plt.grid(True, alpha=0.3)
    
    # Add vertical lines for key statistics
    mean_earnings = df['TOTAL GROSS'].mean()
    median_earnings = df['TOTAL GROSS'].median()
    
    plt.axvline(mean_earnings, color='red', linestyle='--', label=f'Mean: ${mean_earnings:,.0f}')
    plt.axvline(median_earnings, color='green', linestyle='--', label=f'Median: ${median_earnings:,.0f}')
    
    plt.legend()
    
    # Save the figure
    output_path = Path('figures')
    output_path.mkdir(exist_ok=True)
    plt.savefig(output_path / 'earnings_distribution_2023.png', 
                dpi=300, 
                bbox_inches='tight')
    plt.close()
    
    # Print summary statistics
    print("\nEarnings Distribution Summary (2023)")
    print("-" * 50)
    print(f"Total Employees: {len(df):,}")
    print(f"Mean Earnings: ${mean_earnings:,.2f}")
    print(f"Median Earnings: ${median_earnings:,.2f}")
    print(f"Min Earnings: ${df['TOTAL GROSS'].min():,.2f}")
    print(f"Max Earnings: ${df['TOTAL GROSS'].max():,.2f}")
    print(f"Standard Deviation: ${df['TOTAL GROSS'].std():,.2f}") 