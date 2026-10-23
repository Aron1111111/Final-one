"""Check local documentation files without accessing the application API."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
import re
import sys

root = Path(__file__).resolve().parents[1]
required = ['.gitattributes',
 '.github/workflows/python-app.yml',
 '.gitignore',
 'COLLABORATION.md',
 'README.md',
 'REPORT.md',
 'SOURCES.md',
 'STORAGE_POLICY.md',
 'api/bookclub.openapi.yaml',
 'bookclub/__init__.py',
 'bookclub/description_validator.py',
 'bookclub/errors.py',
 'bookclub/status_transitions.py',
 'bookclub/web_app.py',
 'docs/admin-guide.md',
 'docs/architecture.md',
 'docs/build-check.md',
 'docs/document-register.md',
 'docs/images/components.png',
 'docs/images/sequence.png',
 'docs/requirements.md',
 'docs/review-checklist.md',
 'docs/review-requirements.md',
 'docs/testing.md',
 'docs/user-guide.md',
 'docs/verification.md',
 'pytest.ini',
 'tests/test_description_validator.py',
 'tests/test_errors.py',
 'tests/test_status_transitions.py',
 'tests/test_web_app.py',
 'web/index.html',
 'web/styles.css',
 'web/app.js',
 'tools/check_docs.py']
errors = []
count = 0
for name in required:
    if not (root / name).is_file():
        errors.append("Missing required file: " + name)
for page in root.rglob("*.md"):
    if ".git" in page.relative_to(root).parts:
        continue
    for target in re.findall(r"\]\(([^)]+)\)", page.read_text(encoding="utf-8")):
        url = urlsplit(target)
        if url.scheme or url.netloc or not url.path:
            continue
        dest = (page.parent / unquote(url.path)).resolve()
        if not dest.is_relative_to(root):
            errors.append("Path escapes project: " + target)
        elif not dest.is_file():
            errors.append("Missing link target: " + target)
        count += 1
for name in ["components.png", "sequence.png"]:
    path = root / "docs" / "images" / name
    if path.is_file() and path.read_bytes()[:8] != b"\x89PNG\r\n\x1a\n":
        errors.append("Invalid PNG header: " + name)
if errors:
    print("FAIL")
    print("\n".join(errors))
    sys.exit(1)
print(f"PASS: {len(required)} required files; {count} relative file links; 2 PNG headers")
