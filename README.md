# minicode

## Install
Install uv.

## Creating benchmark splits locally

Run all commands from the repository root directory.

1. CodeContests
```
uv run python -m minicode.setup_codecontests
```
2. Small repositories
```
uv run python -m minicode.setup_repos
```
3. Large repositories
```
uv run python -m minicode.setup_large_repos
```
