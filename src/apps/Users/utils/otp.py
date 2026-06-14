import random
from src.apps.users.redis_client import redis_client


def create_otp(email):
    otp = str(random.randint(1000, 9999))

    redis_client.set(
        f"otp:{email}",
        otp,
        ex=120
    )

    return otp


def get_otp(email):
    return redis_client.get(f"otp:{email}")


def delete_otp(email):
    redis_client.delete(f"otp:{email}")