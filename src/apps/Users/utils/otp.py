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



def increment_resend_count(email):
    key = f"resend_count:{email}"

    count = redis_client.incr(key)

    if count == 1:
        redis_client.expire(key, 600)

    return count

def get_resend_count(email):
    count = redis_client.get(
        f"resend_count:{email}"
    )

    return int(count) if count else 0


def set_resend_lock(email):
    redis_client.set(
        f"resend_lock:{email}",
        1,
        ex=30
    )


def has_resend_lock(email):
    return redis_client.exists(
        f"resend_lock:{email}"
    )