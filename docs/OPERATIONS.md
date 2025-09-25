
# Operations

## Running locally
```
infra-sentinel run --config config/sentinel.yaml --events demo/events.jsonl --dry-run
```

## Environment variables
- `INFRA_SENTINEL_ENV` — Override environment (dev/staging/prod)
- `INFRA_SENTINEL_LOG` — Log level (DEBUG/INFO/WARN/ERROR)

## Result artifacts
- Audit log (`results/audit.jsonl`) contains all decisions and actions (dry-run aware).

## Extending providers
Implement a new provider in `src/infra_sentinel/providers/` by subclassing `BaseProvider`.
Register it in `providers.yaml` and wire through the CLI.
