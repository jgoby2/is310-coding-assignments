# CLI Data Entry App

A command-line Python script that shows some example movie data, lets the user enter their own movies, confirms each entry, and saves the confirmed entries to a CSV file.

## Files

- `cli_data_entry.py` – the CLI application
- `requirements.txt` – the packages needed to run it
- `movies.csv` – created automatically the first time you save an entry

## Setup

1. Make sure Python 3 is installed.
2. (Optional) Create and activate a virtual environment:
   ```
   py -m venv venv
   venv\Scripts\activate
   ```
3. Install the required packages:
   ```
   py -m pip install -r requirements.txt
   ```

## How to Run

From the folder that contains the script:

```
py cli_data_entry.py
```

## How It Works

1. The script uses the `Rich` library to display a table of example Star Wars movies with Released, Title, and Box Office.
2. It asks the user to enter a movie's release date, title, and box office earnings. Blank answers are not accepted.
3. It shows the entry back in a table and asks the user to confirm it is correct by using a y/n prompt.
   - If the user says **yes**, the entry is saved to `movies.csv`.
   - If the user says **no**, they re-enter that movie.
4. After each saved entry, the user can choose to add another movie or stop.
5. When finished, the script prints how many entries were saved and the full path to the CSV file.

## Output Format

Data is saved as a CSV file with these columns:

| Released | Title | Box Office |
|----------|-------|------------|

New entries are appended, so running the script again allows the user to put another movie in the CSV file.

## Development Pathway

This assignment was drafted using pathway 1. No AI was used for this assignment.
