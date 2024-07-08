"""Operations with cache module."""

import hashlib
import json
from typing import Any, Optional

import logging
from redis import Redis, ConnectionPool
from redis.backoff import ExponentialBackoff
from redis.exceptions import BusyLoadingError, ConnectionError, TimeoutError
from redis.retry import Retry


class RedisCache:
    """Cache based on Redis."""

    CACHE_KEYS_PREFIX = "PLATFORM_CACHE_"

    def __init__(self, redis_host: str = "localhost:6379") -> None:
        """Create cache class.

        Args:
        ----
            redis_host (str, optional): redis host for read/write. Defaults to "localhost:6379".

        """
        self._redis_client = Redis(
            connection_pool=ConnectionPool.from_url(
                url=f"redis://{redis_host}?decode_responses=True",
                retry=Retry(ExponentialBackoff(), 3),
                retry_on_error=[BusyLoadingError, ConnectionError, TimeoutError],
            )
        )

    def _get_key_name(self, name: str, *args: Optional[Any], **kwargs: Optional[Any]) -> str:
        """Get nmae for cache.

        Args:
        ----
            name (str): function name.
            args (Optional[Any]): arbitrary parameters.
            kwargs (Optional[Any]): arbitrary parameters.

        Returns:
        -------
            str: cache key.

        """
        # prefix if only allowed changeble parameter
        key_params = (
            args,
            tuple(sorted([(k, v) for k, v in kwargs.items() if k != "prefix"])),
        )
        return f"{self.CACHE_KEYS_PREFIX}{name}_{hashlib.md5(bytearray(str(key_params),'utf-8')).hexdigest()}"

    def get_cache(self, name: str, *args: Optional[Any], **kwargs: Optional[Any]) -> Any:
        """Get value from cache.

        Args:
        ----
            name (str): name of cache instance.
            args (Optional[Any]): arbitrary parameters.
            kwargs (Optional[Any]): arbitrary parameters.

        Returns:
        -------
            Any: cached value.

        """
        key = self._get_key_name(name=name, args=args, kwargs=kwargs)

        try:
            cached_value = self._redis_client.get(key)
            value = json.loads(cached_value)["cache"] if cached_value else None
        except Exception:
            value = None

        if value:
            logging.info(f"CACHE: Use cached data for {key}")

        return value

    def set_cache(self, name: str, value: Any, ttl: int = 3600, *args: Optional[Any], **kwargs: Optional[Any]) -> None:
        """Set cache value.

        Args:
        ----
            name (str): name of cache instance.
            value (Any): value.
            ttl (int, optional): TTL. Defaults to 3600.
            args (Optional[Any]): arbitrary parameters
            kwargs (Optional[Any]): arbitrary parameters

        """
        key = self._get_key_name(name=name, args=args, kwargs=kwargs)

        self._redis_client.set(key, json.dumps({"cache": value}))
        self._redis_client.expire(key, ttl)
        logging.info(f"CACHE: Set cached data for {key}")

    def delete_cache(self, name: str, *args: Optional[Any], **kwargs: Optional[Any]) -> None:
        """Delete cache value.

        Args:
        ----
            name (str): name of cache instance.
            args (Optional[Any]): arbitrary parameters.
            kwargs (Optional[Any]): arbitrary parameters.

        """
        key = self._get_key_name(name=name, args=args, kwargs=kwargs)

        logging.info(f"CACHE: Search for {key}")
        keys = self._redis_client.keys(key)
        if keys:
            self._redis_client.delete(*keys)
            logging.info(f"CACHE: Delete cached data for {key}")
