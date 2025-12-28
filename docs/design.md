# Design Document

This document outlines the design decisions for the json-to-essay project.

## Architecture

The project follows a modular architecture with clear separation of concerns:

- **Schemas**: Pydantic models for data validation
- **Providers**: Abstract LLM provider interface with OpenAI and Mock implementations
- **Pipeline**: Core orchestration logic
- **Compliance**: Pre and post-generation checks
- **Eval**: Testing and evaluation utilities
- **Util**: Shared utilities for file operations, text processing, and logging

## Compliance Flow

1. Pre-checks on input spec (PII, prompt injection)
2. Essay generation via LLM provider
3. Post-checks on generated essay (banned words, PII, factual claims)
4. Report generation with status (pass/warn/block)

## Provider Strategy

- MockProvider: Deterministic output for testing
- OpenAIProvider: Production LLM calls
- Default to MockProvider if OPENAI_API_KEY not set

