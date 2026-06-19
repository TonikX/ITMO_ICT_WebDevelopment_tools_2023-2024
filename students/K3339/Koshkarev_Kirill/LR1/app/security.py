"""Безопасность: хэширование паролей, создание и проверка JWT.

Важно по заданию: аутентификация по JWT (п.3) реализована ВРУЧНУЮ, без
сторонних библиотек. Здесь же вручную реализованы и кодирование/проверка
подписи JWT, и хэширование паролей — используется только стандартная
библиотека Python (hashlib, hmac, base64, secrets, json).
"""
import base64
import hashlib
import hmac
import json
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional

from app.config import settings

# ---------------------------------------------------------------------------
# Хэширование паролей (PBKDF2-HMAC-SHA256, стандартная библиотека)
# ---------------------------------------------------------------------------

_PBKDF2_ITERATIONS = 200_000
_SALT_BYTES = 16


def hash_password(password: str) -> str:
    """Возвращает строку формата pbkdf2_sha256$iterations$salt$hash."""
    salt = secrets.token_bytes(_SALT_BYTES)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, _PBKDF2_ITERATIONS)
    return "pbkdf2_sha256${}${}${}".format(
        _PBKDF2_ITERATIONS,
        base64.b64encode(salt).decode("ascii"),
        base64.b64encode(dk).decode("ascii"),
    )


def verify_password(password: str, stored: str) -> bool:
    """Проверяет пароль против сохранённого хэша (защита от timing-атак)."""
    try:
        algorithm, iterations, salt_b64, hash_b64 = stored.split("$")
        if algorithm != "pbkdf2_sha256":
            return False
        salt = base64.b64decode(salt_b64)
        expected = base64.b64decode(hash_b64)
        dk = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt, int(iterations)
        )
        return hmac.compare_digest(dk, expected)
    except (ValueError, TypeError):
        return False


# ---------------------------------------------------------------------------
# JWT: ручная реализация (HS256). Создание токена по условию допускается, но
# здесь оно тоже сделано вручную, чтобы продемонстрировать механизм.
# ---------------------------------------------------------------------------


def _b64url_encode(data: bytes) -> str:
    """Base64URL без padding (как требует спецификация JWT)."""
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def _sign(signing_input: bytes) -> bytes:
    return hmac.new(
        settings.JWT_SECRET.encode("utf-8"), signing_input, hashlib.sha256
    ).digest()


def create_access_token(subject: str, extra: Optional[dict] = None) -> str:
    """Создаёт подписанный JWT (header.payload.signature)."""
    header = {"alg": settings.JWT_ALGORITHM, "typ": "JWT"}
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(subject),
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp()),
    }
    if extra:
        payload.update(extra)

    header_segment = _b64url_encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    payload_segment = _b64url_encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    signing_input = f"{header_segment}.{payload_segment}".encode("ascii")
    signature = _b64url_encode(_sign(signing_input))
    return f"{header_segment}.{payload_segment}.{signature}"


class JWTError(Exception):
    """Ошибка разбора или проверки токена."""


def decode_access_token(token: str) -> dict:
    """Проверяет подпись и срок жизни, возвращает payload.

    Бросает JWTError при любой проблеме (формат, подпись, истёкший срок).
    """
    try:
        header_segment, payload_segment, signature_segment = token.split(".")
    except ValueError:
        raise JWTError("Неверный формат токена")

    signing_input = f"{header_segment}.{payload_segment}".encode("ascii")
    expected_signature = _sign(signing_input)
    try:
        actual_signature = _b64url_decode(signature_segment)
    except Exception:
        raise JWTError("Неверная подпись токена")

    # Сравнение, устойчивое к timing-атакам.
    if not hmac.compare_digest(expected_signature, actual_signature):
        raise JWTError("Подпись токена не совпадает")

    try:
        payload = json.loads(_b64url_decode(payload_segment))
    except Exception:
        raise JWTError("Не удалось прочитать payload токена")

    exp = payload.get("exp")
    if exp is not None and int(exp) < int(datetime.now(timezone.utc).timestamp()):
        raise JWTError("Срок действия токена истёк")

    return payload
