# Contributing

Thanks for contributing to Hermes Figma Prompt Hub!

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git

### Setup

1. **Fork the repository**
   - Click the "Fork" button on GitHub
   - Clone your fork locally:
     ```bash
     git clone https://github.com/YOUR_USERNAME/hermes-figma-prompt-hub.git
     cd hermes-figma-prompt-hub
     ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify your setup**
   ```bash
   python scripts/validate_repo.py
   ```

### Making Changes

1. **Create a branch for your changes**
   ```bash
   git checkout -b your-feature-name
   ```

2. **Make your changes**
   - Keep changes focused on a single issue
   - Follow existing code style
   - Add tests if applicable

3. **Run validation**
   ```bash
   python scripts/validate_repo.py
   python scripts/check_figma_contract.py
   ```

4. **Commit and push**
   ```bash
   git add .
   git commit -m "Description of your changes"
   git push origin your-feature-name
   ```

5. **Open a Pull Request**
   - Provide a clear description of your changes
   - Reference any related issues
   - Keep PRs focused on a single change

## Development Workflow

### Prompt Validation

To validate a prompt file:
```bash
python scripts/validate_prompt.py prompts/raw/your-prompt.json
```

### Figma Contract Check

To check Figma contract compliance:
```bash
python scripts/check_figma_contract.py
```

### Prompt Catalog

To regenerate the prompt catalog:
```bash
python scripts/generate_prompt_catalog.py
```

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to new functions
- Keep functions focused and concise

## Reporting Issues

- Use GitHub Issues for bug reports and feature requests
- Include steps to reproduce for bugs
- Provide environment details when relevant

## Getting Help

- Check existing documentation in `docs/`
- Review `COLLABORATION.md` for collaboration guidelines
- Ask questions in GitHub Discussions
