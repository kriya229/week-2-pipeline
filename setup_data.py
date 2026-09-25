import os
import pandas as pd
import json

# Create the pipeline folders
for f in ['data/raw', 'data/rejected', 'data/standardized', 'data/curated']:
    os.makedirs(f, exist_ok=True)

# Create messy CSV data (Notice case 300 has no title!)
cases_data = pd.DataFrame({
    'case_id': [201, 202, 300],
    'title': ['App crash', 'Slow loading', None],
    'priority': ['High', 'Low', 'Low']
})
cases_data.to_csv('data/raw/file_cases.csv', index=False)

# Create a policy metadata JSON file
policies = [{"priority": "High", "sla_hours": 24}, {"priority": "Medium", "sla_hours": 48}, {"priority": "Low", "sla_hours": 72}]
with open('data/raw/policies.json', 'w') as f:
    json.dump(policies, f)

print("Mock files created in data/raw!")