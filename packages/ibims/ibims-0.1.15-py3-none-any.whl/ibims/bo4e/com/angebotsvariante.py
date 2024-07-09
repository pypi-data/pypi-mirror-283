from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from ..enum.angebotsstatus import Angebotsstatus
from .angebotsteil import Angebotsteil
from .betrag import Betrag
from .menge import Menge


class Angebotsvariante(BaseModel):
    """
    Führt die verschiedenen Ausprägungen der Angebotsberechnung auf

    .. raw:: html

        <object data="../_static/images/bo4e/com/Angebotsvariante.svg" type="image/svg+xml"></object>

    .. HINT::
        `Angebotsvariante JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Angebotsvariante.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    angebotsstatus: Angebotsstatus | None = None
    bindefrist: datetime | None = Field(default=None, title="Bindefrist")
    erstellungsdatum: datetime | None = Field(default=None, title="Erstellungsdatum")
    gesamtkosten: Betrag | None = None
    gesamtmenge: Menge | None = None
    teile: list[Angebotsteil] | None = Field(default=None, title="Teile")
