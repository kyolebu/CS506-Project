import pandas as pd
from pathlib import Path

def load_earnings_data(year):
    """Load earnings data for a specific year"""
    file_path = Path(f'././data/earnings/employee-earnings-report-{year}.csv')
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='latin1')
    
    # Clean numeric columns
    numeric_columns = ['REGULAR', 'RETRO', 'OTHER', 'OVERTIME', 'INJURED', 
                      'DETAIL', 'QUINN_EDUCATION', 'TOTAL GROSS']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].str.replace(',', ''), errors='coerce')
    
    return df 