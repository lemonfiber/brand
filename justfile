default:
    @just --list
ci: lint tokens

# The gate script itself. First: a name that does not exist here reads as a
# token that does not match.
lint:
    uvx ruff@0.16.4 check scripts/

tokens:
    python3 scripts/check_tokens.py --self-test
    python3 scripts/check_tokens.py
