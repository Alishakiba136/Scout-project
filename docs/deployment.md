# SCOUT Deployment Notes

## Development workflow

SCOUT is developed primarily on Ubuntu and deployed to Android/Termux as the runtime target.

```text
PC
  ↓
VS Code
  ↓
Git + GitHub
  ↓
git pull
  ↓
POCO / Termux
```

The repository is the authoritative version of the project. The phone filesystem is not treated as the master copy.

## Deployment principles

- Keep the project under version control.
- Prefer safe, idempotent installation steps.
- Never destroy existing user files without explicit backup guidance.
- Keep runtime configuration separate from committed secrets.

## Future Termux deployment sketch

```bash
git clone <repository>
cd Scout-Project
./scripts/install_termux.sh
python scripts/doctor.py
```

This project does not yet ship a termux installation script because M0 focuses on repository bootstrap and diagnostics, not on hardware-specific runtime deployment.
