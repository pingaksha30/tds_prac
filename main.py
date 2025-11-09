from fastapi import FastAPI, Query, Response
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

df = pd.read_json("data.json")

@app.get("/query")
def query(response: Response, q: str = Query(None)):
    email = "23f2003519@ds.study.iitm.ac.in"
    response.headers["X-Email"] = email
    
    if not q:
        return {"answer": "Please provide a question using the 'q' parameter.", "email": email}
    
    try:
        answer = handle_query(q)
        return {"answer": answer, "email": email}
    except Exception as e:
        return {"error": str(e), "email": email}


def handle_query(q: str):
    q = q.lower().strip()

    if "total sales of" in q:
        product = q.split("total sales of")[1].split("in")[0].strip().capitalize()
        city = q.split("in")[1].replace("?", "").strip().title()
        data = df[(df["product"] == product) & (df["city"] == city)]
        return int(data["sales"].sum())

    if "how many sales reps" in q:
        region = q.split("in")[1].replace("?", "").strip().title()
        data = df[df["region"] == region]
        return int(data["rep"].nunique())

    return "Question not supported yet"
