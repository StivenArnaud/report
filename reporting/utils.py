from datetime import datetime, timedelta, timezone


def temps_restant_jour(date_report: datetime):
    # Obtenir l'heure actuelle avec le fuseau horaire local
    temps_restant = None
    maintenant = date_report.astimezone()

    # Calculer le début du jour suivant (minuit)
    debut_demain = (maintenant + timedelta(days=1)).replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    if datetime.now().astimezone() >= debut_demain:
        temps_restant = None
        return temps_restant

    # Calculer la différence
    temps_restant = debut_demain - datetime.now().astimezone()

    return temps_restant