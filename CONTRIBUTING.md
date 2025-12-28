# Contributing

Thank you for your interest in contributing to this project!

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/form-to-essay.git`
3. Create a virtual environment: `python -m venv .venv`
4. Activate it: `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (macOS/Linux)
5. Install in editable mode: `pip install -e .`
6. Run tests: `pytest`

## Development Guidelines

### Code Style
- Follow PEP 8
- Use type hints where helpful
- Add docstrings for public functions/classes

### Testing
- All tests must pass: `pytest`
- Add tests for new features
- Keep tests deterministic (use MockProvider for LLM-dependent tests)

### Commits
- Write clear commit messages
- **Never commit secrets** (API keys, tokens, etc.)
- Ensure `.env` files are never tracked

### Pull Requests
- Open PRs against `main` branch
- Describe what changes and why
- Ensure CI passes
- Keep PRs focused and reasonably sized

## What to Contribute

**Welcome:**
- Bug fixes
- Documentation improvements
- Additional example specs
- Test coverage improvements
- Small UX enhancements to Streamlit UI

**Please Discuss First:**
- Major architectural changes
- New dependencies
- Breaking changes to the spec→artifacts contract

## Questions?

Open an issue for questions or discussions. This is a reference/demo repo, so contributions should align with keeping it a clean, educational artifact.

