from fastapi import HTTPException

# Custom error responses
class CustomHTTPException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

class NotFoundException(CustomHTTPException):
    def __init__(self, detail: str = "Not Found"):
        super().__init__(status_code=404, detail=detail)

class UnauthorizedException(CustomHTTPException):
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(status_code=401, detail=detail)

class ForbiddenException(CustomHTTPException):
    def __init__(self, detail: str = "Forbidden"):
        super().__init__(status_code=403, detail=detail)

class EmailAlreadyExistsException(CustomHTTPException):
    def __init__(self, detail: str = "Email already registered"):
        super().__init__(status_code=409, detail=detail)

class IncorrectEmailOrPasswordException(HTTPException):
    def __init__(self):
        detail = "Incorrect email or password"
        super().__init__(status_code=401, detail=detail)

class UserNotFoundException(HTTPException):
    def __init__(self):
        detail = "User not found"
        super().__init__(status_code=401, detail=detail)

class InvalidCredentialsException(HTTPException):
    def __init__(self):
        detail = "Could not validate credentials"
        super().__init__(status_code=401, detail=detail)

class TokenExpiresException(HTTPException):
    def __init__(self):
        detail = "Token has expired"
        super().__init__(status_code=401, detail=detail)


class TokenValidationFailedException(HTTPException):
    def __init__(self):
        detail = "Token validation failed"
        super().__init__(status_code=401, detail=detail)


class PermissionDeniedException(HTTPException):
    def __init__(self):
        detail = "Permission denied"
        super().__init__(status_code=403, detail=detail)