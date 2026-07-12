# Security Policy

## Supported Versions

This project is currently pre-1.0. Security fixes are applied to the `main` branch.

## Reporting a Vulnerability

Please do not open a public issue for secrets, credential exposure, or exploitable workflow behavior.

Report privately through GitHub Security Advisories when available, or contact the maintainer directly through the GitHub profile linked from this repository.

Useful details:

- affected file or workflow
- reproduction steps
- expected impact
- whether any token, Figma file, or private prompt data is involved

## Security Scope

Important areas:

- GitHub Actions permissions
- Figma access tokens
- MCP server behavior
- prompt files that may contain private context
- generated catalog or fixture data

Never commit real Figma tokens, GitHub tokens, API keys, private Figma file data, or customer prompt data.

