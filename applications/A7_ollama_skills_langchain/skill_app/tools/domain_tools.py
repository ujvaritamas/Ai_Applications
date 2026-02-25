"""Domain-specific tools that skills can use."""

from langchain.tools import tool
import subprocess


@tool
def calculator(expression: str) -> str:
    """Evaluates a mathematical expression safely.

    Args:
        expression: A mathematical expression to evaluate (e.g., "5 + 3 * 2")

    Returns:
        The result of the calculation as a string

    Examples:
        calculator("5 + 3") -> "8"
        calculator("240 * 0.15") -> "36.0"
        calculator("(100 - 20) / 4") -> "20.0"
    """
    try:
        # Use eval with limited scope for safety
        # In production, use a proper math parser like sympy
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {str(e)}"


@tool
def unit_converter(value: float, from_unit: str, to_unit: str) -> str:
    """Converts values between different units.

    Args:
        value: The numeric value to convert
        from_unit: The source unit (e.g., "miles", "kg", "celsius")
        to_unit: The target unit (e.g., "km", "lbs", "fahrenheit")

    Returns:
        The converted value with unit

    Supported conversions:
    - Length: miles, km, feet, meters, inches, cm
    - Weight: kg, lbs, oz, grams
    - Temperature: celsius, fahrenheit
    """
    # Conversion factors
    conversions = {
        # Length
        ("miles", "km"): 1.60934,
        ("km", "miles"): 0.621371,
        ("feet", "meters"): 0.3048,
        ("meters", "feet"): 3.28084,
        ("inches", "cm"): 2.54,
        ("cm", "inches"): 0.393701,

        # Weight
        ("kg", "lbs"): 2.20462,
        ("lbs", "kg"): 0.453592,
        ("oz", "grams"): 28.3495,
        ("grams", "oz"): 0.035274,
    }

    from_unit = from_unit.lower()
    to_unit = to_unit.lower()

    # Handle temperature separately
    if from_unit == "celsius" and to_unit == "fahrenheit":
        result = (value * 9/5) + 32
        return f"{value} °C = {result:.2f} °F"
    elif from_unit == "fahrenheit" and to_unit == "celsius":
        result = (value - 32) * 5/9
        return f"{value} °F = {result:.2f} °C"

    # Handle other conversions
    key = (from_unit, to_unit)
    if key in conversions:
        result = value * conversions[key]
        return f"{value} {from_unit} = {result:.2f} {to_unit}"
    else:
        return f"Conversion from {from_unit} to {to_unit} is not supported"


@tool
def kubectl_exec(command: str, namespace: str = "default") -> str:
    """Executes a kubectl command and returns the result.

    Args:
        command: The kubectl subcommand and arguments (e.g., "get pods", "describe pod my-pod")
        namespace: The Kubernetes namespace to use (default: "default")

    Returns:
        The output from the kubectl command

    Examples:
        kubectl_exec("get pods") -> List of pods in default namespace
        kubectl_exec("get pods", "kube-system") -> List of pods in kube-system
        kubectl_exec("describe deployment my-app") -> Details about my-app deployment

    Safety:
        - Read-only commands are encouraged (get, describe, logs)
        - Write operations (delete, apply) should be confirmed with user first
    """
    try:
        # Build the full command
        cmd = ["kubectl"]

        # Add namespace if not in the command already
        if "-n" not in command and "--namespace" not in command and namespace != "default":
            cmd.extend(["-n", namespace])

        # Add the user's command
        cmd.extend(command.split())

        # Execute the command
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            return f"Error: {result.stderr}"

        return result.stdout

    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 30 seconds"
    except Exception as e:
        return f"Error executing kubectl command: {str(e)}"


@tool
def file_reader(file_path: str) -> str:
    """Reads the contents of a file.

    Args:
        file_path: Path to the file to read

    Returns:
        The contents of the file as a string
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        return f"Error: File not found: {file_path}"
    except Exception as e:
        return f"Error reading file: {str(e)}"


@tool
def web_search(query: str, num_results: int = 5) -> str:
    """Simulates a web search (placeholder for actual implementation).

    Args:
        query: The search query
        num_results: Number of results to return (default: 5)

    Returns:
        Search results as formatted text

    Note:
        In a real implementation, this would call a search API like Google, Bing, or DuckDuckGo.
        For now, it's a placeholder that returns mock data.
    """
    return f"""Web search results for: "{query}"

[This is a placeholder. Integrate with actual search API]

To implement:
1. Use Google Custom Search API
2. Use SerpAPI
3. Use DuckDuckGo API
4. Or integrate with LangChain's search tools
"""
