import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
import plotly.express as px
from roster import preprocess as preprocess_roster
from roster2 import preprocess_and_merge
import sys
import os
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree
from sklearn.preprocessing import LabelEncoder

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from earnings.utils import load_earnings_data

if __name__ == "__main__":
    # Load and prepare data
    df = load_earnings_data(2020)
    police_df = df[df['DEPARTMENT_NAME'].str.contains('POLICE', case=False, na=False)].copy()
    roster_df = preprocess_roster(pd.read_csv("../../data/roster/bpd-roster-2020.csv"))
    merged_df = preprocess_and_merge(22000, roster_df, police_df).copy()

    # Drop rows without earnings or demographic info
    merged_df = merged_df.dropna(subset=['TOTAL GROSS', 'Sex_M', 'Ethnic Grp Categorical'])

    # Create target: High Earner = 1 if > $150,000
    # merged_df['High_Earner'] = (merged_df['TOTAL GROSS'] > 132488).astype(int) # threshold set according to 2020 mean --> seems too low since almost all classified as false
    merged_df['High_Earner'] = (merged_df['TOTAL GROSS'] > 150000).astype(int)

    # Features to use for prediction
    # feature_cols = ['REGULAR', 'OVERTIME', 'DETAIL', 'QUINN_EDUCATION', 'INJURED', 'RETRO', 'OTHER', 'Sex_M', 'Ethnic Grp_BLACK', 'Ethnic Grp_HISPA', 'Ethnic Grp_WHITE', 'Ethnic Grp_ASIAN'] # everything possible
    # feature_cols = ['REGULAR', 'OVERTIME','Sex_M', 'Ethnic Grp_BLACK', 'Ethnic Grp_HISPA', 'Ethnic Grp_WHITE', 'Ethnic Grp_ASIAN'] # demographic info + minimal pay
    feature_cols = ['Sex_M', 'Ethnic Grp_BLACK', 'Ethnic Grp_HISPA', 'Ethnic Grp_WHITE', 'Ethnic Grp_ASIAN'] # most minimal set, just demogrpahic info
    X = merged_df[feature_cols].copy()
    y = merged_df['High_Earner']

    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train decision tree
    clf = DecisionTreeClassifier(max_depth=3)
    clf.fit(X_train, y_train)

    # Text tree
    tree_rules = export_text(clf, feature_names=X.columns.tolist())
    print("\nDecision Tree Rules:\n")
    print(tree_rules)

    # Visual tree
    plt.figure(figsize=(12, 8))
    plot_tree(clf, feature_names=X.columns, class_names=["Low", "High"], filled=True, rounded=True)
    plt.title("Decision Tree: Predicting High-Earning Officers")

    output_dir = Path(__file__).parent / 'EDA'
    output_dir.mkdir(exist_ok=True)
    plt.savefig(output_dir / f'top_earners_decision_tree{2020}.png', bbox_inches='tight', dpi=300) # comment out when don't want saved
    
    plt.show()
