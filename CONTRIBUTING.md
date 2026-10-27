# Contributing

Thanks for taking the time to improve this educational project. The repository is intentionally small enough to study, but changes should preserve the same production-minded boundaries demonstrated by the example.

## Development workflow

1. Create a branch from `main`.
2. Keep changes focused and explain architectural changes in the pull request.
3. Add or update tests for behavior changes.
4. Run the formatter/linter and test suite locally.
5. Never commit API keys, access tokens, private datasets, or customer data.

## Code style

- Prefer explicit types and small functions.
- Keep HTTP, application, and infrastructure concerns separate.
- Validate data at boundaries.
- Raise domain/application exceptions from services and translate them at the HTTP layer.
- Keep provider-specific SDK code behind an interface or adapter.
- Add comments for *why* a non-obvious decision exists, not for what obvious code does.

## Pull requests

A useful pull request description includes: what changed, why it changed, how it was tested, and any trade-offs or follow-up work.

## Security

If you discover a security issue, do not include secrets or exploit data in a public issue. Use a private disclosure channel for the repository owner instead.
