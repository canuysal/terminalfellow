"""Command generation module for Terminal Fellow."""
from typing import Optional, Dict, Any, List
import os

from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.core.prompts import PromptTemplate

from terminalfellow.core import prompts
from terminalfellow.utils.config import get_openai_api_key

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
        # For now, we'll use a simple template-based approach
        # Later this will be enhanced with RAG using command history
        system_prompt = self.config.get("system_prompt",
                                       prompts.get_system_prompt(self.prompt_type))

        # Get OpenAI API key from config or environment
        api_key = self.config.get("openai_api_key") or get_openai_api_key()

        if api_key:
            # Set the API key in the environment
            os.environ["OPENAI_API_KEY"] = api_key

            try:
                # Try to use OpenAI if API key is available
                self.llm = OpenAI(
                    model="gpt-3.5-turbo",
                    temperature=0.1,
                    system_prompt=system_prompt,
                    api_key=api_key
                )
                Settings.llm = self.llm
                self.using_openai = True
                return
            except Exception as e:
                # Fall back to template-based responses for PoC
                print(f"Error initializing OpenAI: {e}")

        # If we get here, we couldn't initialize OpenAI
        self.using_openai = False
        print("Using template-based command generation (no valid OpenAI API key found)")

    def _get_command_template(self, query: str) -> str:
        """Get a command template based on the query."""
        # Simple mapping for PoC
        command_templates = {
            "list": "ls -la",
            "find": "find . -name '{}'",
            "search": "grep -r '{}' .",
            "directory": "cd {}",
            "create": "mkdir -p {}",
            "remove": "rm {}",
            "file": "cat {}",
            "process": "ps aux | grep {}",
            "install": "sudo apt-get install {}",
            "download": "wget {}",
            "compress": "tar -czvf {}.tar.gz {}",
            "extract": "tar -xzvf {}",
            "permission": "chmod {} {}",
            "network": "ping -c 4 {}",
            "system": "uname -a",
        }

        # Find the best matching template
        for key, template in command_templates.items():
            if key in query.lower():
                # Extract potential argument
                parts = query.lower().split(key, 1)
                if len(parts) > 1 and parts[1].strip():
                    # Try to extract a meaningful argument
                    arg = parts[1].strip().split()[0].strip('.,!? ')
                    return template.format(arg)
                return template.replace(" {}", "").replace("{}", "")

        # Default fallback
        return "echo 'Command not found for: {}'".format(query)

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

        if self.using_openai:
            try:
                # Use LlamaIndex with OpenAI
                prompt_text = prompts.format_command_prompt(prompt_type, **prompt_args)
                prompt = PromptTemplate(prompt_text)
                response = self.llm.complete(prompt_text)
                return response.text.strip()
            except Exception as e:
                # Fall back to template approach
                print(f"OpenAI API error: {e}")
                pass

        # Fallback to template-based approach for PoC
        return self._get_command_template(query)