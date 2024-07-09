from pydantic import BaseModel, ConfigDict, Field

from ..enum.sparte import Sparte


class TransaktionsdatenQuantities(BaseModel):
    """
    This class adds additional data to the transaktionsdaten, which is needed for an energy amount
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    migration_id: str | None = Field(default=None, title="Migration_id")
    import_fuer_storno_adhoc: str | None = Field(default=None, title="Import_fuer_storno_adhoc")
    sparte: Sparte | None = Field(default=None, title="Sparte")
    pruefidentifikator: str | None = Field(default=None, title="Pruefidentifikator")
    datenaustauschreferenz: str | None = Field(default=None, title="Datenaustauschreferenz")
    nachrichtendatum: str | None = Field(default=None, title="Nachrichtendatum")
    nachrichten_referenznummer: str | None = Field(default=None, title="Nachrichten_referenznummer")
    absender: str | None = Field(default=None, title="Absender")
    empfaenger: str | None = Field(default=None, title="Empfaenger")
    dokumentennummer: str | None = Field(default=None, title="Dokumentennummer")
    kategorie: str | None = Field(default=None, title="Kategorie")
    nachrichtenfunktion: str | None = Field(default=None, title="Nachrichtenfunktion")
    typ: str | None = Field(default=None, title="Typ")
    datumsformat: str | None = Field(default=None, title="Datumsformat")
    status: str | None = Field(default=None, title="Status")
