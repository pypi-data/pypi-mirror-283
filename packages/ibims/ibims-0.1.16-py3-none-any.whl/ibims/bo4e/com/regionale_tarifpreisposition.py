from pydantic import BaseModel, ConfigDict, Field

from ..enum.mengeneinheit import Mengeneinheit
from ..enum.preistyp import Preistyp
from ..enum.waehrungseinheit import Waehrungseinheit
from .regionale_preisstaffel import RegionalePreisstaffel


class RegionaleTarifpreisposition(BaseModel):
    """
    Mit dieser Komponente können Tarifpreise verschiedener Typen im Zusammenhang mit regionalen Gültigkeiten abgebildet
    werden.

    .. raw:: html

        <object data="../_static/images/bo4e/com/RegionaleTarifpreisposition.svg" type="image/svg+xml"></object>

    .. HINT::
        `RegionaleTarifpreisposition JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/RegionaleTarifpreisposition.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    bezugseinheit: Mengeneinheit | None = None
    einheit: Waehrungseinheit | None = None
    mengeneinheitstaffel: Mengeneinheit | None = None
    preisstaffeln: list[RegionalePreisstaffel] | None = Field(default=None, title="Preisstaffeln")
    preistyp: Preistyp | None = None
