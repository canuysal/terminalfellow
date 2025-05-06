# Terminal Fellow

## Project Description
Terminal Fellow is a CLI tool that understands your command line history and generates commands or scripts based on natural language requests. It serves as an intelligent terminal assistant that can interpret contextual instructions and convert them to executable commands.

## Core Functionality
- Parse natural language requests to generate relevant terminal commands
- Analyze user's command history to understand context and preferences
- Generate one-liners or scripts based on the request and historical usage patterns
- Understand and reference project structures and common workflows

## Example
**User Input:**
`tfa go to my last project and start the web server`

**Generated Command:**
`cd ~/myfs/codes/latestprojectiwasworkingonbasedonbashhistory && npm run dev`

## Technical Stack
- **Language**: Python
- **Vector Store**: ChromaDB for RAG implementation
- **LLM Framework**: LlamaIndex for context-aware command generation
- **Installation**: System-wide command (`tfa`)

## Project Roadmap
1. **Setup & Core Architecture**
   - Project structure and development environment
   - Command parsing mechanism
   - A simple proof of concept one-liner generator without history.

2. **Knowledge Base Development**
   - History analysis utilities
   - Shell history integration
   - Command embedding and storage in ChromaDB
   - Context retrieval system

3. **Command Generation Engine**
   - LlamaIndex RAG implementation
   - Command templating and generation
   - Context-aware response formatting

4. **Installation & Distribution**
   - CLI wrapper
   - System-wide installation process
   - Configuration options

5. **Testing & Refinement**
   - Accuracy testing
   - Performance optimization
   - User feedback integration

## Current Status
As of the proof of concept implementation, we have:
1. Created a modular project structure with separation of concerns
2. Set up a conda environment with Python 3.12
3. Implemented LlamaIndex-based command generation
4. Created a sophisticated command-line interface with Typer and Rich
5. Developed a template-based fallback when API keys aren't available
6. Implemented basic shell history analysis with frequency tracking
7. Added configuration management system for API keys and settings
8. Set up comprehensive testing infrastructure

## Next Steps
1. Implement ChromaDB integration for vector storage
2. Enhance history analysis with more sophisticated pattern detection
3. Add support for multiple shell types (zsh, fish)
4. Implement RAG pipeline with command history as context
5. Expand test coverage for edge cases





