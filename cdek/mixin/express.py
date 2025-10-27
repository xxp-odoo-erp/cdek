from dataclasses import dataclass
from typing import Any


@dataclass
class Express:

    @classmethod
    def express(cls, args: dict[str, Any]):
        instance = cls()

        for key, value in args.items():
            if value is not None:
                setattr(instance, key, value)

        return instance
