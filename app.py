import os
import requests
import streamlit
import pandas as pd
from dotenv import load_dotenv
from db import save_favorite_recipes, get_favorite_recipes, delete_favorite_recipe

# API Key aus .env-Datei laden
load_dotenv()
API_KEY = os.getenv("SPOONACULAR_KEY")

BASE_URL = "https://api.spoonacular.com/recipes"

# Rezept anhand Suchbegriffes suchen
def search_recipes(name, number):
    url = f"{BASE_URL}/complexSearch"
    params = {
        "apiKey": API_KEY,
        "query": name,  # Suchbegriff
        "number": number    # Ergebnisanzahl
    }
    
    response = requests.get(url, params=params)
    
    # Statuscode 200 --> Anfrage wurde erfolgreich vom Server verarbeitet
    if response.status_code == 200:
        return response.json().get("results", []) # Rückgabe der Suchtreffer
    else:
        streamlit.error(f"API-Error: {response.status_code}")
        return []

# Rezeptdetails abrufen
def get_recipe_details(id):
    url = f"{BASE_URL}/{id}/information"
    params = {
        "apiKey": API_KEY,
        "includeNutrition": False,  # Nährwertangaben nicht darstellen
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        streamlit.error(f"API-Error: {response.status_code}")
        return []


# Streamlit-UI
streamlit.title("Spoonacular Recipe Finder")
query = streamlit.text_input("Search recipe", "Pasta")  # Suchfeld
max_results = streamlit.slider("Number of results", 1, 20, 5)   # Slider Ergebnisanzahl

# Button suchen von Rezepten
if streamlit.button("Search recipes"):
    streamlit.session_state["recipes"] = search_recipes(query, number = max_results)    # Aufruf der Suchfunktion
    
if streamlit.button("Show saved recipes"):
    streamlit.session_state["favorites"] = get_favorite_recipes()
if "favorites" in streamlit.session_state:
    favorites = streamlit.session_state["favorites"]
    df = pd.DataFrame(favorites)
    streamlit.dataframe(df)
    id = [fav[0] for fav in favorites]
    selected_id = streamlit.selectbox("Delete chosen recipe", id)
    
    if streamlit.button("Delete recipe"):
        delete_favorite_recipe(selected_id)
        streamlit.success(f"Recipe {selected_id} deleted!")     
        
        streamlit.session_state["favorites"] = get_favorite_recipes()       
else:
    streamlit.info("no saved recipes")

if "recipes" in streamlit.session_state:
    # Anzeige Rezepttitel und Bild
    for rec in streamlit.session_state["recipes"]:
        streamlit.subheader(rec["title"])
        streamlit.image(rec["image"], width=300)
        
        # Button Rezeptdetails anzeigen
        with streamlit.expander("Show recipe details"):
            detail = get_recipe_details(rec["id"])
            if detail:
                for ingre in detail.get("extendedIngredients", []):
                    streamlit.write("- ", ingre["original"])
            
                streamlit.write("### Servings")
                streamlit.write(detail.get("servings", "no serving information"))
                
                streamlit.write("### Instructions")
                instructions = []
                for ins in detail.get("analyzedInstructions", []):
                    for step in ins.get("steps", []):
                        instructions.append(step["step"])
                if instructions:
                    for i, step in enumerate(instructions, start=1):
                        streamlit.markdown(f"{i}.  {step}")
                else:
                    streamlit.markdown(detail.get("instructions", "no instructions"))
        if streamlit.button(f"Save recipe: " + rec['title'], key=f"fav{rec['id']}"):
            detail = get_recipe_details(rec["id"])
            if detail:
                save_favorite_recipes(rec["id"], detail)
                streamlit.success(f"{rec['title']} has been saved!")
            


                        
                        
                        
    
    
        
                    
                
                 
                        
                     