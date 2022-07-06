from django.conf import settings
from redis import Redis


def record_nfts_on_redis(nfts):
    redis_client = Redis(settings.REDIS_HOST, port=settings.REDIS_PORT)
    with redis_client.pipeline() as pipe:
        pipe.delete('nfts')
        pipe.rpush('nfts', *nfts)
        pipe.execute()


def get_nfts_from_redis():
    redis_client = Redis(settings.REDIS_HOST, port=settings.REDIS_PORT)
    nfts = redis_client.lrange('nfts', 0, -1)
    if nfts is not None and len(nfts) > 0:
        return nfts
    return None


def record_status_purchase(key, value):
    redis_client = Redis(settings.REDIS_HOST, port=settings.REDIS_PORT)
    with redis_client.pipeline() as pipe:
        pipe.delete(key)
        pipe.set(key, value)
        pipe.execute()
