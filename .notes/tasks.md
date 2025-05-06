# Terminal Fellow Tasks

## 1. Project Setup
- [x] Create project structure
- [x] Set up development environment
- [x] Initialize git repository
- [x] Create README.md with installation and usage instructions
- [x] Set up Python virtual environment, use conda and python=3.12
- [x] Configure linting and code formatting

## 1.5 Proof of Concept
- [x] Install and configure LlamaIndex
- [x] Design prompt templates
- [x] Command generation
- [x] Create a PoC one-liner generator python script without history.

## 2. Shell History Integration
- [x] Develop shell history reader
  - [x] Bash history parser
  - [ ] Zsh history parser (optional)
  - [ ] Fish history parser (optional)
- [x] Create history data model

## 3. Vector Database Implementation
- [ ] Set up ChromaDB
- [ ] Design embedding schema
- [ ] Create command embedding pipeline
- [ ] Implement storage and retrieval mechanisms
- [ ] Develop context-based query system

## 4. RAG Integration
- [ ] Create RAG pipeline
  - [ ] Query preprocessing
  - [ ] Context retrieval
  - [ ] Command generation
- [ ] Implement response formatting

## 5. CLI Development
- [x] Create command-line interface
- [x] Implement natural language request parser
- [x] Develop command suggestion mechanism
- [x] Add command execution functionality
- [x] Create configuration management
- [x] Improve UX for simpler command usage
- [x] Add interactive configuration
- [x] Implement spinner and clean output formatting

## 6. Installation & Packaging
- [x] Create setup.py for packaging
- [x] Implement system-wide command installation
- [x] Develop user configuration system
- [x] Create installation documentation

## 7. Testing & Quality Assurance
- [ ] Write unit tests
- [ ] Create integration tests
- [ ] Implement end-to-end testing
- [ ] Performance testing
- [ ] User acceptance testing

## 8. Documentation
- [x] Create user guide
- [ ] Develop API documentation
- [x] Write developer setup instructions
- [x] Create usage examples

## 9. Continuous Integration
- [ ] Set up CI/CD pipeline
- [ ] Implement automatic testing
- [ ] Create release workflow

## 10. Future Enhancements
- [ ] Multi-shell support expansion
- [ ] Command explanation feature
- [ ] Command history visualization
- [ ] Custom command templates
- [ ] User feedback system


## Edge Cases
- [x] Prevent loop calls for unattended terminals
- [x] Remove template based fallback mode on no llm key
- [ ] Add --explain mode.
- [ ] Edit help menu.
