import os
import requests
import streamlit
from dotenv import load_dotenv

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
        streamlit.error(f"API-Anfragefehler: {response.status_code}")
        return []

# Rezeptdetails abrufen
def get_recipe_details(id):
    url = f"{BASE_URL}/{id}/information"
    params = {
        "apiKey": API_KEY,
        "addRecipeInformation": True,
        # TODO noch weitere Parameter für die Rezeptdetails anzeigen (Zubereitung, Kalorien, Portionen, etc.)
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        ingredients = [ingre["original"] for ingre in data.get("extendedIngredients", [])]  # 'original' --> formatierter Text
        servings = data.get("servings", "no serving information")
        instrucions = data.get("instructions", "no Instructions")
        
        instruction_steps = []
        for instr in data.get("analyzedInstructions", []):
            for step in instr.get("steps", []):
                instruction_steps.append(step["step"])    
        if not instruction_steps:
            instruction_steps = [data.get("instructions", "no instructions")]
            
        return ingredients, servings, instruction_steps
    else:
        streamlit.error(f"API-Anfragefehler: {response.status_code}")
        return [],[],[]


# Streamlit-UI
streamlit.title("Spoonacular Recipe Finder")
query = streamlit.text_input("Search recipe", "Pasta")  # Suchfeld
max_results = streamlit.slider("Number of results", 1, 20, 5)   # Slider Ergebnisanzahl

# Button suchen von Rezepten
if streamlit.button("Search recipes"):
    streamlit.session_state["recipes"] = search_recipes(query, number = max_results)    # Aufruf der Suchfunktion

    
if "recipes" in streamlit.session_state:
    # Anzeige Rezepttitel und Bild
    for rec in streamlit.session_state["recipes"]:
        streamlit.subheader(rec["title"])
        streamlit.image(rec["image"], width=300)
        
        # Button Rezeptdetails anzeigen
        with streamlit.expander("Show recipe details"):
            ingredients, servings, instructions = get_recipe_details(rec["id"]) # Aufruf Detailanzeige Funktion
            if ingredients or servings or instructions:
                streamlit.write("### Ingredients")
                for ingre in ingredients:
                    if isinstance(ingre, dict):
                        streamlit.write("- ", ingre["original"])    # falls dict
                    else:
                        streamlit.write("-", ingre) # falls String
                streamlit.write("### Servings")
                streamlit.write(servings)
                streamlit.write("### Instructions")
                if isinstance(instructions, list):
                    for i, step in enumerate(instructions, start=1):
                        streamlit.markdown(f"{i}. {step}")
                else:
                    streamlit.markdown(instructions, unsafe_allow_html=True)
                        
                        
                        
    
    
        
                    
                
                 
                        
                     