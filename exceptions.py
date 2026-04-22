"""Custom exception hierarchy for the library-domain."""


class LibraryError(Exception):
    """Base exception for all library-domain errors."""


class DataLoadError(LibraryError):
    """CSV/JSON file missing, malformed, or schema mismatch."""


class PersistenceError(LibraryError):
    """Failed to write or read data.json."""


class ValidationError(LibraryError):
    """User-supplied input failed a Validator rule."""


class NotFoundError(LibraryError):
    """Member, Item or Transaction ID not found."""


class BorrowingError(LibraryError):
    """Cannot borrow/return (already borrowed, no copies, not held by member, etc.)."""
