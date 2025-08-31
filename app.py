import os
import requests
import streamlit
from dotenv import load_dotenv

# API Key aus .env-Datei laden
load_dotenv()
api_key = os.getenv("SPOONACULAR_KEY")

base_url = "https://api.spoonacular.com/recipes"

# Rezept anhand Suchbegriffes suchen
def search_recipes(name, number):
    url = f"{base_url}/complexSearch"
    params = {
        "apiKey": api_key,
        "query": name,  # Suchbegriff
        "number": number    # Ergebnisanzahl
    }
    
    response = requests.get(url, params=params)
    
    # Statuscode 200 --> Anfrage wurde erfolgreich vom Server verarbeitet
    if response.status_code == 200:
        return response.json().get("results", []) # Rückgabe der Suchtreffer
    else:
        streamlit.error(f"API-Anfragefehler: {response.status_code}")
        return []

# Rezeptdetails abrufen
def get_recipe_details(id):
    url = f"{base_url}/{id}/information"
    params = {
        "apiKey": api_key,
        # TODO noch weitere Parameter für die Rezeptdetails anzeigen (Zubereitung, Kalorien, Portionen, etc.)
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        ingredients = [ingre["original"] for ingre in data.get("extendedIngredients", [])]  # 'original' --> formatierter Text
        return ingredients
    else:
        streamlit.error(f"API-Anfragefehler: {response.status_code}")
        return []


# Streamlit-UI
streamlit.title("Spoonacular Recipe Finder")
query = streamlit.text_input("Rezept suchen", "Pasta")  # Suchfeld
max_results = streamlit.slider("Anzahl der Ergebnisse", 1, 20, 5)   # Slider Ergebnisanzahl

# Button suchen von Rezepten
if streamlit.button("Rezepte finden"):
    streamlit.session_state["recipes"] = search_recipes(query, number = max_results)    # Aufruf der Suchfunktion

    
if "recipes" in streamlit.session_state:
    # Anzeige Rezepttitel und Bild
    for rec in streamlit.session_state["recipes"]:
        streamlit.subheader(rec["title"])
        streamlit.image(rec["image"], width=300)
        
        # Button Rezeptdetails anzeigen
        if streamlit.button(f"Rezeptdetails zu {rec['title']}", key=rec["id"]):
            ingredients = get_recipe_details(rec["id"]) # Aufruf Detailanzeige Funktion
            if ingredients:
                streamlit.write("### Zutaten")
                for ingre in ingredients:
                    if isinstance(ingre, dict):
                        streamlit.write("- ", ingre["original"])    # falls dict
                    else:
                        streamlit.write("-", ingre) # falls String
    
    
        
                    
                
                 
                        
                     