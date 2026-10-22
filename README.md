# envdoctor

**Catch missing `.env` keys before they hit production.**

Compares your `.env` to `.env.example` and reports what’s missing (or extra).

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Install

```bash
pip install envdoctor
# or from source
pip install .
```

## Usage

```bash
envdoctor
envdoctor -e .env.local -x .env.example
envdoctor --strict          # also fail on unknown extra keys
```

### Example output

```text
example: .env.example (12 keys)
env:     .env (10 keys)

missing in .env (required by example):
  - DATABASE_URL
  - JWT_SECRET
```

Exit code `1` when keys are missing — ready for CI:

```yaml
- run: envdoctor --strict
```

## License

MIT © [kianPk](https://github.com/kianPk)
