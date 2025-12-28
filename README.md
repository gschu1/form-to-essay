> 🚧 **Reference/Demo Repo**  
> This repository is a demo/reference implementation. The hosted product adds storage, RAG, optimizers, and reliability layers.

# JSON to Essay

A client-safe demo project that demonstrates end-to-end LLM pipeline delivery: **structured input (JSON) → generated essay (Markdown) → compliance checks → auditable report + saved artifacts**.

## What It Does

This project generates well-structured essays from JSON specifications using LLM providers (OpenAI or mock), then runs compliance checks to ensure output quality and safety. It produces a complete audit trail with four core artifacts: the input spec, generated essay, compliance report, and metadata. The system includes both a CLI and a Streamlit UI, both calling the same core engine.

## Quickstart

### Installation

```bash
# Clone the repository
git clone https://github.com/gschu1/form-to-essay.git
cd form-to-essay

# Create virtual environment
python -m venv .venv

# Activate (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Activate (macOS/Linux)
source .venv/bin/activate

# Install dependencies
pip install -e .
```

### CLI Usage

```bash
# Generate an essay from a JSON spec
json-to-essay render examples/spec_min.json -o outputs/my_run

# Show help
json-to-essay --help
```

### Streamlit UI

```bash
# Launch the web interface
streamlit run ui/app.py
```

Then open your browser to `http://localhost:8501` and use the form to generate essays without writing JSON.

## What This Repo Is / Is Not

**This repo IS:**
- A CLI + Streamlit demo/reference implementation
- A stable spec→artifacts contract (input_spec.json, essay.md, compliance_report.json, meta.json)
- Provider abstraction (MockProvider, OpenAIProvider)
- Compliance checking framework (PII, prompt injection, banned words, factual claims)
- Complete test suite with examples

**This repo IS NOT:**
- A production service with user accounts or authentication
- A system with persistent storage or run history
- A RAG (Retrieval-Augmented Generation) implementation
- An optimization loop or multi-pass revision system
- A system with SLOs, monitoring, billing, or production hardening

## Why Open Source?

This repository serves as:
- **Portfolio artifact**: Demonstrates end-to-end LLM pipeline design, compliance thinking, and clean architecture
- **Reference implementation**: Shows how to structure a spec→essay→compliance pipeline
- **Learning resource**: Open code for studying LLM integration patterns, compliance checks, and provider abstraction

The hosted product (private repo) adds production features: authentication, persistent storage, RAG for facts mode, multi-pass optimizers, analytics, and reliability layers.

## Roadmap (Public vs Private)

**Public Repo (This Repository):**
- Keep spec→artifacts contract stable
- Small UX improvements to Streamlit UI
- Enhanced quality/compliance reports
- Template scaffolding (if useful for community)
- Additional example specs

**Private Product (Separate Repository):**
- Authentication and user management
- Persistent run history and storage
- RAG (Retrieval-Augmented Generation) for facts mode
- Multi-pass optimizers and revision loops
- Analytics dashboard and usage metrics
- Production hardening (SLOs, monitoring, alerting)
- Billing and subscription management

## Features

- **JSON Spec Input**: Define essay requirements via structured JSON
- **Essay Generation**: Generate well-structured essays using LLM providers (OpenAI or Mock)
- **Compliance Checking**: Pre and post-generation checks for PII, prompt injection, banned words, and factual claims
- **Audit Trail**: Complete artifacts saved for every run (spec, essay, compliance report, metadata)
- **CLI Interface**: Command-line tool for batch processing
- **Streamlit UI**: Interactive web interface for testing
- **Evaluation Runner**: Test multiple specs and generate compliance reports

## Project Structure

```
json-to-essay/
├── config/
│   └── policy.yaml          # Compliance policy configuration
├── docs/
│   ├── anchor.md           # Project anchor document
│   └── design.md           # Design documentation
├── examples/
│   ├── spec_min.json       # Minimal example spec
│   ├── spec_rich.json      # Rich example spec
│   └── spec_adversarial.json  # Adversarial test case
├── src/
│   └── json_to_essay/      # Main package
│       ├── cli.py           # CLI interface
│       ├── settings.py      # Configuration
│       ├── schemas/         # Pydantic models
│       ├── providers/       # LLM providers
│       ├── pipeline/        # Core pipeline logic
│       ├── compliance/      # Compliance checking
│       ├── eval/            # Evaluation utilities
│       └── util/            # Utility functions
├── tests/                   # Test suite
├── ui/
│   └── app_streamlit.py    # Streamlit UI
└── outputs/                 # Runtime output directory (gitignored)
```

## Installation

### Prerequisites

- Python 3.11 or higher
- pip or uv

### Setup

1. **Create a virtual environment:**

```bash
python -m venv .venv
```

2. **Activate the virtual environment:**

**On Windows (PowerShell or CMD):**
```bash
.venv\Scripts\activate
```

**On macOS/Linux:**
```bash
source .venv/bin/activate
```

> **Note:** Only run the command for your operating system. You'll know it worked when you see `(.venv)` at the start of your command prompt.

3. **Install dependencies:**

```bash
pip install -e .
```

Or with uv:
```bash
uv pip install -e .
```

4. **Configure environment (optional):**

Copy `.env.example` to `.env` and add your OpenAI API key if you want to use the OpenAI provider:

```bash
OPENAI_API_KEY=your_key_here
PROVIDER=openai
OPENAI_MODEL=gpt-4o-mini
```

**Environment Variables:**
- `OPENAI_API_KEY`: Your OpenAI API key (required for `PROVIDER=openai`)
- `PROVIDER`: Provider to use - `mock` (default) or `openai`
- `OPENAI_MODEL`: Model name for OpenAI (default: `gpt-4o-mini`)
- `OPENAI_MAX_OUTPUT_TOKENS`: Optional override for max output tokens (default: auto-calculated from reading time)

**Token Budgeting:**
The system automatically calculates `max_tokens` based on reading time:
- Short (2 min): ~600 tokens
- Medium (5 min): ~1400 tokens
- Long (10 min): ~2800 tokens

You can override this by setting `OPENAI_MAX_OUTPUT_TOKENS` in your `.env` file. If the output is truncated (finish_reason="length"), you'll see a warning in the UI and can increase this value.

**Banned Words Policy:**
The system uses a configurable banned words list from `config/policy.yaml`. By default, this is a heuristic flag list (warns but doesn't block) and includes only words that are rarely used in legitimate contexts. Common words like "harmful" are NOT included by default. You can customize the list in `config/policy.yaml` or add spec-specific banned words in your JSON spec.

If `PROVIDER=openai` is set but `OPENAI_API_KEY` is missing, the system will raise an error. If no provider is specified, the system will use the MockProvider by default.

## Usage

### CLI

**Show help and available commands:**

```bash
json-to-essay --help
```

**Render an essay from a JSON spec (using MockProvider):**

```bash
json-to-essay render examples/spec_min.json
```

**Render an essay using OpenAI (set PROVIDER=openai):**

```bash
# Windows PowerShell
$env:PROVIDER="openai"
json-to-essay render examples/spec_min.json -o outputs

# Or set in .env file and run:
json-to-essay render examples/spec_min.json -o outputs
```

**Specify output directory:**

```bash
json-to-essay render examples/spec_min.json -o outputs/my_run
```

**Show render command help:**

```bash
json-to-essay render --help
```

**Exit codes:**
- `0`: Success (pass or warn)
- `2`: Blocked due to compliance issues

### Streamlit UI (Local Demo)

**Launch the web interface:**

```bash
streamlit run ui/app.py
```

Then open your browser to the URL shown (typically `http://localhost:8501`).

**Windows PowerShell:**
```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run Streamlit
streamlit run ui/app.py
```

**macOS/Linux:**
```bash
# Activate virtual environment
source .venv/bin/activate

# Run Streamlit
streamlit run ui/app.py
```

**Features:**
- Form-based input (no JSON required)
- Real-time essay generation
- Compliance report display
- Download artifacts (essay, compliance report, or full run bundle as ZIP)

**Provider Configuration:**
- The UI uses the same provider settings as the CLI
- Set `PROVIDER=openai` and `OPENAI_API_KEY` in your `.env` file (in the repo root) to use OpenAI
- Defaults to `PROVIDER=mock` (no API key required)
- The UI shows current provider status without exposing API keys

### Evaluation Runner

**Run evaluation on all example specs:**

```bash
python -m json_to_essay.eval.runner
```

This will process all `spec_*.json` files in the `examples/` directory and print a summary table.

## Input Specification Format

The JSON spec must include:

**Required fields:**
- `language`: Language code (e.g., "en")
- `reading_time_minutes`: Target reading time (integer > 0)
- `topic`: Essay topic (string)
- `audience`: Target audience description (string)
- `style`: Style object (see below)
- `constraints`: Constraints object (see below)

**Optional fields:**
- `persona`: Writing persona (default: "reflective")
- `mode`: "reflective" or "facts" (default: "reflective")
- `sources`: List of source URLs (optional)

**Style object:**
```json
{
  "tone": ["contemplative", "gentle"],
  "register": "formal",
  "banned_words": ["word1", "word2"],
  "allowed_hedges": ["perhaps", "might"]
}
```

**Constraints object:**
```json
{
  "must_include": ["topic1", "topic2"],
  "must_avoid": ["topic3"]
}
```

See `examples/spec_min.json` for a complete example.

## Compliance Checks

The system performs the following checks:

### Pre-checks (on input spec):
- **PII Detection**: Email addresses, phone numbers
- **Prompt Injection**: Detection of common injection patterns

### Post-checks (on generated essay):
- **Banned Words**: Words from policy and spec
- **PII Detection**: PII in output
- **Factual Claims**: Strong claims without sources (especially in "facts" mode)

### Compliance Report

Every run produces a `compliance_report.json` with:
- `status`: "pass", "warn", or "block"
- `reasons`: List of issues found
- `checks`: Individual check results
- `actions_taken`: Actions performed
- `run_id`: Unique identifier

## Output Artifacts

Each run creates the following files in the output directory (this is the stable contract):

- `input_spec.json`: Copy of the input specification
- `essay.md`: Generated essay in Markdown
- `compliance_report.json`: Compliance check results (status, reasons, checks, actions_taken)
- `meta.json`: Run metadata (run_id, timestamp, model, duration, finish_reason, usage stats)

All artifacts are JSON (except `essay.md`) and can be parsed programmatically for audit trails or downstream processing.

## Testing

**Run all tests:**

```bash
pytest
```

**Run specific test file:**

```bash
pytest tests/test_spec_schema.py
```

**Run with coverage:**

```bash
pytest --cov=json_to_essay tests/
```

## Development

### Project Structure

- **Schemas** (`schemas/`): Pydantic models for validation
- **Providers** (`providers/`): LLM provider interfaces (OpenAI, Mock)
- **Pipeline** (`pipeline/`): Core orchestration logic
- **Compliance** (`compliance/`): Policy loading and check implementations
- **Eval** (`eval/`): Evaluation and testing utilities
- **Util** (`util/`): Shared utilities (files, text processing, logging)

### Adding a New Provider

1. Create a new class in `providers/` that inherits from `LLMProvider`
2. Implement the `generate_essay()` method
3. Update `pipeline/run.py` to support the new provider

### Extending Compliance Checks

1. Add check function in `compliance/checks.py`
2. Register in `compliance/router.py` (pre or post checks)
3. Update policy schema if needed

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**License Note:** The public demo code is permissive (MIT). The product value in the hosted service comes from proprietary reliability layers, optimization algorithms, and production infrastructure that live in a separate private repository.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. This is a reference/demo repo - contributions should align with keeping it a clean, educational artifact.

For production use, consider:
- Enhanced PII detection
- More sophisticated prompt injection detection
- RAG integration for facts mode
- Multi-iteration revision loops
- Additional compliance checks

