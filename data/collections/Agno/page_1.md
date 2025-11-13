[Skip to main content](https://docs.agno.com/introduction#content-area)

[Agno home page![light logo](https://mintcdn.com/agno-v2/yeT29TzCG5roT0hQ/logo/black.svg?fit=max&auto=format&n=yeT29TzCG5roT0hQ&q=85&s=a6afd99095eb38a8797b215b10a4944d)![dark logo](https://mintcdn.com/agno-v2/yeT29TzCG5roT0hQ/logo/white.svg?fit=max&auto=format&n=yeT29TzCG5roT0hQ&q=85&s=dd3d606ef000b66252d19edf387dc7fc)](https://docs.agno.com/)

Search...

Ctrl K

Search...

Navigation

Introduction

What is Agno?

[Documentation](https://docs.agno.com/introduction) [AgentOS](https://docs.agno.com/agent-os/introduction) [Examples](https://docs.agno.com/examples/introduction) [Deploy](https://docs.agno.com/deploy/introduction) [Reference](https://docs.agno.com/reference/agents/agent) [FAQs](https://docs.agno.com/faq/environment-variables)

Use it to build multi-agent systems with memory, knowledge, human in the loop and MCP support. You can orchestrate agents as multi-agent teams (more autonomy) or step-based agentic workflows (more control).Here’s an example of an Agent that connects to an MCP server, manages conversation state in a database, and is served using a FastAPI application that you can interact with using the [AgentOS UI](https://os.agno.com/).

agno\_agent.py

Copy

Ask AI

```
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.anthropic import Claude
from agno.os import AgentOS
from agno.tools.mcp import MCPTools

# ************* Create Agent *************
agno_agent = Agent(
    name="Agno Agent",
    model=Claude(id="claude-sonnet-4-5"),
    db=SqliteDb(db_file="agno.db"),
    tools=[MCPTools(transport="streamable-http", url="https://docs.agno.com/mcp")],
    add_history_to_context=True,
    markdown=True,
)

# ************* Create AgentOS *************
agent_os = AgentOS(agents=[agno_agent])
app = agent_os.get_app()

# ************* Run AgentOS *************
if __name__ == "__main__":
    agent_os.serve(app="agno_agent:app", reload=True)
```

## [​](https://docs.agno.com/introduction\#what-is-the-agentos%3F)  What is the AgentOS?

AgentOS is a high-performance runtime for multi-agent systems. Key features include:

1. **Pre-built FastAPI runtime**: AgentOS ships with a ready-to-use FastAPI app for orchestrating your agents, teams, and workflows. This gives you a major head start in building your AI product.
2. **Integrated Control Plane**: The [AgentOS UI](https://os.agno.com/) connects directly to your runtime, letting you test, monitor, and manage your system in real time. This gives you unmatched visibility and control over your system.
3. **Private by Design**: AgentOS runs entirely in your cloud, ensuring complete data privacy. No data ever leaves your system. This is ideal for security-conscious enterprises.

Here’s what the [AgentOS UI](https://os.agno.com/) looks like in action:

## [​](https://docs.agno.com/introduction\#the-complete-agentic-solution)  The Complete Agentic Solution

For companies building agents, Agno provides the complete solution:

- The fastest framework for building agents, multi-agent teams and agentic workflows.
- A ready-to-use FastAPI app that gets you building AI products on day one.
- A control plane for testing, monitoring and managing your system.

We bring a novel architecture that no other framework provides, your AgentOS runs securely in your cloud, and the control plane connects directly to it from your browser. You don’t need to send data to any external services or pay retention costs, you get complete privacy and control.

## [​](https://docs.agno.com/introduction\#getting-started)  Getting started

If you’re new to Agno, follow the [quickstart](https://docs.agno.com/introduction/quickstart) to build your first Agent and run it using the AgentOS.After that, checkout the [examples gallery](https://docs.agno.com/examples/introduction) and build real-world applications with Agno.

If you’re looking for Agno 1.0 docs, please visit [docs-v1.agno.com](https://docs-v1.agno.com/).We also have a [migration guide](https://docs.agno.com/how-to/v2-migration) for those coming from Agno 1.0.

Was this page helpful?

YesNo

[Quickstart](https://docs.agno.com/introduction/quickstart)

Ctrl+I

Assistant

Responses are generated using AI and may contain mistakes.