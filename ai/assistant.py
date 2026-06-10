from pathlib import Path

import pandas as pd


DATA_PATH = Path(__file__).resolve().parents[1] / "pipelines" / "data" / "customers.csv"


class AnalyticsAssistant:
    """Rule-based analytics assistant.

    Replace with LangChain + LLM + SQL agent in production.
    """

    def __init__(self, data_path: Path = DATA_PATH) -> None:
        self.customers = pd.read_csv(data_path, comment="#")
        self.customers["monthly_revenue"] = pd.to_numeric(self.customers["monthly_revenue"])
        self.customers["status"] = self.customers["status"].str.lower()

    def answer(self, question: str) -> str:
        q = question.lower()
        if "revenue" in q:
            revenue = self.customers["monthly_revenue"].sum()
            return f"Current monthly recurring revenue in the demo data is ${revenue:,.2f}."
        if "country" in q and ("highest" in q or "most" in q):
            top = self.customers["country"].value_counts().idxmax()
            count = self.customers["country"].value_counts().max()
            return f"{top} has the highest customer count with {count} customers."
        if "churn" in q:
            churn_rate = (self.customers["status"] == "churned").mean()
            return f"The churn rate in the demo data is {churn_rate:.1%}."
        if "active" in q:
            active = int((self.customers["status"] == "active").sum())
            return f"There are {active} active customers."
        return "I can answer questions about revenue, top countries, churn rate, and active customers."


if __name__ == "__main__":
    assistant = AnalyticsAssistant()
    examples = [
        "How much revenue do we have?",
        "Which country has the highest customers?",
        "What is the churn rate?",
    ]
    for item in examples:
        print(f"Q: {item}")
        print(f"A: {assistant.answer(item)}")
