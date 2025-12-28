# Repository Discipline

This document outlines the operating model for maintaining the public reference repo versus the private product repo.

## Public Repo Rules

**This Repository (form-to-essay):**

- ✅ `main` branch must always be green (all tests pass)
- ✅ Use tags/releases for versioning (e.g., `v0.1.0`)
- ✅ CI required for all PRs (GitHub Actions)
- ✅ **No secrets ever committed** (verify `.env` is gitignored)
- ✅ No user data storage beyond local artifacts in `outputs/`
- ✅ Keep spec→artifacts contract stable
- ✅ Documentation must be clear and accurate
- ✅ All code must be MIT licensed

**What Goes in Public:**
- Core engine code (pipeline, providers, compliance)
- CLI and Streamlit UI (thin wrappers)
- Tests and examples
- Documentation and README
- CI workflows

**What Does NOT Go in Public:**
- API keys or secrets
- User data or run history
- Proprietary optimization algorithms
- Production monitoring/analytics code
- Billing or subscription logic

## Private Repo Rules

**Private Product Repository:**

- ⚠️ **Never sync branches into public** (keep work separate)
- ⚠️ Treat templates, evals, and user feedback as proprietary
- ⚠️ Strict secret management (use secure vaults, not `.env` in repo)
- ⚠️ Production-grade security practices
- ⚠️ Separate CI/CD pipelines

**Naming Guidance:**
- Public: `form-to-essay` (reference/demo)
- Private: `form-n-essay` or similar (product)

## Keep-Options-Open Architecture

**Core Principle:** Interfaces and abstractions stay stable; implementations can swap later.

**Stable Contracts:**
- `run_pipeline(spec, output_dir)` → produces 4 artifacts
- Provider interface: `generate_essay(prompt, max_tokens)` → `(text, metadata)`
- Spec schema: `EssaySpec` Pydantic model
- Compliance report schema: `ComplianceReport` Pydantic model

**What Can Change:**
- Provider implementations (add new providers)
- UI frameworks (Streamlit → FastAPI → Next.js)
- Storage backends (local files → database → S3)
- Optimization strategies (single-pass → multi-pass)

**Migration Path:**
The private product can import and extend the public repo's core engine, adding proprietary layers without breaking the public contract.

