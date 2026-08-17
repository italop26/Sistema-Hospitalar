import jwt

from datetime import datetime, timedelta, timezone

from django.conf import settings


def gerar_token(user):

    payload = {
        "user_id": user.id,
        "exp": datetime.now(timezone.utc) + timedelta(hours=2),
        "iat": datetime.now(timezone.utc),
    }

    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm="HS256"
    )

    return token


def decodificar_token(token):

    try:

        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"]
        )

        return payload

    except jwt.ExpiredSignatureError:
        return None

    except jwt.InvalidTokenError:
        return None