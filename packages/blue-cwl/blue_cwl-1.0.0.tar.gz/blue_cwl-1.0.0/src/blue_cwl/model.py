# SPDX-License-Identifier: Apache-2.0

"""Custom Base Model for pydantic classes."""

import pydantic

_PYDANTIC_MAJOR = int(pydantic.__version__.split(".", maxsplit=1)[0])


class CustomBaseModel(pydantic.BaseModel):
    """Custom Model Config."""

    class Config:
        """Custom Model Config."""

        frozen = True
        extra = pydantic.Extra.forbid
        validate_assignment = True
        arbitrary_types_allowed = True

    @classmethod
    def from_dict(cls, obj):
        """Convert object to model instance."""
        return cls.model_validate(obj) if _PYDANTIC_MAJOR > 1 else cls.parse_obj(obj)

    def to_dict(self) -> dict:
        """Convert the object into a dict."""
        return self.model_dump() if _PYDANTIC_MAJOR > 1 else self.dict()

    def to_json(self) -> str:
        """Serialize the object to JSON."""
        return self.model_dump_json() if _PYDANTIC_MAJOR > 1 else self.json()
