from .errors import DomainError

ALLOWED = {
    "draft": frozenset({"published", "cancelled"}),
    "published": frozenset({"completed", "cancelled"}),
    "completed": frozenset(),
    "cancelled": frozenset(),
}


def transition_status(current: str, target: str, role: str) -> str:
    """Validate an organizer's transition and return the new status."""
    if role != "organizer":
        raise DomainError("ROLE_FORBIDDEN", "Only organizers may change meeting status")
    if not isinstance(current, str) or not isinstance(target, str):
        raise DomainError("INVALID_STATUS", "Status must be a string")
    if current not in ALLOWED or target not in ALLOWED:
        raise DomainError("INVALID_STATUS", "Unknown meeting status")
    if target not in ALLOWED[current]:
        raise DomainError("INVALID_STATUS_TRANSITION", "This status transition is not allowed")
    return target
