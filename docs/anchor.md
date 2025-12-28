# JSON → Essay (with Compliance Report): Anchor Doc

## Goal
Build a small, client-safe GenAI artifact that demonstrates end-to-end delivery:
**structured input (JSON) → generated essay (Markdown) → compliance checks → auditable report + saved artifacts.**

This is a portfolio-quality demo for roles like:
- GenAI Solutions Engineer
- Forward-Deployed Engineer (FDE)
- RAG/LLM App Engineer (with governance mindset)

## Product in one sentence
A CLI + simple web UI that turns a JSON brief into a reflective essay, then produces a **Compliance Report** explaining what passed/failed, what was flagged, and why.

## MVP scope (must ship fast)
1) Accept a JSON "Spec" describing topic, audience, tone, length.
2) Generate an essay in Markdown using an LLM provider.
3) Run a compliance router:
   - Pre-checks on the input Spec (PII, injection-ish content, unsafe intent).
   - Post-checks on the essay output (banned words, PII, strong factual claims without sources, disallowed categories).
4) Save artifacts to an output folder for every run:
   - input_spec.json
   - essay.md
   - compliance_report.json
   - meta.json (model, timings, run_id, checks triggered)
5) Provide a tiny eval runner that executes example specs and prints pass/fail summaries.

## Non-goals (for MVP)
- No multi-iteration revise loops.
- No perfect “Montaigne voice.”
- No full Retrieval-Augmented Generation (RAG) yet.
- No heavy deployment; local demo is enough.

## Why this matters (employer/stakeholder framing)
This repo proves:
- I can translate a spec into a working LLM pipeline.
- I can implement governance/guardrails as software (not vibes).
- I can produce audit-friendly artifacts and deterministic checks.
- I can build a clickable demo and a repeatable eval harness.

## Inputs: Spec JSON (v1)
Required fields:
- language: "en" | "he" | ...
- reading_time_minutes: integer (e.g., 5)
- topic: string
- audience: string (e.g., "educated general")
- style: object (tone, register, banned_words, allowed_hedges)
- constraints: object (must_include, must_avoid)

Optional fields:
- persona: string (default "reflective")
- mode: "reflective" | "facts" (facts mode is stricter)
- sources: list of strings (if provided, facts mode can be allowed)

## Outputs: Compliance Report (v1)
compliance_report.json should include:
- status: "pass" | "warn" | "block"
- reasons: list of reason objects {code, message, severity, evidence}
- actions_taken: list (e.g., "redacted_pii", "forced_reflective_mode", "blocked_output")
- checks: map of check_name -> {passed, details}
- run_id: string

## Compliance checks (MVP)
Pre-checks:
- PII detection in Spec fields (emails/phones/address-like patterns).
- Prompt-injection heuristics (e.g., "ignore previous instructions", "reveal system prompt").
- Intent gate: block disallowed content categories (simple rules).

Post-checks:
- PII detection in output.
- Banned words check.
- "Strong factual claim" heuristic:
  - If mode="facts" and no sources, flag/block strong claims.
  - If mode="reflective", allow but warn if tone becomes overly assertive.
- Optional: "medical/legal advice" blocker for MVP.

All checks should be deterministic and testable.

## Interfaces / Modules
- schemas/spec.py: Pydantic model for Spec
- providers/base.py: LLMProvider interface
- pipeline/run.py: orchestrator (load spec, run generate, run compliance, save artifacts)
- compliance/router.py: returns report + decisions
- eval/runner.py: runs examples and prints a table

## CLI
Command:
- json-to-essay render <spec.json> -o <output_dir>

Artifacts folder always contains:
- essay.md
- compliance_report.json
- meta.json
- input_spec.json

## UI (optional but recommended)
Streamlit app:
- Upload/paste JSON
- Click "Generate"
- Show essay + compliance report panel
- Download artifacts zip (optional)

## Development constraints
- Start with a local .venv and clean .gitignore.
- No secrets committed. Use .env and OPENAI_API_KEY (or equivalent).
- Keep scope tight; prioritize a working demo with clean logs and tests.

## Phase plan after MVP
Phase 2: Add optional plan.json (structured intermediate object).
Phase 3: Add critique.json + a single revise pass (max 2 iterations).
Phase 4: Add RAG for facts mode (sources + citations).
