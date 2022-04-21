import re
from typing import Dict, Optional, Tuple, Union

from aio_proxy.helper import serialize
from aio_proxy.labels.helpers import get_codes_naf, get_tranches_effectifs
from aiohttp import web


def parse_and_clean_parameter(request, param: str, default_value=None):
    param = request.rel_url.query.get(param, default_value)
    if param is None:
        return None
    param_clean = param.replace(" ", "").upper()
    return param_clean


def validate_code_postal(code_postal_clean: str) -> Optional[str]:
    if code_postal_clean is None:
        return None
    if len(code_postal_clean) != 5:
        raise ValueError("Code postal doit contenir 5 caractères !")
    # test the validity of a code_postal
    codes_valides = "^((0[1-9])|([1-8][0-9])|(9[0-8])|(2A)|(2B))[0-9]{3}$"
    if not re.search(codes_valides, code_postal_clean):
        raise ValueError("Code postal non valide.")
    return code_postal_clean


def validate_activite_principale(activite_principale_clean: str) -> Optional[str]:
    if activite_principale_clean is None:
        return None
    if len(activite_principale_clean) != 6:
        raise ValueError("Activité principale doit contenir 6 caractères.")
    # test the validity of activite_principale
    codes_naf_decoded = get_codes_naf()
    if activite_principale_clean not in codes_naf_decoded:
        raise ValueError("Activité principale inconnue.")
    return activite_principale_clean


def validate_is_entrepreneur_individuel(
    is_entrepreneur_individuel_clean: str,
) -> Optional[bool]:
    if is_entrepreneur_individuel_clean is None:
        return None
    if (is_entrepreneur_individuel_clean != "YES") and (
        is_entrepreneur_individuel_clean != "NO"
    ):
        raise ValueError(
            "Seuls les valeurs 'yes' ou bien 'no' sont possibles pour 'is_"
            "entrepreneur_individuel'."
        )
    if is_entrepreneur_individuel_clean == "YES":
        return True
    return False


def validate_tranche_effectif_salarie_entreprise(
    tranche_effectif_salarie_entreprise_clean: str,
) -> Optional[str]:
    if tranche_effectif_salarie_entreprise_clean is None:
        return None
    if len(tranche_effectif_salarie_entreprise_clean) != 2:
        raise ValueError("Tranche salariés doit contenir 2 caractères.")
    # test the validity of tranche_effectif_salarie_entreprise
    tranches_effectifs_decoded = get_tranches_effectifs()
    if tranche_effectif_salarie_entreprise_clean not in tranches_effectifs_decoded:
        raise ValueError("Tranche salariés non valide.")
    return tranche_effectif_salarie_entreprise_clean


def extract_parameters(
    request,
) -> Tuple[str, int, int, Dict[str, Union[str, None, bool]]]:
    try:
        terms = request.rel_url.query["q"]
    except KeyError:
        raise web.HTTPBadRequest(
            text=serialize(
                "Veuillez indiquer la requête avec le paramètre: " "?q=ma+recherche."
            ),
            content_type="application/json",
        )
    try:
        page = int(request.rel_url.query.get("page", 1)) - 1
        per_page = int(request.rel_url.query.get("per_page", 10))
    except ValueError as error:
        raise web.HTTPBadRequest(
            text=serialize(str(error)), content_type="application/json"
        )

    try:
        activite_principale = validate_activite_principale(
            parse_and_clean_parameter(request, param="activite_principale")
        )
        code_postal = validate_code_postal(
            parse_and_clean_parameter(request, param="code_postal")
        )
        is_entrepreneur_individuel = validate_is_entrepreneur_individuel(
            parse_and_clean_parameter(request, param="is_entrepreneur_individuel")
        )
        tranche_effectif_salarie_entreprise = (
            validate_tranche_effectif_salarie_entreprise(
                parse_and_clean_parameter(
                    request, param="tranche_effectif_salarie_entreprise"
                )
            )
        )
    except (ValueError, TypeError) as error:
        raise web.HTTPBadRequest(
            text=serialize(str(error)), content_type="application/json"
        )

    filters = {
        "activite_principale_entreprise": activite_principale,
        "code_postal": code_postal,
        "is_entrepreneur_individuel": is_entrepreneur_individuel,
        "tranche_effectif_salarie_entreprise": tranche_effectif_salarie_entreprise,
    }

    return terms, page, per_page, filters