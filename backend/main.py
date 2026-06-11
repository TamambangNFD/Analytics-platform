from fastapi import FastAPI
from backend.database import get_connection
import pandas as pd


app = FastAPI(
    title="Analytics Platform API",
    version="1.0"
)



@app.get("/")
def home():

    return {

        "message":
        "Analytics API running",

        "status":
        "healthy"

    }



@app.get("/customers")
def customers():

    query = """

    SELECT *

    FROM raw.customers

    LIMIT 100

    """

    try:

        conn = get_connection()

        df = pd.read_sql(
            query,
            conn
        )


        return df.to_dict(
            orient="records"
        )


    except Exception as e:


        return {

            "error": str(e)

        }




@app.get("/revenue")
def revenue():


    query = """

    SELECT

    SUM(monthly_revenue)
    AS revenue

    FROM raw.customers

    """


    try:

        conn = get_connection()


        df = pd.read_sql(
            query,
            conn
        )


        return {

            "revenue":
            float(df.iloc[0]["revenue"])

        }


    except Exception:


        return {

            "revenue":0

        }