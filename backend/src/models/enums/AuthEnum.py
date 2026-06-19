from enum import Enum

class AuthEnum(Enum):
    COLLECTION_NAME='users'
    AUTH_HEADER_MISSED='Authorization header missing or malformed'
    TOKEN_PAYLOAD_MISSED_USER_ID="Token payload does not contain user_id"
    USER_NOT_FOUND="User not found"
    USER_WITH_EMAIL_ALREADY_EXITS="A user with this email already exists"
    USER_WITH_NAME_ALREADY_EXITS="A user with this username already exists"
    INVALID_EMAIL_OR_PASSWORD="Invalid email or password"
    AT_LEAST_ONE_FIELD_MUST_BE_PROVIDED="At least one field must be provided to update"
    USERNAME_ALREADY_IN_USE="Username is already in use"
    EMAIL_ALREADY_IN_USE="Email is already in use"
    FAILED_TO_UPDATE="Failed to update user profile"
    FAILED_TO_DELETE_USER="Failed to delete user"
    TOKEN_EXPIRED="Token has expired"
    INVALID_TOKEN="Invalid authentication token"