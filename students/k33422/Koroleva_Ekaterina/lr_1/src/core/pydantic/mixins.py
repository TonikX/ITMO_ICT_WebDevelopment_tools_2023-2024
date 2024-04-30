from pydantic import ConfigDict


class SolidMixin:
    """Frozen model config"""

    model_config = ConfigDict(
        frozen=True,
    )


class UnionMixin:
    """From_attributes model config"""

    model_config = ConfigDict(
        from_attributes=True
    )


class SolidUnionMixin:
    """Frozen and from_attributes model config"""

    model_config = ConfigDict(
        frozen=True,
        from_attributes=True
    )
