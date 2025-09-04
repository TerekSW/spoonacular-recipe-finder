import os
from dotenv import load_dotenv
from sqlalchemy import *

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "recipedb")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

metadata = MetaData()

favorite_recipes = Table(
    "favorite_recipes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String),
    Column("cuisine", String),
    Column("dish_type", String),
    Column("servings", Integer),
    Column("source_url", String)
)

metadata.create_all(engine)

def save_favorite_recipes(recipe_id, details):
    try:
        with engine.begin() as con:
            insert_stmt = favorite_recipes.insert().values(
                id = recipe_id,
                title = details["title"],
                servings = details["servings"],
                cuisine = details.get("cuisines", [""])[0] if details.get("cuisines") else None, # optionaler Wert
                dish_type = details.get("dishTypes", [""])[0] if details.get("dishTypes") else None, # optionaler Wert
                source_url = details.get("sourceUrl")
            )
            con.execute(insert_stmt)
    except Exception as ex:
        print(f"Error while saving: {ex}")

def get_favorite_recipes():
    with engine.connect() as con:
        result = con.execute(favorite_recipes.select())
        return result.fetchall()