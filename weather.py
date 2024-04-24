import requests

# Faire une requête HTTP à l'URL fournie
response = requests.get("https://wttr.in/location?format=%C")

# Vérifier si la requête a réussi (code 200)
if response.status_code == 200:
    # Récupérer le contenu de la réponse
    weather_condition = response.text
    print("Condition météorologique:", weather_condition)
else:
    print("La requête a échoué avec le code:", response.status_code)
