# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2025-12-28

### Added
- Initial release with CLI and Streamlit UI
- JSON spec → essay generation pipeline
- Compliance checking (PII, prompt injection, banned words, factual claims)
- Support for MockProvider (testing) and OpenAIProvider (production)
- Token budgeting based on reading time with configurable overrides
- Finish reason and usage tracking in metadata
- Policy-driven banned words with configurable lists

### Fixed
- Improved token budgeting to prevent truncation (2min→600, 5min→1400, 10min→2800 tokens)
- Removed "harmful" from default banned words (too common in legitimate contexts)
- Enhanced compliance reports with policy source information

### Changed
- Provider interface now returns tuple (essay_text, metadata) for better observability
- Meta.json includes finish_reason and usage statistics

