# Contributing to Python-Dictionary-IP-MAC

Although **Python-Dictionary-IP-MAC** is developed as a solo project, it intentionally follows **professional, production-grade workflows**. This document defines the conventions used throughout the repository.

---

## 🌿 Branching Strategy

### Permanent branches
- **`development`** – Default branch, active integration branch
- **`main`** – Stable, demo-ready releases only

Direct commits to these branches are **not allowed**.
All changes must go through Pull Requests.

---

## 🌱 Local Branch Naming

Local branches must follow this convention:

```
<prefix>/<short-description>
```

### Allowed prefixes

| Prefix | Purpose |
|------|--------|
| `feature/` | New business functionality |
| `bugfix/` | Fixing incorrect behavior |
| `refactor/` | Internal restructuring without behavior change |
| `chore/` | Non-functional maintenance |
| `infra/` | Infrastructure changes |
| `test/` | Tests only |
| `docs/` | Documentation only |

### Examples

```
feature/network-info
feature/scanner
feature/parser
feature/exporter
feature/config
bugfix/parser-mac-extraction
refactor/network-info-cidr
docs/readme-and-contributing
test/parser
```

---

## 📝 Commit Message Convention

Commits follow **Conventional Commits**:

```
<type>(<scope>): <description>
```

### Common types

- `feat` – New functionality
- `fix` – Bug fix
- `refactor` – Code restructuring
- `chore` – Maintenance or tooling
- `infra` – Infrastructure changes
- `docs` – Documentation
- `test` – Tests

### Examples

```
chore(scaffold): add main.py and network_info.py empty structure
feat(network-info): parse all available network interfaces from ipconfig
feat(network-info): convert selected interface to CIDR notation
feat(scanner): run nmap scan and return raw XML output via -oX flag
feat(parser): extract ip, mac and vendor and tag localhost device
feat(exporter): structure device list into json payload
feat(logger-integration): add logging to main pipeline
feat(config): integrate config into scanner module
test(parser): verify correct number of devices parsed
docs(readme-and-contributing): update project documentation
```

---

## ⚙️ Configuration

All configurable values are managed from `config/settings.json`.
**Never hardcode values** that belong in the config file.

When adding new configurable values:
1. Add them to `config/settings.json`
2. Expose them via `get_config()` in `src/utils/config.py`
3. Consume them from `get_config()` in the relevant module

---

## 🔀 Pull Request Workflow

1. Branch off from `development`
2. Keep branches short-lived and focused on a single module or concern
3. Open a Pull Request targeting `development`
4. Use **Squash and Merge**
5. Delete branch after merge

### Pull Request format

```
Title: <type>(<scope>): <short description>

Summary:
Brief description of what this PR does and why.

Key features:
- What was added or changed
- Each bullet is a meaningful unit of work

Infrastructure:
- Files added or modified

Notes:
- Any important decisions, limitations or follow-ups
```

---

## 🚀 Merging & Releases

- All PRs merge into `development`
- `main` is updated only at milestones
- Releases are tagged (e.g. `v0.1.0`, `v1.0.0`)

---

## ⚠️ History & Safety Rules

- Force pushes are not allowed on protected branches
- Deleting protected branches is restricted
- History must remain clean and traceable

---

## 🧪 Running Tests

```bash
python -m unittest tests/test_parser.py -v
```

- Tests do not require Nmap or Administrator privileges
- All new modules should have corresponding unit tests in `tests/`
- Logger is disabled in tests using `logging.disable(logging.CRITICAL)`
- Never use hardcoded values in tests — use the sample XML fixture pattern

---

## 📌 Final Notes

These rules are intentionally strict to encourage:
- Clean Git history
- Clear module responsibility
- Real-world engineering discipline

Consistency is more important than perfection.
