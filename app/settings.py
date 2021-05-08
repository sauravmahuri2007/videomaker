import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
TEMP_DIR = BASE_DIR / 'temp_files'  # this is how you join two paths using pathlib

# Make sure TEMP_DIR path exists:
TEMP_DIR.mkdir(parents=True, exist_ok=True)