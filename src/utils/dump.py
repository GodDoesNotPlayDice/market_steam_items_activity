import pandas as pd
import os, json
from d_types import MarketData

e_file = os.path.join(os.path.dirname(__file__), '../data/market_activity.xlsx')

if not os.path.exists(e_file):
    headers = ["action", "price", "timestamp"]
    df = pd.DataFrame(columns=headers)
    df.to_excel(e_file, index=False, sheet_name='MarketActivity')
    print('Excel file created')

df_existing = pd.read_excel(e_file, sheet_name='MarketActivity')

with open(os.path.join(os.path.dirname(__file__), '../data/data.json'), 'r') as f:
    data = MarketData(**json.load(f))
    activity_data = [dict(activity) for activity in data.activities]
    df_new = pd.DataFrame(activity_data)
    df_existing = df_existing.dropna(axis=1, how='all')
    df_new = df_new.dropna(axis=1, how='all')
    df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    df_combined.to_excel(e_file, index=False, sheet_name='MarketActivity')
    print('Data added to market_activity.xlsx')
    print(df_combined)
