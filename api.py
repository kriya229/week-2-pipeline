from fastapi import FastAPI

app = FastAPI()

@app.get("/cases/")
def get_cases():
    # This represents the data coming out of your Week 1 database
    return [
        {"case_id": 101, "title": "Login Issue", "priority": "High"},
        {"case_id": 102, "title": "Billing Error", "priority": "Medium"}
    ]