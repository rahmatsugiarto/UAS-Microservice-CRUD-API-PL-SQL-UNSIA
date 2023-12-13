import datetime
import jwt


def create_access_token(id):
    return jwt.encode({
        "user_id": id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=30),
        "iat": datetime.datetime.utcnow(),
    }, "refresh_secret", algorithm='HS256')