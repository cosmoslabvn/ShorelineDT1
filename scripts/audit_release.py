"""Fail when a public release contains likely private or sensitive material."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAX_PUBLIC_FILE_BYTES = 1024 * 1024
ALLOWED_TOP_LEVEL = {
    ".gitattributes",
    ".github",
    ".gitignore",
    ".project",
    "CITATION.cff",
    "LICENSE",
    "PUBLIC_RELEASE_MANIFEST.md",
    "README.md",
    "SECURITY.md",
    "docs",
    "models",
    "output",
    "sample_data",
    "scripts",
}
DENIED_DIRECTORY_NAMES = {
    "includes",
    "manuscript",
    "paper",
    "private",
    "raw",
    "restricted",
    "research",
    "reviews",
}
DENIED_SUFFIXES = {
    ".doc",
    ".docx",
    ".key",
    ".mat",
    ".pdf",
    ".pem",
    ".pfx",
    ".pickle",
    ".pkl",
    ".ppt",
    ".pptx",
    ".rar",
    ".shp",
    ".tif",
    ".tiff",
    ".xls",
    ".xlsx",
    ".zip",
    ".7z",
}
TEXT_SUFFIXES = {
    "",
    ".cff",
    ".csv",
    ".gaml",
    ".gitignore",
    ".gitattributes",
    ".json",
    ".md",
    ".project",
    ".py",
    ".txt",
    ".yml",
    ".yaml",
}
SENSITIVE_PATTERNS = {
    "GitHub token": re.compile(r"(?:ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})"),
    "AWS access key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "private key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "credential assignment": re.compile(
        r"(?i)(?:api[_-]?key|client[_-]?secret|password|access[_-]?token|secret[_-]?key)\s*[:=]"
    ),
    "Windows user path": re.compile(r"[A-Za-z]:\\Users\\"),
    "Unix home path": re.compile(r"/(?:home|Users)/[^/\s]+/"),
}


def iter_public_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if ".git" in relative.parts or "__pycache__" in relative.parts:
            continue
        if path.is_file():
            files.append(path)
    return files


def main() -> int:
    issues: list[str] = []
    top_level = {path.name for path in ROOT.iterdir() if path.name != ".git"}
    unexpected = sorted(top_level.difference(ALLOWED_TOP_LEVEL))
    if unexpected:
        issues.append(f"unexpected top-level content: {', '.join(unexpected)}")

    required = {"README.md", "LICENSE", "CITATION.cff", "SECURITY.md"}
    missing = sorted(name for name in required if not (ROOT / name).is_file())
    if missing:
        issues.append(f"missing required files: {', '.join(missing)}")

    for path in iter_public_files():
        relative = path.relative_to(ROOT)
        lower_parts = {part.lower() for part in relative.parts[:-1]}
        denied_parts = sorted(lower_parts.intersection(DENIED_DIRECTORY_NAMES))
        if denied_parts:
            issues.append(f"{relative}: denied directory name {denied_parts[0]!r}")
        if path.suffix.lower() in DENIED_SUFFIXES:
            issues.append(f"{relative}: denied public-release file type")
        if path.stat().st_size > MAX_PUBLIC_FILE_BYTES:
            issues.append(f"{relative}: exceeds 1 MiB public-release limit")
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            issues.append(f"{relative}: expected UTF-8 text")
            continue
        for label, pattern in SENSITIVE_PATTERNS.items():
            if pattern.search(content):
                issues.append(f"{relative}: possible {label}")

    if issues:
        print("PUBLIC RELEASE AUDIT FAILED")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print(f"PUBLIC RELEASE AUDIT PASSED ({len(iter_public_files())} files checked)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
