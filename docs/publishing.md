# Publishing Guide

This document describes how to maintain and publish releases for the public reference repo.

## Cutting a Release

### 1. Update Version

Update version in `pyproject.toml`:
```toml
version = "0.1.0"
```

### 2. Update CHANGELOG.md

Add a new section for the release:
```markdown
## [0.1.0] - YYYY-MM-DD

### Added
- Feature X
- Feature Y

### Fixed
- Bug Z
```

### 3. Create Git Tag

```bash
git tag -a v0.1.0 -m "Release v0.1.0: Initial public demo"
git push origin v0.1.0
```

### 4. Create GitHub Release (Optional)

- Go to GitHub → Releases → "Draft a new release"
- Select the tag
- Copy changelog content
- Mark as "Latest release"

## Keeping Public vs Private Work Separated

**Do:**
- Work on public features in this repo
- Keep commits focused and clean
- Use feature branches for larger changes

**Don't:**
- Commit private product code to this repo
- Sync private repo branches here
- Include proprietary algorithms or data

**Workflow:**
1. Public repo: Reference implementation, examples, docs
2. Private repo: Import public repo as dependency, add proprietary layers

## GitHub About Box (Manual Steps)

If GitHub CLI (`gh`) is not available, manually set the About box:

1. Go to: https://github.com/gschu1/form-to-essay/settings
2. Scroll to "Repository details"
3. Set **Description:**
   ```
   Demo/reference repo: JSON/Form → essay + compliance report. Hosted product adds storage, RAG, optimizers, reliability.
   ```
4. Add **Topics:**
   - `llm`
   - `streamlit`
   - `typer`
   - `evals`
   - `ai-tools`
   - `python`
   - `compliance`
   - `essay-generation`

## Pre-Push Checklist

- [ ] All tests pass: `pytest`
- [ ] No secrets in staged files: `git diff --staged | findstr -i "api_key\|secret\|password"`
- [ ] `.env` is gitignored and not tracked
- [ ] `outputs/` directory is gitignored
- [ ] README is updated and accurate
- [ ] CHANGELOG.md reflects changes
- [ ] Version in `pyproject.toml` is correct

