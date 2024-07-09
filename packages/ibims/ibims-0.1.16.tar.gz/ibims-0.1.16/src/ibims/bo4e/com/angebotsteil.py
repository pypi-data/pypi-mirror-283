from pydantic import BaseModel, ConfigDict, Field

from ..bo.marktlokation import Marktlokation
from .angebotsposition import Angebotsposition
from .betrag import Betrag
from .menge import Menge
from .zeitraum import Zeitraum


class Angebotsteil(BaseModel):
    """
    Mit dieser Komponente wird ein Teil einer Angebotsvariante abgebildet.
    Hier werden alle Angebotspositionen aggregiert.
    Angebotsteile werden im einfachsten Fall für eine Marktlokation oder Lieferstellenadresse erzeugt.
    Hier werden die Mengen und Gesamtkosten aller Angebotspositionen zusammengefasst.
    Eine Variante besteht mindestens aus einem Angebotsteil.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Angebotsteil.svg" type="image/svg+xml"></object>

    .. HINT::
        `Angebotsteil JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Angebotsteil.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    anfrage_subreferenz: str | None = Field(default=None, alias="anfrageSubreferenz", title="Anfragesubreferenz")
    gesamtkostenangebotsteil: Betrag | None = None
    gesamtmengeangebotsteil: Menge | None = None
    lieferstellenangebotsteil: list[Marktlokation] | None = Field(default=None, title="Lieferstellenangebotsteil")
    lieferzeitraum: Zeitraum | None = None
    positionen: list[Angebotsposition] | None = Field(default=None, title="Positionen")
