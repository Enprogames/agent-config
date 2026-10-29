"""Domain errors with user-readable messages."""


class ResponsePdfError(RuntimeError):
    """Base class for expected workflow failures."""


class CaptureError(ResponsePdfError):
    """Raised when a deterministic response cannot be captured."""


class RenderError(ResponsePdfError):
    """Raised when browser rendering fails."""


class VerificationError(ResponsePdfError):
    """Raised when a generated artifact fails validation."""


class PrintError(ResponsePdfError):
    """Raised when a print plan or submission is unsafe or invalid."""
