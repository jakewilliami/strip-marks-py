# -*- mode: just -*-

# Test project
test:
    uv run pytest -v

# Check formatting with blue style
fmt:
    # See also configuration for pre-commit:
    #   github.com/jakewilliami/ispunct-py/blob/05934d5c/.pre-commit-config.yaml
    #
    # And for Ruff:
    #   github.com/jakewilliami/ispunct-py/blob/05934d5c/pyproject.toml#L23-L44
    uv run pre-commit run --all-files
    # Alternatively, run fmt-all, because pre-commit seems to refuse to run `ruff`
    # on all files!

fmt-all:
    uv run ruff check --fix  # Linter
    uv run ruff format       # Formatter

# Audit project dependencies
audit:
    # There seems to be a few different methods of auditing dependencies
    # using UV.  The initial method I wrote (390c877b) used:
    #     export_flags := "--no-hashes --no-emit-project --format=requirements-txt"
    #     audit_flags := "--desc --strict --progress-spinner=off"
    #
    #     uv export $(export_flags) > requirements.txt
    #     uvx pip-audit $(audit_flags) -r requirements.txt
    #
    # However, the current version (36870d46) seems to be the most direct.  This was
    # adapted from:
    #   github.com/scottzach1/Python-Injection-Framework/blob/ab4c1780/.github/workflows/pipeline.yml
    #
    # See also:
    #   github.com/astral-sh/uv/issues/9189
    uv tree
    uv pip compile pyproject.toml -o requirements.txt
    uvx pip-audit -r requirements.txt --fix

# Benchmark performance
# bench:
#     TODO
