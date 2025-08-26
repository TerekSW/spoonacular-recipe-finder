import os
import requests
import streamlit
from dotenv import load_dotenv

# API Key laden
load_dotenv()
api_key = os.getenv("SPOONACULAR_KEY")

base_url = "https://api.spoonacular.com/recipes"

def search_recipes(name, number):
    url = f"{base_url}/complexSearch"
    params = {
        "apiKey": api_key,
        "query": name,
        "number": number
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        streamlit.error(f"API-Anfragefehler: {response.status_code}")
        return None
    
def get_recipe_details_by_id(id):
    url = f"{base_url}/{id}/information"
    params = {
        "apiKey": api_key,
        "includeNutrition": True,  
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        streamlit.error(f"API-Anfragefehler: {response.status_code}")
        return None


streamlit.title("Spoonacular Recipe Finder")

query = streamlit.text_input("Rezept suchen", "Pasta")

max_results = streamlit.slider("Anzahl der Ergebnisse", 1,10,20,)

if streamlit.button("Rezepte finden"):
    recipes = search_recipes(query, number=max_results)

    if recipes:
        for r in recipes:
            streamlit.subheader(r["title"])
            streamlit.image(r["image"], width=200)
            
            if streamlit.button(f"Rezeptdetails zu {r['title']}", key=r["id"]):
                info = get_recipe_details_by_id(r["id"])
                 
                        
                     