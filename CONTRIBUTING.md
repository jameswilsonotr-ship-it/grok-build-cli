# Contributing to Grok Build CLI

## Multi-Agent & Forking Workflow

This project is designed to be edited by multiple agents and humans simultaneously.

### Branching Strategy (Hybrid Semantic + Date Versioning)

- `main`: Stable, versioned releases.
- `feature/phase-N-YYYY-MM-DD-description`: For phase work.
- `agent/<agent-name>/task`: For specific agent contributions.
- Tags: Use semantic (v0.1.0) + date (2026-06-18-pre-extract) for hybrid versioning.

### How to Fork & Collaborate

1. Fork the repo.
2. Create a branch from main with clear name.
3. Use config files (YAML) for runtime behavior instead of hardcoding.
4. All changes should pass CI.
5. For data work (Phase 3+), use date ranges and never commit large raw exports.

### Versioning

- Code versions follow Semantic Versioning.
- Data extraction protocols have their own version in manifests.
- Export format schemas are versioned separately (see schemas/ when added).

### Automated CI/CD

GitHub Actions run on every push and PR:
- Lint (ruff)
- Tests (pytest)
- Type checks if applicable

See `.github/workflows/ci.yml`

### Code Style

- Black + Ruff for formatting/linting.
- Extensive docstrings (with fun characters where appropriate).
- Config-driven where possible.

### Adding New Platform Support

See Phase 3 pre-extract for how schemas and conversion passes are handled. Add new platform to config/schemas.

## Code of Conduct

Be kind. This is a sovereign project — treat the data and each other with care.
