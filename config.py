import os

# --- Configuration ---
API_KEY = os.environ.get("CEREBRAS_API_KEY")
MODEL_NAME = "qwen-3-32b"
OPTIONS_SEPARATOR = "--- Options ---"

# Define genre options
GENRE_OPTIONS = ["Fantasy", "Sci-Fi", "Medieval", "Mystery", "Horror", "Western"]
