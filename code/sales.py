import os

import duckdb
import pandas as pd
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

load_dotenv(".env_vars")

data_path = os.environ["SALES_DATA_PATH"]
data = pd.read_parquet(data_path)

duckdb.sql("CREATE TABLE sales AS SELECT * FROM data")


@tool
def run_query(query: str):
    """Run a duckdb SQL query on the sales table."""
    print(f"Query: {query}")
    try:
        return duckdb.sql(query).fetchdf().to_string()
    except Exception as e:
        return f"Error: {e}"


INSTRUCTIONS = f"""\
You are a Senior Data Analyst and a SQL Expert.
You have access to a duckdb database with a table called 'sales' that contains sales data.
The sales table has the following columns: {", ".join(data.columns)}.
Analyze the user input and translate it into valid SQL queries to perform the requested data operations.
Your output should be a detailed report based on the data.
"""

llm = ChatOpenAI()
agent = create_react_agent(
    model=llm,
    tools=[run_query],
    prompt=INSTRUCTIONS,
    checkpointer=MemorySaver(),
)

if __name__ == "__main__":
    print("Welcome to the SQL Data Analyst Agent!")
    print("You can ask me any question about the sales data.")
    print("Type 'exit', 'quit', or 'bye' to exit the program.")
    while True:
        question = input("> ").strip()
        if not question:
            continue
        if question.lower() in ["exit", "quit", "bye"]:
            break
        messages = agent.invoke(
            {"messages": [question]}, config={"configurable": {"thread_id": "1234"}}
        )["messages"]
        print(messages[-1].content)
