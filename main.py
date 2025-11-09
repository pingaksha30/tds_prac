from fastapi import FastAPI, Query, Response
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load dataset
df = pd.read_json("data.json")

@app.get("/query")
def query(q: str = Query(...), response: Response = None):
    response.headers["X-Email"] = "23f2003519@ds.study.iitm.ac.in"
    
    try:
        answer = handle_query(q)
        return {"answer": answer}
    except Exception as e:
        return {"error": str(e)}


def handle_query(q: str):
    q = q.lower()

    # Example question type: total sales
    if "total sales of" in q:
        product = q.split("total sales of")[1].split("in")[0].strip().capitalize()
        city = q.split("in")[1].split("?")[0].strip().title()
        data = df[(df["product"] == product) & (df["city"] == city)]
        return data["sales"].sum()

    # Example question type: number of sales reps in region
    if "how many sales reps" in q:
        region = q.split("in")[1].split("?")[0].strip().title()
        data = df[df["region"] == region]
        return data["rep"].nunique()

    # Add other question type handlers here...

    return "Question not supported yet"

