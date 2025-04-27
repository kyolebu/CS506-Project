import pandas as pd
from pathlib import Path

def load_earnings_data(year):
    """Load earnings data for a given year and standardize column names."""
    data_dir = Path(__file__).parent.parent.parent / 'data' / 'earnings'
    file_path = data_dir / f'employee-earnings-report-{year}.csv'
    
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='latin-1')
    
    print(f"\nProcessing {year} data:")
    print("Original columns:", df.columns.tolist())
    
    # Clean column names by stripping whitespace
    df.columns = df.columns.str.strip()
    
    # Map column names to standardized format
    column_mapping = {
        'TOTAL EARNINGS': 'TOTAL GROSS',
        'TOTAL_EARNINGS': 'TOTAL GROSS',
        'TOTAL GROSS': 'TOTAL GROSS',
        'TOTAL_ GROSS': 'TOTAL GROSS',  # Handle space variation
        ' TOTAL EARNINGS ': 'TOTAL GROSS',  # Handle 2020 format
        'QUINN': 'QUINN_EDUCATION',
        'QUINN/EDUCATION INCENTIVE': 'QUINN_EDUCATION',
        'QUINN / EDUCATION INCENTIVE': 'QUINN_EDUCATION',
        ' QUINN / EDUCATION INCENTIVE ': 'QUINN_EDUCATION',  # Handle 2020 format
        'DEPARTMENT': 'DEPARTMENT_NAME',
        'DEPARTMENT NAME': 'DEPARTMENT_NAME',
        'DETAIL ': 'DETAIL'  # Handle extra space
    }
    
    # Apply column mapping
    df = df.rename(columns=column_mapping)
    print("Columns after mapping:", df.columns.tolist())
    
    # Function to clean numeric values
    def clean_numeric(x):
        if pd.isna(x):
            return x
        if isinstance(x, str):
            # If the string contains multiple values (space-separated), take the first one
            x = x.split()[0] if ' ' in x else x
            # Remove $ and , and convert to float
            x = x.replace('$', '').replace(',', '')
        return pd.to_numeric(x, errors='coerce')
    
    # Clean numeric columns
    numeric_columns = ['TOTAL GROSS', 'REGULAR', 'RETRO', 'OTHER', 'OVERTIME', 'INJURED', 'DETAIL', 'QUINN_EDUCATION']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = df[col].apply(clean_numeric)
    
    print("Final columns:", df.columns.tolist())
    print(f"Number of rows: {len(df)}\n")
    
    return df 