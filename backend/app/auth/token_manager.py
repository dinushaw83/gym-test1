"""Token management for JWT authentication in proj3."""

import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict
from dataclasses import dataclass

import jwt
from jwt import InvalidTokenError

from app.config import (
    JWT_ACCESS_TOKEN_TTL_SECONDS,
    JWT_ALGORITHM,
    JWT_ISSUER,
    JWT_SECRET_KEY,
)


@dataclass
class TokenData:
    """Token metadata extracted from JWT."""
    user_id: int
    role: str
    email: str
    expires_at: datetime
    run_id: str


class TokenManager:
    """Manages JWT token generation and validation."""

    def __init__(
        self,
        token_ttl_seconds: int = JWT_ACCESS_TOKEN_TTL_SECONDS,
        secret_key: str = JWT_SECRET_KEY,
        algorithm: str = JWT_ALGORITHM,
        issuer: str = JWT_ISSUER,
    ):
        self._token_ttl = timedelta(seconds=token_ttl_seconds)
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._issuer = issuer
        self._revoked_jtis: Dict[str, datetime] = {}

    def create_token(self, user_id: int, role: str, email: str, run_id: str = "default") -> str:
        """Generate a new JWT access token."""
        now = datetime.now(timezone.utc)
        expires_at = now + self._token_ttl

        jti = secrets.token_urlsafe(16)
        payload = {
            "sub": str(user_id),
            "email": email,
            "role": role,
            "run_id": run_id,
            "iss": self._issuer,
            "iat": int(now.timestamp()),
            "exp": int(expires_at.timestamp()),
            "jti": jti,
        }

        token = jwt.encode(payload, self._secret_key, algorithm=self._algorithm)
        if isinstance(token, bytes):
            token = token.decode("utf-8")
        return token

    def validate_token(self, token: str) -> Optional[TokenData]:
        """Validate token and return associated data."""
        if not token:
            return None

        try:
            payload = jwt.decode(
                token,
                self._secret_key,
                algorithms=[self._algorithm],
                issuer=self._issuer,
                options={"require": ["exp", "iat", "sub"]},
            )
        except InvalidTokenError:
            return None

        jti = payload.get("jti")
        if isinstance(jti, str) and jti in self._revoked_jtis:
            return None

        try:
            user_id = int(payload.get("sub"))
        except Exception:
            return None

        role = payload.get("role")
        email = payload.get("email")
        exp = payload.get("exp")
        run_id = payload.get("run_id", "default")

        if not isinstance(role, str) or not isinstance(email, str) or not isinstance(exp, int):
            return None

        expires_at = datetime.fromtimestamp(exp, tz=timezone.utc)

        return TokenData(
            user_id=user_id,
            role=role,
            email=email,
            expires_at=expires_at,
            run_id=str(run_id),
        )

    def revoke_token(self, token: str) -> bool:
        """Revoke a token (best-effort, per-process only)."""
        token_data = self.validate_token(token)
        if not token_data:
            return False
        # Extract JTI from token for revocation
        try:
            payload = jwt.decode(
                token, self._secret_key, algorithms=[self._algorithm], options={"verify_signature": False}
            )
            jti = payload.get("jti")
            if isinstance(jti, str):
                self._revoked_jtis[jti] = token_data.expires_at
                return True
        except Exception:
            pass
        return False


# Global token manager instance
_token_manager: Optional[TokenManager] = None


def get_token_manager() -> TokenManager:
    """Get the global token manager instance."""
    global _token_manager
    if _token_manager is None:
        _token_manager = TokenManager()
    return _token_manager


