# spoonacular-recipe-finder

Small Python web application built with Streamlit using the Spoonacular API.

Features include:
- Recipe search
- Recipe details (ingredients, servings, instructions)
- Save favorite recipes in PostgreSQL
- View and delete saved favorites


---


## Demo (local)

# 1. Clone the repository 
```bash
git clone https://github.com/TerekSW/spoonacular-recipe-finder
```
# 2. (Optional) create virtual environment
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```
# 3. Install dependencies
```bash
pip install -r requirements.txt
```
# 4. Add configuration file (.env) (see below)


## Configuration (.env)

# Spoonacular API

SPOONACULAR_KEY=your_api_key 

# PostgreSQL

DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=recipedb

# Get your free API-Key [here](https://spoonacular.com/food-api) 

⚠️ Do not commit .env to GitHub (add to .gitignore).

## Database setup (PostgreSQL)

Login to PostgreSQL:
```bash
psql -U postgres -d postgres

CREATE DATABASE recipedb;
```
## Run the app
```bash
streamlit run app.py
```

## Requirements 

Install with:
```bash
pip install -r requirements.txt
```

Contents of requirements.txt:

streamlit>=1.34
requests>=2.31
python-dotenv>=1.0
SQLAlchemy>=2.0
psycopg2-binary>=2.9
pandas>=2.0
