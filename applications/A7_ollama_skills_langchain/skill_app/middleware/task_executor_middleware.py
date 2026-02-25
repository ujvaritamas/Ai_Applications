"""
Task Executor Middleware - Second stage of two-stage architecture.

This middleware ONLY provides domain tools (calculator, kubectl_exec, etc.)
No skill management tools - those are handled by the first stage.
"""

from langchain.agents.middleware import AgentMiddleware
import tools


class TaskExecutorMiddleware(AgentMiddleware):
    """
    Middleware for the second-stage task executor.

    This agent receives:
    - User's original query
    - Loaded skill content with instructions
    - Access to domain tools only

    It does NOT have access to skill management tools.
    """

    # Only domain tools, no skill management
    tools = [
        tools.calculator,
        tools.unit_converter,
        tools.kubectl_exec,
        tools.file_reader,
        tools.web_search,
    ]

    def __init__(self):
        """Initialize the task executor middleware."""
        pass  # No special initialization needed
