import matplotlib.pyplot as plt
from pathlib import Path
from utils import load_earnings_data

if __name__ == "__main__":
    # Load data for 2023 (most recent complete year)
    df = load_earnings_data(2023)
    
    # Calculate overtime percentage
    df['OT_PERCENTAGE'] = (df['OVERTIME'] / df['TOTAL GROSS'] * 100).round(2)
    
    # Create figure
    plt.figure(figsize=(12, 6))
    
    # Plot histogram of overtime percentage
    plt.hist(df['OT_PERCENTAGE'], bins=50, color='orange', edgecolor='black')
    plt.title('Distribution of Overtime as Percentage of Total Earnings (2023)')
    plt.xlabel('Overtime Percentage (%)')
    plt.ylabel('Number of Employees')
    plt.grid(True, alpha=0.3)
    
    # Add vertical lines for key statistics
    mean_percentage = df['OT_PERCENTAGE'].mean()
    median_percentage = df['OT_PERCENTAGE'].median()
    
    plt.axvline(mean_percentage, color='red', linestyle='--', label=f'Mean: {mean_percentage:.1f}%')
    plt.axvline(median_percentage, color='green', linestyle='--', label=f'Median: {median_percentage:.1f}%')
    
    plt.legend()
    
    # Save the figure
    output_path = Path('figures')
    output_path.mkdir(exist_ok=True)
    plt.savefig(output_path / 'overtime_percentage_2023.png', 
                dpi=300, 
                bbox_inches='tight')
    plt.close()
    
    # Print summary statistics
    print("\nOvertime Percentage Summary (2023)")
    print("-" * 50)
    print(f"Total Employees: {len(df):,}")
    print(f"Mean Overtime %: {mean_percentage:.2f}%")
    print(f"Median Overtime %: {median_percentage:.2f}%")
    print(f"Min Overtime %: {df['OT_PERCENTAGE'].min():.2f}%")
    print(f"Max Overtime %: {df['OT_PERCENTAGE'].max():.2f}%")
    
    # Print top 10 employees by overtime percentage
    print("\nTop 10 Employees by Overtime Percentage:")
    print("-" * 50)
    top_10 = df.nlargest(10, 'OT_PERCENTAGE')[['NAME', 'TOTAL GROSS', 'OVERTIME', 'OT_PERCENTAGE']]
    print(top_10.to_string(index=False)) 