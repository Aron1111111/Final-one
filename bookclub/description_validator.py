from .errors import DomainError


def validate_description(value: str | None) -> str:
    """Return stripped text of 10..1000 Unicode code points, inclusive."""
    if value is None:
        raise DomainError("DESCRIPTION_REQUIRED", "Description is required")
    if not isinstance(value, str):
        raise DomainError("INVALID_DESCRIPTION_TYPE", "Description must be a string")
    text = value.strip()
    if not text:
        raise DomainError("DESCRIPTION_REQUIRED", "Description is required")
    if len(text) < 10:
        raise DomainError("DESCRIPTION_TOO_SHORT", "Description must have at least 10 characters")
    if len(text) > 1000:
        raise DomainError("DESCRIPTION_TOO_LONG", "Description must have at most 1000 characters")
    return text
