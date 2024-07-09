from pydantic import BaseModel, ConfigDict, Field


class COM(BaseModel):
    """
    base class for all components

    .. raw:: html

        <object data="../_static/images/bo4e/com/COM.svg" type="image/svg+xml"></object>

    .. HINT::
        `COM JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/COM.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
