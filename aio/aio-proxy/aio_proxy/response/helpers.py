import json


def serialize_error_text(text: str) -> str:
    """Serialize a text string to a JSON formatted string."""
    message = {"erreur": text}
    return json.dumps(message)


def get_value(dict, key, default=None):
    """Set value to value of key if key found in dict, otherwise set value to
    default."""
    value = dict[key] if key in dict else default
    return value


def format_collectivite_territoriale(
    colter_code=None, colter_code_insee=None, colter_elus=None, colter_niveau=None
):
    if colter_code is None:
        return None
    else:
        return {
            "code": colter_code,
            "code_insee": colter_code_insee,
            "elus": format_elus(colter_elus),
            "niveau": colter_niveau,
        }


def format_dirigeants(dirigeants_pp=None, dirigeants_pm=None):
    dirigeants = []
    if dirigeants_pp:
        for dirigeant_pp in dirigeants_pp:
            annee_de_naissance = (
                get_value(dirigeant_pp, "date_naissance")[:4]
                if get_value(dirigeant_pp, "date_naissance")
                else None
            )

            dirigeant = {
                "nom": get_value(dirigeant_pp, "nom"),
                "prenoms": get_value(dirigeant_pp, "prenoms"),
                "annee_de_naissance": annee_de_naissance,
                "qualite": get_value(dirigeant_pp, "qualite"),
                "type_dirigeant": "personne physique",
            }
            dirigeants.append(dirigeant)
    if dirigeants_pm:
        for dirigeant_pm in dirigeants_pm:
            sigle = (
                get_value(dirigeant_pm, "sigle")
                if get_value(dirigeant_pm, "sigle") != ""
                else None
            )
            dirigeant = {
                "siren": get_value(dirigeant_pm, "siren"),
                "denomination": get_value(dirigeant_pm, "denomination"),
                "sigle": sigle,
                "qualite": get_value(dirigeant_pm, "qualite"),
                "type_dirigeant": "personne morale",
            }
            dirigeants.append(dirigeant)
    return dirigeants


def format_elus(elus=None):
    format_elus = []
    if elus:
        for elu in elus:
            annee_de_naissance = (
                get_value(elu, "date_naissance")[:4]
                if get_value(elu, "date_naissance")
                else None
            )

            format_elu = {
                "nom": get_value(elu, "nom"),
                "prenoms": get_value(elu, "prenom"),
                "annee_de_naissance": annee_de_naissance,
                "fonction": get_value(elu, "fonction"),
                "sexe": get_value(elu, "sexe"),
            }
            format_elus.append(format_elu)
    return format_elus


def format_etablissement(source_etablissement):
    formatted_etablissement = {
        "activite_principale": get_value(source_etablissement, "activite_principale"),
        "activite_principale_registre_metier": get_value(
            source_etablissement, "activite_principale_registre_metier"
        ),
        "cedex": get_value(source_etablissement, "cedex"),
        "code_pays_etranger": get_value(source_etablissement, "code_pays_etranger"),
        "code_postal": get_value(source_etablissement, "code_postal"),
        "commune": get_value(source_etablissement, "commune"),
        "complement_adresse": get_value(source_etablissement, "complement_adresse"),
        "date_creation": get_value(source_etablissement, "date_creation"),
        "date_debut_activite": get_value(source_etablissement, "date_debut_activite"),
        "distribution_speciale": get_value(
            source_etablissement, "distribution_speciale"
        ),
        "enseigne_1": get_value(source_etablissement, "enseigne_1"),
        "enseigne_2": get_value(source_etablissement, "enseigne_2"),
        "enseigne_3": get_value(source_etablissement, "enseigne_3"),
        "est_source_etablissement": get_value(
            source_etablissement, "est_source_etablissement"
        ),
        "etat_administratif": get_value(source_etablissement, "etat_administratif"),
        "geo_adresse": get_value(source_etablissement, "geo_adresse"),
        "geo_id": get_value(source_etablissement, "geo_id"),
        "indice_repetition": get_value(source_etablissement, "indice_repetition"),
        "latitude": get_value(source_etablissement, "latitude"),
        "libelle_cedex": get_value(source_etablissement, "libelle_cedex"),
        "libelle_commune": get_value(source_etablissement, "libelle_commune"),
        "libelle_commune_etranger": get_value(
            source_etablissement, "libelle_commune_etranger"
        ),
        "libelle_pays_etranger": get_value(
            source_etablissement, "libelle_pays_etranger"
        ),
        "libelle_voie": get_value(source_etablissement, "libelle_voie"),
        "liste_finess": get_value(source_etablissement, "liste_finess"),
        "liste_idcc": get_value(source_etablissement, "liste_idcc"),
        "liste_rge": get_value(source_etablissement, "liste_rge"),
        "liste_uai": get_value(source_etablissement, "liste_uai"),
        "longitude": get_value(source_etablissement, "longitude"),
        "nom_commercial": get_value(source_etablissement, "nom_commercial"),
        "numero_voie": get_value(source_etablissement, "numero_voie"),
        "siret": get_value(source_etablissement, "siret"),
        "tranche_effectif_salarie": get_value(
            source_etablissement, "tranche_effectif_salarie"
        ),
        "type_voie": get_value(source_etablissement, "type_voie"),
        "adresse": get_value(source_etablissement, "adresse"),
        "coordonnees": get_value(source_etablissement, "coordonnees"),
        "departement": get_value(source_etablissement, "departement"),
    }
    return formatted_etablissement


def format_etablissements(etablissements=None):
    complements = {
        "liste_uai": False,
        "liste_rge": False,
        "liste_finess": False,
        "liste_idcc": False,
    }
    etablissements_formatted = []
    if etablissements:
        for etablissement in etablissements:
            etablissement_formatted = format_etablissement(etablissement)
            # We use the iteration over etablissements to buid the boolean variables
            # (est_uai, est_rge, est_finess, convention_collective_renseignee
            for field in ["liste_rge", "liste_finess", "liste_uai", "liste_idcc"]:
                if get_value(etablissement_formatted, field):
                    complements[field] = True
            etablissements_formatted.append(etablissement_formatted)
    return etablissements_formatted, complements


def format_siege(siege=None):
    siege_formatted = format_etablissement(siege)
    return siege_formatted


def format_bool_field(value):
    if value is None:
        return False
    else:
        return True


def format_ess(value):
    if value is None or value == "N":
        return False
    else:
        return True
