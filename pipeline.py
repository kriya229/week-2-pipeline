import pandas as pd
import requests
import json
from datetime import datetime

print("--- Starting Pipeline ---")

# 1. INGEST FROM WEEK 1 API
print("Fetching from API...")
response = requests.get("http://127.0.0.1:8000/cases/")
api_df = pd.DataFrame(response.json())
api_df.to_csv('data/raw/api_cases.csv', index=False)

# 2. INGEST FROM FILES
print("Reading local files...")
file_df = pd.read_csv('data/raw/file_cases.csv')
with open('data/raw/policies.json', 'r') as f:
    policies_df = pd.DataFrame(json.load(f))

# Combine API data and File data into one big table
all_cases = pd.concat([api_df, file_df], ignore_index=True)
initial_count = len(all_cases)

# 3. QUALITY CONTROLS (Quarantine rows missing a title)
print("Checking data quality...")
is_valid = all_cases['title'].notna()
good_cases = all_cases[is_valid].copy()
bad_cases = all_cases[~is_valid].copy()

# Save the bad data for humans to look at later
bad_cases.to_csv('data/rejected/bad_cases.csv', index=False)
rejected_count = len(bad_cases)

# 4. TRANSFORMATION (Join cases with SLA policy rules)
print("Standardizing and joining data...")
standardized_df = pd.merge(good_cases, policies_df, on='priority', how='left')
standardized_df.to_csv('data/standardized/clean_cases.csv', index=False)

# 5. CURATED (Create a summary report)
print("Publishing curated tables...")
curated_df = standardized_df.groupby('priority').size().reset_index(name='total_cases')
curated_df.to_csv('data/curated/priority_summary.csv', index=False)

# 6. AUDIT
print(f"\n=== AUDIT LOG ===")
print(f"Total Ingested: {initial_count}")
print(f"Total Rejected: {rejected_count}")
print(f"Total Cleaned:  {len(good_cases)}")
if initial_count == rejected_count + len(good_cases):
    print("STATUS: SUCCESS")