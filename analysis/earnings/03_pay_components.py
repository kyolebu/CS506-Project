import matplotlib.pyplot as plt
from pathlib import Path
from utils import load_earnings_data

if __name__ == "__main__":
    df = load_earnings_data(2023)
    
    # Calculate total for each component
    components = ['REGULAR', 'OVERTIME', 'DETAIL', 'OTHER', 'INJURED', 'QUINN_EDUCATION']
    totals = {col: df[col].sum() for col in components if col in df.columns}
    
    # Create figure
    plt.figure(figsize=(12, 6))
    
    # Create pie chart
    plt.pie(totals.values(), labels=totals.keys(), autopct='%1.1f%%', 
            colors=['lightblue', 'lightgreen', 'pink', 'orange', 'purple', 'yellow'])
    plt.title('Distribution of Pay Components (2023)')
    
    # Save the figure
    output_path = Path('figures')
    output_path.mkdir(exist_ok=True)
    plt.savefig(output_path / 'pay_components_2023.png', 
                dpi=300, 
                bbox_inches='tight')
    plt.close()
    
    # Print summary statistics
    print("\nPay Components Summary (2023)")
    print("-" * 50)
    total_gross = df['TOTAL GROSS'].sum()
    for component, amount in totals.items():
        percentage = (amount / total_gross * 100)
        print(f"{component}: ${amount:,.2f} ({percentage:.1f}%)")
    
    print(f"\nTotal Gross Pay: ${total_gross:,.2f}") 