"""Module: errors.py

Description:
    Custom error classes used through the application. All custom errors return the same structure:
    {
        "detail": [
            {
                "message": "Human readable error message",
                "code": "OPTIONAL_ERROR_CODE",
                "field": "optional_field_name"
            }
        ]
    }

Author: Nathan Thomas
"""

from fastapi import HTTPException


class CustomError(HTTPException):
    """Custom exception class that provides a standardized error response format."""

    def __init__(
        self,
        status_code: int,
        message: str,
        code: str | None = None,
        field: str | None = None,
    ):
        detail = [{"message": message, "code": code, "field": field}]
        super().__init__(status_code=status_code, detail=detail)


class ValidationError(CustomError):
    """Validation error with field-specific information."""

    def __init__(self, message: str, field: str, code: str = "VALIDATION_ERROR"):
        super().__init__(status_code=422, message=message, code=code, field=field)


class NotFoundError(CustomError):
    """Resource not found error."""

    def __init__(self, resource: str = "Resource", resource_id: str | None = None):
        message = f"{resource} not found"
        if resource_id:
            message += f" with id: {resource_id}"
        super().__init__(status_code=404, message=message, code="NOT_FOUND")


class ConflictError(CustomError):
    """Resource conflict error (e.g., duplicate entries)."""

    def __init__(self, message: str, field: str | None = None):
        super().__init__(status_code=409, message=message, code="CONFLICT", field=field)


class UnauthorizedError(CustomError):
    """Authentication required error."""

    def __init__(self, message: str = "Authentication required"):
        super().__init__(status_code=401, message=message, code="UNAUTHORIZED")


class ForbiddenError(CustomError):
    """Access forbidden error."""

    def __init__(self, message: str = "Access forbidden"):
        super().__init__(status_code=403, message=message, code="FORBIDDEN")
