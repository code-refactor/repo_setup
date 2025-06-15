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

## Run agent baseline

Make sure that `.env` exists in the main directory with `TOGETHER_API_KEY` and `OPENAI_API_KEY` and `ANTHROPIC_API_KEY`.

1. CodeContests
```
bash scripts/codecontests/run_claude.sh
```

2. Small repositories
```
bash scripts/small_repos/run_codex.sh
bash scripts/small_repos/run_claude.sh
```

3. Large repositories
```
bash scripts/large_repos/run_claude.sh
```
