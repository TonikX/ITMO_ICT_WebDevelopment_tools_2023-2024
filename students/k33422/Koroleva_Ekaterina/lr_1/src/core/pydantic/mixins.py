from pydantic import ConfigDict


class SolidMixin:
    """Strict and frozen model config"""

    model_config = ConfigDict(
        frozen=True,
        strict=True
    )
