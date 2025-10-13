"""Module: test_errors.py

Description:
    Test cases for custom error classes.

Author: Nathan Thomas
"""

from fastapi import HTTPException

from app.shared.errors.errors import (
    ConflictError,
    CustomError,
    ForbiddenError,
    NotFoundError,
    UnauthorizedError,
    ValidationError,
)


class TestCustomError:
    """Test CustomError base class."""

    def test_custom_error_basic(self) -> None:
        """Test basic CustomError initialization."""

        error = CustomError(status_code=400, message="Test error message", code="TEST_ERROR", field="test_field")

        assert error.status_code == 400
        assert error.detail == [{"message": "Test error message", "code": "TEST_ERROR", "field": "test_field"}]

    def test_custom_error_minimal(self) -> None:
        """Test CustomError with minimal parameters."""
        error = CustomError(status_code=500, message="Server error")

        assert error.status_code == 500
        assert error.detail == [{"message": "Server error", "code": None, "field": None}]

    def test_custom_error_inheritance(self) -> None:
        """Test that CustomError inherits from HTTPException."""
        error = CustomError(status_code=400, message="Test")
        assert isinstance(error, HTTPException)

    def test_custom_error_with_code_only(self) -> None:
        """Test CustomError with code but no field."""
        error = CustomError(status_code=400, message="Test message", code="TEST_CODE")

        assert error.detail == [{"message": "Test message", "code": "TEST_CODE", "field": None}]

    def test_custom_error_with_field_only(self) -> None:
        """Test CustomError with field but no code."""
        error = CustomError(status_code=400, message="Test message", field="test_field")

        assert error.detail == [{"message": "Test message", "code": None, "field": "test_field"}]


class TestValidationError:
    """Test ValidationError class."""

    def test_validation_error_basic(self) -> None:
        """Test basic ValidationError initialization."""
        error = ValidationError(message="Invalid input", field="username")

        assert error.status_code == 422
        assert error.detail == [{"message": "Invalid input", "code": "VALIDATION_ERROR", "field": "username"}]

    def test_validation_error_custom_code(self) -> None:
        """Test ValidationError with custom code."""
        error = ValidationError(message="Email format invalid", field="email", code="INVALID_EMAIL_FORMAT")

        assert error.status_code == 422
        assert error.detail == [{"message": "Email format invalid", "code": "INVALID_EMAIL_FORMAT", "field": "email"}]

    def test_validation_error_inheritance(self) -> None:
        """Test ValidationError inheritance."""
        error = ValidationError(message="Test", field="test")
        assert isinstance(error, CustomError)
        assert isinstance(error, HTTPException)


class TestNotFoundError:
    """Test NotFoundError class."""

    def test_not_found_error_basic(self) -> None:
        """Test basic NotFoundError with default resource."""
        error = NotFoundError()

        assert error.status_code == 404
        assert error.detail == [{"message": "Resource not found", "code": "NOT_FOUND", "field": None}]

    def test_not_found_error_with_resource(self) -> None:
        """Test NotFoundError with custom resource name."""
        error = NotFoundError(resource="User")

        assert error.status_code == 404
        assert error.detail == [{"message": "User not found", "code": "NOT_FOUND", "field": None}]

    def test_not_found_error_with_resource_id(self) -> None:
        """Test NotFoundError with resource and ID."""
        error = NotFoundError(resource="User", resource_id=123)

        assert error.status_code == 404
        assert error.detail == [{"message": "User not found with id: 123", "code": "NOT_FOUND", "field": None}]

    def test_not_found_error_with_string_id(self) -> None:
        """Test NotFoundError with string resource ID."""
        error = NotFoundError(resource="Document", resource_id="doc-abc-123")

        assert error.status_code == 404
        assert error.detail == [
            {"message": "Document not found with id: doc-abc-123", "code": "NOT_FOUND", "field": None}
        ]

    def test_not_found_error_inheritance(self) -> None:
        """Test NotFoundError inheritance."""
        error = NotFoundError()
        assert isinstance(error, CustomError)
        assert isinstance(error, HTTPException)


class TestConflictError:
    """Test ConflictError class."""

    def test_conflict_error_basic(self) -> None:
        """Test basic ConflictError initialization."""
        error = ConflictError(message="Resource already exists")

        assert error.status_code == 409
        assert error.detail == [{"message": "Resource already exists", "code": "CONFLICT", "field": None}]

    def test_conflict_error_with_field(self) -> None:
        """Test ConflictError with field."""
        error = ConflictError(message="Username already taken", field="username")

        assert error.status_code == 409
        assert error.detail == [{"message": "Username already taken", "code": "CONFLICT", "field": "username"}]

    def test_conflict_error_inheritance(self) -> None:
        """Test ConflictError inheritance."""
        error = ConflictError(message="Test")
        assert isinstance(error, CustomError)
        assert isinstance(error, HTTPException)


class TestUnauthorizedError:
    """Test UnauthorizedError class."""

    def test_unauthorized_error_default(self) -> None:
        """Test UnauthorizedError with default message."""
        error = UnauthorizedError()

        assert error.status_code == 401
        assert error.detail == [{"message": "Authentication required", "code": "UNAUTHORIZED", "field": None}]

    def test_unauthorized_error_custom_message(self) -> None:
        """Test UnauthorizedError with custom message."""
        error = UnauthorizedError(message="Invalid credentials")

        assert error.status_code == 401
        assert error.detail == [{"message": "Invalid credentials", "code": "UNAUTHORIZED", "field": None}]

    def test_unauthorized_error_inheritance(self) -> None:
        """Test UnauthorizedError inheritance."""
        error = UnauthorizedError()
        assert isinstance(error, CustomError)
        assert isinstance(error, HTTPException)


class TestForbiddenError:
    """Test ForbiddenError class."""

    def test_forbidden_error_default(self) -> None:
        """Test ForbiddenError with default message."""
        error = ForbiddenError()

        assert error.status_code == 403
        assert error.detail == [{"message": "Access forbidden", "code": "FORBIDDEN", "field": None}]

    def test_forbidden_error_custom_message(self) -> None:
        """Test ForbiddenError with custom message."""
        error = ForbiddenError(message="Insufficient permissions")

        assert error.status_code == 403
        assert error.detail == [{"message": "Insufficient permissions", "code": "FORBIDDEN", "field": None}]

    def test_forbidden_error_inheritance(self) -> None:
        """Test ForbiddenError inheritance."""
        error = ForbiddenError()
        assert isinstance(error, CustomError)
        assert isinstance(error, HTTPException)


class TestErrorInteraction:
    """Test error classes working together."""

    def test_all_errors_have_consistent_structure(self) -> None:
        """Test that all error types maintain consistent detail structure."""
        errors = [
            CustomError(status_code=400, message="Custom"),
            ValidationError(message="Validation", field="field"),
            NotFoundError(resource="Test"),
            ConflictError(message="Conflict"),
            UnauthorizedError(),
            ForbiddenError(),
        ]

        for error in errors:
            assert isinstance(error.detail, list)
            assert len(error.detail) == 1
            assert "message" in error.detail[0]
            assert "code" in error.detail[0]
            assert "field" in error.detail[0]
            assert isinstance(error.detail[0]["message"], str)

    def test_status_codes_are_correct(self) -> None:
        """Test that all errors have the correct HTTP status codes."""
        test_cases = [
            (ValidationError(message="Test", field="field"), 422),
            (NotFoundError(), 404),
            (ConflictError(message="Test"), 409),
            (UnauthorizedError(), 401),
            (ForbiddenError(), 403),
        ]

        for error, expected_status in test_cases:
            assert error.status_code == expected_status

    def test_error_codes_are_set(self) -> None:
        """Test that all specific error types have proper error codes."""
        test_cases = [
            (ValidationError(message="Test", field="field"), "VALIDATION_ERROR"),
            (NotFoundError(), "NOT_FOUND"),
            (ConflictError(message="Test"), "CONFLICT"),
            (UnauthorizedError(), "UNAUTHORIZED"),
            (ForbiddenError(), "FORBIDDEN"),
        ]

        for error, expected_code in test_cases:
            assert error.detail[0]["code"] == expected_code
