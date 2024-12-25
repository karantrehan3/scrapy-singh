from redis import Redis
import json
from typing import Any, Dict, Optional, Union
from src.config import settings


class Cache:
    def __init__(self, host: str = "localhost", port: int = 6379) -> None:
        """
        Initialize the Cache with a Redis client.
        """

        self.client = Redis(host=host, port=port)

    def hset(
        self, name: str, key: str, value: Union[str, int, float, bool, dict]
    ) -> None:
        """
        Set the value of a hash field.
        """

        if isinstance(value, (dict, list)):
            value = json.dumps(value, indent=4)
        self.client.hset(name, key, str(value))

    def hget(self, name: str, key: str, parse_type: Optional[str] = "json") -> Any:
        """
        Get the value of a hash field.
        """

        value = self.client.hget(name, key)
        if not value:
            return None
        value = value.decode("utf-8")
        if parse_type:
            if parse_type == "json":
                return json.loads(value)
            elif parse_type == "int":
                return int(value)
            elif parse_type == "bool":
                return value.lower() in ("true", "1")
            elif parse_type == "str":
                return value
        return value

    def hgetall(self, name: str, parse_type: Optional[str] = "json") -> Dict[str, Any]:
        """
        Get all the fields and values in a hash.
        """

        values = self.client.hgetall(name)
        if not values:
            return {}
        if parse_type:
            if parse_type == "json":
                return {k.decode("utf-8"): json.loads(v) for k, v in values.items()}
            elif parse_type == "int":
                return {k.decode("utf-8"): int(v) for k, v in values.items()}
            elif parse_type == "bool":
                return {
                    k.decode("utf-8"): v.lower() in ("true", "1")
                    for k, v in values.items()
                }
            elif parse_type == "str":
                return {k.decode("utf-8"): v.decode("utf-8") for k, v in values.items()}
        return {k.decode("utf-8"): v.decode("utf-8") for k, v in values.items()}

    def hgetall_values(
        self, name: str, parse_type: Optional[str] = "json"
    ) -> list[Any]:
        """
        Get all the values in a hash.
        """

        all_items = self.hgetall(name, parse_type)
        if all_items == {}:
            return []
        return list(all_items.values())

    def set(self, key: str, value: Union[str, int, float, bool, dict]) -> None:
        """
        Set the value of a key.
        """
        if isinstance(value, (dict, list)):
            value = json.dumps(value, indent=4)
        self.client.set(key, str(value))

    def get(self, key: str, parse_type: Optional[str] = "json") -> Any:
        """
        Get the value of a key.
        """
        value = self.client.get(key)
        if not value:
            return None
        value = value.decode("utf-8")
        if parse_type:
            if parse_type == "json":
                return json.loads(value)
            elif parse_type == "int":
                return int(value)
            elif parse_type == "bool":
                return value.lower() in ("true", "1")
            elif parse_type == "str":
                return value
        return value


cache = Cache(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
