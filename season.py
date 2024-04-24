import datetime
from typing import Optional

import requests


def find_season(city: Optional[str] = None) -> str:
    date = datetime.datetime.now()
    
    if get_coordinates(city=city):
        month = date.month
    else:
        month = date.month + 6
    
    day = date.day
    
    if (month == 3 and day >= 20) or (month == 4) or (month == 5) or (month == 6 and day < 21):
        return "Printemps"
    elif (month == 6 and day >= 21) or (month == 7) or (month == 8) or (month == 9 and day < 23):
        return "Été"
    elif (month == 9 and day >= 23) or (month == 10) or (month == 11) or (month == 12 and day < 21):
        return "Automne"
    else:
        return "Hiver"


def get_coordinates(city: Optional[str] = None) -> Optional[bool]:
    try:
        url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json"
        
        response = requests.get(url)
        response.raise_for_status()  # Lever une exception pour les codes d'erreur HTTP
        
        data = response.json()
        if data:
            latitude = data[0]["lat"]
            if float(latitude) > 0:
                return True
            else:
                return False
        else:
            return None
    except requests.RequestException as e:
        print(f"Erreur lors de la récupération des coordonnées : {e}")
        return None
    except (KeyError, ValueError) as e:
        print(f"Erreur lors de l'analyse des données JSON : {e}")
        return None
