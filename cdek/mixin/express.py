from dataclasses import dataclass
from typing import Any


@dataclass
class ExpressMixin:
    """Mixin for creating instances from dictionaries."""
    
    @classmethod
    def express(cls, args: dict[str, Any]):
        """
        Create an instance from a dictionary.

        Args:
            args: Dictionary with attribute names as keys

        Returns:
            Instance of the class with attributes set from the dictionary
        """
        instance = cls()

        for key, value in args.items():
            if value is not None:
                setattr(instance, key, value)

        return instance
