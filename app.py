import os
import requests
import streamlit
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("SPOONACULAR_KEY")

