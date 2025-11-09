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
def query(response: Response, q: str = Query(None)):
    response.headers["X-Email"] = "23f2003519@ds.study.iitm.ac.in"
    
    if q is None:
        return {"answer": "Please provide a question using the 'q' parameter."}
    
    try:
        answer = handle_query(q)
        return {"answer": answer}
    except Exception as e:
        return {"error": str(e)}





def handle_query(q: str):
    q = q.lower().strip()

    # 1️⃣ Total sales query
    if "total sales of" in q:
        product = q.split("total sales of")[1].split("in")[0].strip().capitalize()
        city = q.split("in")[1].replace("?", "").strip().title()
        data = df[(df["product"] == product) & (df["city"] == city)]
        return int(data["sales"].sum())

    # 2️⃣ Number of sales reps query
    if "how many sales reps" in q:
        region = q.split("in")[1].replace("?", "").strip().title()
        data = df[df["region"] == region]
        return int(data["rep"].nunique())

    return "Question not supported yet"

