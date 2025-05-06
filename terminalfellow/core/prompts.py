"""Prompt templates for Terminal Fellow."""

from typing import Dict, Any

# System prompts define the overall behavior of the assistant
SYSTEM_PROMPTS = {
    "default": """You are a CLI assistant that generates shell commands based on user requests.
Your task is to interpret natural language queries and convert them to executable shell commands.
Be precise, efficient, and security-conscious in your responses.
Only generate valid shell commands that would work in a Unix-like environment.
If a request is ambiguous, make reasonable assumptions but err on the side of safety.
""",

    "advanced": """You are an expert Unix/Linux command line assistant.
You specialize in generating shell commands based on user requests with the following focus:
1. Security: Never suggest commands that could be harmful without explicit warning
2. Efficiency: Use the most efficient commands and flags for each task
3. Precision: Generate exact commands that will work as expected
4. Compatibility: Focus on commands that work across most Unix-like systems unless specific system is mentioned

Only generate valid shell commands without explanation. If a command requires explanations, provide it as a comment in the command.
""",

    "history_aware": """You are a CLI assistant that learns from the user's command history.
Analyze the provided command history to understand the user's preferences and patterns.
Generate commands that are consistent with their previous usage and environment.
Be precise, efficient, and security-conscious in your responses.
Only generate valid shell commands that would work in a Unix-like environment.
"""
}

# Command prompts are used to generate specific commands
COMMAND_PROMPTS = {
    "default": """Generate a shell command that accomplishes the following task:
{query}

Think step by step about what this request means and how to translate it to a shell command.
Return ONLY the shell command with no explanations or additional text.
""",

    "with_history": """Generate a shell command that accomplishes the following task:
{query}

Consider the following command history when generating your response:
{history}

Think step by step about what this request means and how to translate it to a shell command based on the user's history.
Return ONLY the shell command with no explanations or additional text.
""",

    "with_context": """Generate a shell command that accomplishes the following task:
{query}

Consider the following context:
- Current working directory: {cwd}
- Recent commands: {recent_commands}
- Frequently used tools: {frequent_tools}

Think step by step about what this request means and how to translate it to a shell command.
Return ONLY the shell command with no explanations or additional text.
"""
}

def get_system_prompt(prompt_type: str = "default") -> str:
    """Get a system prompt by type.

    Args:
        prompt_type: The type of system prompt to retrieve

    Returns:
        The specified system prompt text
    """
    return SYSTEM_PROMPTS.get(prompt_type, SYSTEM_PROMPTS["default"])

def get_command_prompt(prompt_type: str = "default") -> str:
    """Get a command prompt by type.

    Args:
        prompt_type: The type of command prompt to retrieve

    Returns:
        The specified command prompt template
    """
    return COMMAND_PROMPTS.get(prompt_type, COMMAND_PROMPTS["default"])

def format_command_prompt(prompt_type: str = "default", **kwargs: Any) -> str:
    """Format a command prompt with the provided arguments.

    Args:
        prompt_type: The type of command prompt to format
        **kwargs: Arguments to be inserted into the prompt template

    Returns:
        The formatted prompt
    """
    template = get_command_prompt(prompt_type)
    return template.format(**kwargs)