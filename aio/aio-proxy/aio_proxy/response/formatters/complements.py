from dataclasses import asdict

from aio_proxy.response.unite_legale_model import UniteLegaleComplements


def format_complements(
    collectivite_territoriale,
    convention_collective_renseignee,
    egapro_renseignee,
    est_bio,
    est_entrepreneur_individuel,
    est_entrepreneur_spectacle,
    est_ess,
    est_finess,
    est_organisme_formation,
    est_qualiopi,
    liste_id_organisme_formation,
    est_rge,
    est_service_public,
    est_societe_mission,
    est_uai,
    identifiant_association,
    statut_entrepreneur_spectacle,
):
    return asdict(
        UniteLegaleComplements(
            collectivite_territoriale=collectivite_territoriale,
            convention_collective_renseignee=convention_collective_renseignee,
            egapro_renseignee=egapro_renseignee,
            est_bio=est_bio,
            est_entrepreneur_individuel=est_entrepreneur_individuel,
            est_entrepreneur_spectacle=est_entrepreneur_spectacle,
            est_ess=est_ess,
            est_finess=est_finess,
            est_organisme_formation=est_organisme_formation,
            est_qualiopi=est_qualiopi,
            liste_id_organisme_formation=liste_id_organisme_formation,
            est_rge=est_rge,
            est_service_public=est_service_public,
            est_societe_mission=est_societe_mission,
            est_uai=est_uai,
            identifiant_association=identifiant_association,
            statut_entrepreneur_spectacle=statut_entrepreneur_spectacle,
        )
    )
