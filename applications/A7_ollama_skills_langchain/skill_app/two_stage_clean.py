"""
Improved Two-Stage Skill Agent.

This is the cleanest implementation of the two-stage architecture.
"""

from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from middleware.middleware import SkillMiddleware
from middleware.task_executor_middleware import TaskExecutorMiddleware


class TwoStageSkillAgent:
    """
    Two-stage agent architecture:

    Stage 1 (Skill Router):
      - Input: User query
      - Tools: load_skill, list_skill
      - Output: Skill content

    Stage 2 (Task Executor):
      - Input: User query + Skill content
      - Tools: calculator, unit_converter, kubectl_exec, etc.
      - Output: Final answer
    """

    def __init__(self, model_name: str = "llama3.1:8b", temperature: float = 0):
        """Initialize both stages."""

        # Stage 1: Skill Router
        # Only has skill management tools
        self.skill_router = create_agent(
            ChatOllama(model=model_name, temperature=temperature),
            system_prompt=(
                "You are a skill router. Your job is to:\n"
                "1. Read the user's query\n"
                "2. Identify which skill best matches their need\n"
                "3. Call load_skill(skill_name) to load that skill\n\n"
                "Do NOT try to answer the question yourself.\n"
                "Just load the appropriate skill."
            ),
            middleware=[SkillMiddleware()],
        )

        # Stage 2: Task Executor
        # Only has domain tools
        self.task_executor = create_agent(
            ChatOllama(model=model_name, temperature=temperature),
            system_prompt=(
                "You are a task executor. You will receive:\n"
                "1. The user's original query\n"
                "2. Skill instructions that guide you\n\n"
                "Follow the skill instructions to use the available tools correctly.\n"
                "The skill tells you which tools to use and how to format parameters."
            ),
            middleware=[TaskExecutorMiddleware()],
        )

    def invoke(self, user_query: str, verbose: bool = True) -> dict:
        """
        Execute the two-stage process.

        Args:
            user_query: The user's question
            verbose: Print debug information

        Returns:
            dict with 'answer', 'skill_used', 'stage1_messages', 'stage2_messages'
        """

        if verbose:
            print("\n" + "=" * 60)
            print("STAGE 1: Skill Routing")
            print("=" * 60)

        # Stage 1: Route to appropriate skill
        stage1_result = self.skill_router.invoke({
            "messages": [{
                "role": "user",
                "content": user_query
            }]
        })

        # Extract skill content from Stage 1
        skill_content = None
        skill_name = None

        for message in stage1_result["messages"]:
            if hasattr(message, 'type') and message.type == "tool":
                skill_content = message.content
                # Try to extract skill name from content
                if "Loaded skill:" in skill_content:
                    skill_name = skill_content.split("Loaded skill:")[1].split("\n")[0].strip()
                break

        if not skill_content:
            return {
                "answer": "Error: Could not load appropriate skill",
                "skill_used": None,
                "stage1_messages": stage1_result["messages"],
                "stage2_messages": []
            }

        if verbose:
            print(f"\n✓ Loaded skill: {skill_name}")
            print(f"✓ Skill content: {len(skill_content)} characters")

            print("\n" + "=" * 60)
            print("STAGE 2: Task Execution")
            print("=" * 60)

        # Stage 2: Execute task with skill guidance
        enhanced_query = f"""Original Query: {user_query}

Skill Guidance:
{skill_content}

Instructions: Answer the user's original query above, following the skill guidance.
Use the available tools as instructed by the skill."""

        stage2_result = self.task_executor.invoke({
            "messages": [{
                "role": "user",
                "content": enhanced_query
            }]
        })

        # Extract final answer from Stage 2
        final_answer = None
        for message in reversed(stage2_result["messages"]):
            if hasattr(message, 'type') and message.type == "ai":
                final_answer = message.content
                break

        if verbose:
            print("\n✓ Task execution complete")

        return {
            "answer": final_answer or "Error: Could not generate response",
            "skill_used": skill_name,
            "stage1_messages": stage1_result["messages"],
            "stage2_messages": stage2_result["messages"]
        }


def main():
    """Test the two-stage agent."""

    print("\n" + "=" * 70)
    print("TWO-STAGE SKILL AGENT DEMONSTRATION")
    print("=" * 70)
    print("\nThis demonstrates a clean two-stage architecture:")
    print("  Stage 1: Skill Router (loads appropriate skill)")
    print("  Stage 2: Task Executor (uses tools with skill guidance)")

    agent = TwoStageSkillAgent()

    # Test 1: Math calculation
    print("\n\n" + "=" * 70)
    print("TEST 1: Mathematical Calculation")
    print("=" * 70)

    result = agent.invoke("What is 15% of 240?", verbose=True)

    print("\n" + "=" * 60)
    print("FINAL ANSWER:")
    print("=" * 60)
    print(result["answer"])

    # Test 2: Unit conversion
    print("\n\n" + "=" * 70)
    print("TEST 2: Unit Conversion")
    print("=" * 70)

    result = agent.invoke("Convert 10 miles to kilometers", verbose=True)

    print("\n" + "=" * 60)
    print("FINAL ANSWER:")
    print("=" * 60)
    print(result["answer"])

    # Test 3: Kubernetes query
    print("\n\n" + "=" * 70)
    print("TEST 3: Kubernetes Query")
    print("=" * 70)

    result = agent.invoke("How do I check if my pods are running?", verbose=True)

    print("\n" + "=" * 60)
    print("FINAL ANSWER:")
    print("=" * 60)
    print(result["answer"])

    print("\n" + "=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
