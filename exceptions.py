class AppError(Exception):
    """Base class for expected, business-level errors."""

    def __init__(self, status_code: int, error_code: str, message: str):
        self.status_code = status_code
        self.error_code = error_code
        self.message = message
        super().__init__(message)


class DisposableEmailError(AppError):
    def __init__(self):
        super().__init__(
            status_code=400,
            error_code="DISPOSABLE_EMAIL",
            message="Disposable/throwaway email addresses are not accepted.",
        )


class LowEffortMessageError(AppError):
    def __init__(self):
        super().__init__(
            status_code=400,
            error_code="LOW_EFFORT_MESSAGE",
            message="Message must contain meaningful content, not repeated characters.",
        )