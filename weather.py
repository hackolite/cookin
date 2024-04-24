import requests
import json
from typing import Optional, Dict, Any

def get_weather(city: Optional[str] = None) -> Dict[str, Any]:
    # Faire une requête HTTP à l'URL fournie
    weather_api = f"https://wttr.in/{city}?format=j1"
    response = requests.get(weather_api)
    
    # Vérifier si la requête a réussi (code 200)
    if response.status_code == 200:
        # Récupérer le contenu de la réponse
        weather_condition = response.text
        json_data = json.loads(weather_condition) 
        return json_data['current_condition'][0]
    else:
        print("La requête a échoué avec le code:", response.status_code)
        return {"error": "La requête a échoué"}
