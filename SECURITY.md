# Security and responsible disclosure

## Supported version

Only the latest tagged release is supported.

## Reporting a vulnerability

Do not open a public issue containing credentials, private paths, restricted
data, or unpublished research material. Contact the repository maintainers
privately through the institutional contact listed in the accompanying
submission materials.

Include only the minimum information needed to reproduce the problem. Do not
attach raw project data or manuscript files.

## Public-release policy

This repository must never contain:

- authentication tokens, passwords, private keys, or `.env` files;
- manuscript source, peer-review correspondence, or editorial files;
- raw or restricted project data;
- private absolute filesystem paths;
- production calibration archives;
- unpublished work intended for a separate study.

Run `python scripts/audit_release.py` before every commit and release.
