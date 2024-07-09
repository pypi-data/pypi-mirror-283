from pydantic import BaseModel, ConfigDict, Field

from ..enum.sparte import Sparte


class TransaktionsdatenInvoices(BaseModel):
    """
    This class adds additional data to the transaktionsdaten, which is needed for an invoice
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    migration_id: str | None = Field(default=None, title="Migration_id")
    import_fuer_storno_adhoc: str = Field(..., title="Import_fuer_storno_adhoc")
    sparte: Sparte = Field(..., title="Sparte")
    pruefidentifikator: str = Field(..., title="Pruefidentifikator")
    datenaustauschreferenz: str = Field(..., title="Datenaustauschreferenz")
    nachrichtendatum: str = Field(..., title="Nachrichtendatum")
    nachrichten_referenznummer: str = Field(..., title="Nachrichten_referenznummer")
    absender: str = Field(..., title="Absender")
    empfaenger: str = Field(..., title="Empfaenger")
    lieferrichtung: str | None = Field(default=None, title="Lieferrichtung")
    referenznummer: str | None = Field(default=None, title="Referenznummer")
    duplikat: str = Field(..., title="Duplikat")
    status: str = Field(..., title="Status")
