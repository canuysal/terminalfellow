"""Command generation module for Terminal Fellow."""

from typing import Optional, Dict, Any, List
import os
import sys

from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.core.prompts import PromptTemplate

from terminalfellow.core import prompts
from terminalfellow.utils.config import get_openai_api_key, get_config_value


class CommandGenerator:
    """Generate commands based on natural language requests."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the command generator.

        Args:
            config: Optional configuration parameters
        """
        self.config = config or {}
        self.prompt_type = self.config.get("prompt_type", "default")
        self._setup_llm()

    def _setup_llm(self):
        """Set up the LLM for command generation."""
        system_prompt = self.config.get(
            "system_prompt", prompts.get_system_prompt(self.prompt_type)
        )

        # Get OpenAI API key from config or environment
        api_key = self.config.get("openai_api_key") or get_openai_api_key()

        # Get the model from config or default to gpt-3.5-turbo
        model = self.config.get("model") or get_config_value("model", "gpt-3.5-turbo")

        if api_key:
            # Set the API key in the environment
            os.environ["OPENAI_API_KEY"] = api_key

            try:
                # Try to use OpenAI if API key is available
                self.llm = OpenAI(
                    model=model,
                    temperature=0.1,
                    system_prompt=system_prompt,
                    api_key=api_key,
                )
                Settings.llm = self.llm
                self.using_openai = True
                return
            except Exception as e:
                # Display error and exit instead of falling back to templates
                print(f"Error initializing OpenAI API: {e}", file=sys.stderr)
                print(
                    "Please check your API key and internet connection.",
                    file=sys.stderr,
                )
                sys.exit(1)
        else:
            print(
                "No OpenAI API key found. Please run 'tfa --config' to set up your configuration.",
                file=sys.stderr,
            )
            sys.exit(1)

    def generate(self, query: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Generate a command based on the natural language query.

        Args:
            query: Natural language request for a command
            context: Optional context information (history, current directory, etc.)

        Returns:
            A shell command that satisfies the request
        """
        context = context or {}
        prompt_args = {"query": query, **context}

        # Determine which prompt to use based on available context
        if "history" in context and context["history"]:
            prompt_type = "with_history"
        elif all(k in context for k in ["cwd", "recent_commands", "frequent_tools"]):
            prompt_type = "with_context"
        else:
            prompt_type = self.prompt_type

        try:
            # Use LlamaIndex with OpenAI
            prompt_text = prompts.format_command_prompt(prompt_type, **prompt_args)
            prompt = PromptTemplate(prompt_text)
            response = self.llm.complete(prompt_text)
            return response.text.strip()
        except Exception as e:
            # Return error as command
            return f"echo 'Error generating command: {str(e)}'"
