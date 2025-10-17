import pandas as pd
from datetime import datetime, date, timedelta

def get_presence_data(file_path):
    mois_map = {
        "janv.": "01", "févr.": "02", "mars": "03", "avr.": "04",
        "mai": "05", "juin": "06", "juil.": "07", "août": "08",
        "sept.": "09", "oct.": "10", "nov.": "11", "déc.": "12"
    }

    def convert_date(date_str):
        try:
            jour, mois_txt, annee = date_str.split("-")
            mois_num = mois_map.get(mois_txt.strip().lower(), "01")
            return f"{annee}/{mois_num}/{jour.zfill(2)}"
        except Exception:
            return date_str

    # Lecture du fichier Excel
    excel_data = pd.ExcelFile(file_path)
    df = excel_data.parse(excel_data.sheet_names[0])
    df.columns = df.columns.str.strip()

    # Conversion en format texte normalisé
    df["Date"] = df["Date"].astype(str).apply(convert_date)

    # Conversion en objet date Python
    df["Date"] = df["Date"].apply(
        lambda d: datetime.strptime(d, "%Y/%m/%d").date() if "/" in d else None
    )
    date_month = df.iloc[0].to_dict()['Date'].strftime("%Y-%m")

    # Convertir les dates en texte pour JSON
    df["Date"] = df["Date"].apply(lambda d: d.strftime("%Y-%m-%d") if isinstance(d, date) else d)

    # Groupement par prénom
    data = []
    for prenom, group in df.groupby("Prénom"):
        records = group.to_dict(orient="records")
        data.append({prenom: records})

    return date_month, data



def calculer_retard_et_sup_par_jour(data):
    # Références horaires
    debut_service = datetime.strptime("08:00", "%H:%M").time()
    tolerance = datetime.strptime("08:30", "%H:%M").time()
    fin_service = datetime.strptime("17:00", "%H:%M").time()
    sup_debut = datetime.strptime("17:30", "%H:%M").time()

    resultats = {}

    for employe in data:
        for prenom, records in employe.items():
            # Trier les enregistrements par date et temps
            records = sorted(records, key=lambda x: (x["Date"], x["Temps"]))

            # Groupement par jour
            par_jour = {}
            for rec in records:
                date = rec["Date"]
                if date not in par_jour:
                    par_jour[date] = []
                par_jour[date].append(rec)

            details = []
            total_retard = timedelta(0)
            total_sup = timedelta(0)
            total_dettes = timedelta(0)

            for date, events in par_jour.items():
                entrees = [e for e in events if e["Etat du Ptg"].upper() == "ENTREE"]
                sorties = [e for e in events if e["Etat du Ptg"].upper() == "SORTIE"]

                retard = timedelta(0)
                heure_sup = timedelta(0)
                heures_dettes = timedelta(0)

                # Calcul du retard
                if entrees:
                    premiere_entree = datetime.strptime(entrees[0]["Temps"], "%H:%M").time()
                    if premiere_entree > tolerance:
                        retard = datetime.combine(datetime.today(), premiere_entree) - datetime.combine(datetime.today(), tolerance)

                # Gestion de l'absence de sortie
                if sorties:
                    derniere_sortie = datetime.strptime(sorties[-1]["Temps"], "%H:%M").time()
                else:
                    # Si aucune sortie, on suppose sortie à 17:00
                    derniere_sortie = fin_service

                # Calcul des heures sup ou dettes
                if derniere_sortie > sup_debut:
                    heure_sup = datetime.combine(datetime.today(), derniere_sortie) - datetime.combine(datetime.today(), sup_debut)
                elif derniere_sortie < fin_service:
                    heures_dettes = datetime.combine(datetime.today(), fin_service) - datetime.combine(datetime.today(), derniere_sortie)

                # Ajout aux totaux
                total_retard += retard
                total_sup += heure_sup
                total_dettes += heures_dettes

                # Formatage des durées
                def fmt(td):
                    heures = td.seconds // 3600
                    minutes = (td.seconds // 60) % 60
                    return f"{heures}h {minutes:02d}min"

                details.append({
                    "Date": date,
                    "Retard": fmt(retard),
                    "HeureSup": fmt(heure_sup),
                    "heures_dettes": fmt(heures_dettes)
                })

            # Résumé total par employé
            def fmt(td):
                heures = td.seconds // 3600
                minutes = (td.seconds // 60) % 60
                return f"{heures}h {minutes:02d}min"

            resultats[prenom] = {
                "data": employe[prenom],
                "details": details,
                "total_retard": fmt(total_retard),
                "total_heures_sup": fmt(total_sup),
                "total_dettes": fmt(total_dettes)
            }

    return resultats
