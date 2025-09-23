from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain import hub
from langgraph.prebuilt import create_react_agent
from app.db import db
from app.llm import llm
import asyncio

# Toolkit (SQL agent tools)
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# Pull base system prompt from LangChain hub
prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")

# Use PostgreSQL dialect here (not SQLite!)
system_prompt = prompt_template.format(dialect="PostgreSQL", top_k=5)

# Create LangGraph ReAct Agent
agent_executor = create_react_agent(
    llm,
    toolkit.get_tools(),
    prompt=system_prompt,
)


async def run_sql_agent_stream(query: str, typing_delay: float = 0.03):
    """
    Stream agent response with typing delay effect.
    
    Args:
        query: User query string
        typing_delay: Delay in seconds between tokens (default: 0.03s = 30ms)
    """

    async for event in agent_executor.astream_events(
        {"messages": [{"role": "user", "content": query}]},
        version="v2",
    ):
        event_type = event["event"]

        # ---- LLM Streaming ----
        if event_type == "on_chat_model_stream":
            token = event["data"]["chunk"].content
            if token:
                # AI message piece
                yield {"type": "token", "content": token,"run_id":event["run_id"]}
                # apply typing delay only for token chunks
                if typing_delay and typing_delay > 0:
                    await asyncio.sleep(typing_delay)

        # ---- Tool Start ----
        elif event_type == "on_tool_start":
            tool_name = event["name"]
            input_data = event.get("data", {}).get("input")
            yield{
                "type": "tool_start",
                "tool": tool_name,
                "input": input_data,
                "run_id":event["run_id"]
            }

        # ---- Tool End ----
        elif event_type == "on_tool_end":
            tool_name = event["name"]
            output_data = event.get("data", {}).get("output").content
            yield{
                "type": "tool_end",
                "tool": tool_name,
                "output": output_data,
                "run_id":event["run_id"]
            }
        # no global delay for non-token events