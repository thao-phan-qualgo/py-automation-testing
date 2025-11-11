"""
API Configuration for Keycloak Authentication
"""

# Keycloak Configuration
KEYCLOAK_CONFIG = {
    'endpoint': 'https://nonprod-common-keycloak.qualgo.dev/realms/dev-ai-soc/protocol/openid-connect/token',
    'realm': 'dev-ai-soc',
    'base_url': 'https://nonprod-common-keycloak.qualgo.dev',
}

# Test Credentials (for non-prod environment)
TEST_CREDENTIALS = {
    'valid': {
        'client_id': 'be-admin',
        'client_secret': 'fiuX5GrVdLzDzql4jgyd46DZk0Llorar',
        'username': 'thao.pt@qualgo.net',
        'password': 'Password123@',
        'grant_type': 'password'
    },
    'invalid_username': {
        'client_id': 'be-admin',
        'client_secret': 'fiuX5GrVdLzDzql4jgyd46DZk0Llorar',
        'username': 'invalid@qualgo.net',
        'password': 'Password123@',
        'grant_type': 'password'
    },
    'invalid_password': {
        'client_id': 'be-admin',
        'client_secret': 'fiuX5GrVdLzDzql4jgyd46DZk0Llorar',
        'username': 'thao.pt@qualgo.net',
        'password': 'WrongPassword123@',
        'grant_type': 'password'
    }
}

# Expected Response Structure
EXPECTED_TOKEN_RESPONSE = {
    'access_token': str,
    'expires_in': int,
    'refresh_expires_in': int,
    'refresh_token': str,
    'token_type': str,
    'not-before-policy': int,
    'session_state': str,
    'scope': str
}

# JWT Expected Claims
EXPECTED_JWT_CLAIMS = {
    'exp': 'Expiration time',
    'iat': 'Issued at',
    'jti': 'JWT ID',
    'iss': 'Issuer',
    'aud': 'Audience',
    'sub': 'Subject',
    'typ': 'Type',
    'azp': 'Authorized party',
    'sid': 'Session ID',
    'acr': 'Authentication Context Class Reference',
    'scope': 'Scope',
    'email_verified': 'Email verified',
    'preferred_username': 'Preferred username',
    'email': 'Email'
}

# Performance Thresholds
PERFORMANCE_THRESHOLDS = {
    'max_response_time_ms': 3000,
    'token_expires_in': 300,  # 5 minutes
    'refresh_token_expires_in': 1800  # 30 minutes
}

