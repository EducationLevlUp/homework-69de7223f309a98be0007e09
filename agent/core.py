"""Agent core module: creates and configures the deep research agent."""

from deepagents import StateBackend, create_deep_agent
from langchain_core.messages import HumanMessage

from config.settings import get_llm_model
from tools.search import create_search_tool


SYSTEM_PROMPT = """You are a deep research assistant. You can search the internet for information
and create, read, and manage virtual files.

When the user asks a question:
1. Use the internet_search tool to find relevant information.
2. Summarize findings and optionally save them to virtual files using write_file.
3. You can list, read, and edit virtual files as needed.
4. Be thorough and cite sources when possible.

Virtual files are stored in memory and will be exported to the real filesystem
when the session ends."""


def create_agent():
    """Create and return a compiled deep agent with search and filesystem tools.

    Returns:
        A compiled LangGraph state graph ready for .invoke() or .stream().
    """
    # Create the search tool
    search_tool = create_search_tool()

    # Create the agent with StateBackend (in-memory virtual filesystem)
    agent = create_deep_agent(
        model=get_llm_model(),
        tools=[search_tool],
        backend=StateBackend(),
        system_prompt=SYSTEM_PROMPT,
    )

    return agent


def run_agent(agent, user_query: str, thread_id: str):
    """Run the agent with a user query and return the final state.

    Args:
        agent: Compiled LangGraph agent.
        user_query: The user's question or command.
        thread_id: Session identifier for state persistence.

    Returns:
        The final agent state after processing the query.
    """
    config = {"configurable": {"thread_id": thread_id}}
    messages = [HumanMessage(content=user_query)]

    response = agent.invoke({"messages": messages}, config=config)
    return response
