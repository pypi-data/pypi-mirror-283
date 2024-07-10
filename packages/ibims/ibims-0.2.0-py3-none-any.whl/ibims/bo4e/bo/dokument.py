from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from ..enum.typ import Typ
from ..zusatz_attribut import ZusatzAttribut


class Dokument(BaseModel):
    """
    A generic document reference like for bills, order confirmations and cancellations
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    versionstruktur: str | None = Field(default="2", title="Versionstruktur")
    bo_typ: Typ | None = Field(default=Typ.GESCHAEFTSOBJEKT, alias="boTyp")
    externe_referenzen: list[ZusatzAttribut] | None = Field(
        default=None, alias="externeReferenzen", title="Externereferenzen"
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    erstellungsdatum: datetime = Field(..., title="Erstellungsdatum")
    has_been_sent: bool = Field(..., alias="hasBeenSent", title="Hasbeensent")
    dokumentenname: str = Field(..., title="Dokumentenname")
    vorlagenname: str = Field(..., title="Vorlagenname")
