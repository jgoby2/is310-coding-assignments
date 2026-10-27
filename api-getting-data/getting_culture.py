"""
GETting Culture Across APIs
IS 310 — api-getting-data/getting_culture.py

Two APIs:
  1. Bulbapedia's MediaWiki Action API (a fan-run Pokémon wiki)
  2. PokéAPI (a community-run, open REST API of Pokémon game data)

The connection: for each Pokémon, I look up its official data and its
official names in other languages on PokéAPI, then find the matching
Bulbapedia article and compare how much the fan wiki writes about it and
which other-language wikis it links to.

Install:  python -m pip install requests beautifulsoup4 rich
No API keys are needed for either API.
"""

import csv
import json
import time

import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table

console = Console()

# Identify the script honestly and give a way to contact you (same practice as the lesson).
HEADERS = {
    "User-Agent": "is310-course/1.0 (https://jgoby2.github.io; jgoby2@illinois.edu)"
}

BULBAPEDIA_API_URL = "https://bulbapedia.bulbagarden.net/w/api.php"
POKEAPI_URL = "https://pokeapi.co/api/v2"

# A mix of easy and awkward cases. The awkward names (punctuation, gender
# symbols) are deliberate: they test whether the two APIs agree on identity.
# "missingno" is a famous glitch Pokémon that PokéAPI does not include,
# so it shows the error handling working.
POKEMON = ["pikachu", "mr-mime", "farfetchd", "nidoran-f", "sprigatito", "missingno"]

PAUSE_SECONDS = 1  # be polite: one request at a time, with a short pause


# ---------------------------------------------------------------------------
# Helper: one safe GET request that never crashes the script
# ---------------------------------------------------------------------------
def get_json(url, params=None):
    """Return parsed JSON, or None if anything goes wrong."""
    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=15)
    except requests.RequestException as error:
        console.print(f"[red]Request failed for {url}: {error}[/red]")
        return None

    if response.status_code != 200:
        console.print(f"[red]{response.status_code} from {response.url}[/red]")
        return None

    try:
        return response.json()
    except ValueError:
        # Some sites answer bots with an HTML challenge page instead of JSON.
        console.print(f"[red]Response from {response.url} was not JSON (possible bot protection).[/red]")
        return None


# ---------------------------------------------------------------------------
# Part 1: Query the MediaWiki Action API (Bulbapedia)
# ---------------------------------------------------------------------------
def get_category_members(category, limit=20):
    data = get_json(BULBAPEDIA_API_URL, params={
        "action": "query",
        "list": "categorymembers",
        "cmtitle": category,
        "cmtype": "page",
        "cmlimit": limit,
        "format": "json",
    })
    if data is None or "error" in data:
        return []
    return data["query"]["categorymembers"]


def analyze_bulbapedia_page(title):
    """Same measures as the lesson: words, characters, links, language links."""
    data = get_json(BULBAPEDIA_API_URL, params={
        "action": "parse",
        "page": title,
        "prop": "text|langlinks",
        "redirects": 1,  # follow redirects, but record that it happened
        "format": "json",
    })
    if data is None:
        return None
    if "error" in data:
        console.print(f"[yellow]Bulbapedia could not parse '{title}': {data['error']['info']}[/yellow]")
        return None

    page = data["parse"]
    soup = BeautifulSoup(page["text"]["*"], "html.parser")
    article_text = soup.get_text(" ", strip=True)

    internal_links = []
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if href.startswith("/wiki/") and "#" not in href:
            internal_links.append(href)

    langlinks = page.get("langlinks", [])

    return {
        "bulbapedia_title": page["title"],
        "bulbapedia_redirected": len(page.get("redirects", [])) > 0,
        "word_count": len(article_text.split()),
        "character_count": len(article_text),
        "internal_link_count": len(internal_links),
        "unique_internal_link_count": len(set(internal_links)),
        "bulbapedia_language_links": sorted(link["lang"] for link in langlinks),
    }


# ---------------------------------------------------------------------------
# Part 2: Query the second API (PokéAPI)
# ---------------------------------------------------------------------------
def get_pokeapi_species(name):
    species = get_json(f"{POKEAPI_URL}/pokemon-species/{name}")
    if species is None:
        return None

    # The species record links to its default "pokemon" record, which has types.
    default_url = None
    for variety in species["varieties"]:
        if variety["is_default"]:
            default_url = variety["pokemon"]["url"]

    types = []
    if default_url:
        time.sleep(PAUSE_SECONDS)
        pokemon = get_json(default_url)
        if pokemon is not None:
            types = [slot["type"]["name"] for slot in pokemon["types"]]

    # Official names in each language PokéAPI records
    official_names = {entry["language"]["name"]: entry["name"] for entry in species["names"]}

    return {
        "pokeapi_id": species["id"],
        "pokeapi_name": species["name"],
        "english_name": official_names.get("en", species["name"]),
        "generation": species["generation"]["name"],
        "types": types,
        "is_legendary": species["is_legendary"],
        "is_mythical": species["is_mythical"],
        "pokeapi_name_languages": sorted(official_names),
        "official_names": official_names,
    }


# ---------------------------------------------------------------------------
# Part 3: Connect the two
# ---------------------------------------------------------------------------
def connect(pokemon_name):
    """PokéAPI gives the official English name; Bulbapedia titles species
    articles as '<English name> (Pokémon)'. Build the title and look it up."""
    species = get_pokeapi_species(pokemon_name)
    if species is None:
        console.print(f"[yellow]Skipping '{pokemon_name}': not found on PokéAPI.[/yellow]")
        return None

    time.sleep(PAUSE_SECONDS)
    title = f"{species['english_name']} (Pokémon)"
    wiki = analyze_bulbapedia_page(title)

    row = {**species, "bulbapedia_title_tried": title}
    if wiki is None:
        row["match_status"] = "no Bulbapedia match"
    else:
        row.update(wiki)
        row["match_status"] = "redirected" if wiki["bulbapedia_redirected"] else "direct match"
    return row


def main():
    # 1. MediaWiki: print a category's members
    console.rule("Bulbapedia: Category:Generation I Pokémon (first 20)")
    members = get_category_members("Category:Generation I Pokémon")
    for member in members:
        console.print(member["title"])
    if not members:
        console.print("[yellow]No category members returned.[/yellow]")

    # 2. PokéAPI: print one full response so you can see its shape
    time.sleep(PAUSE_SECONDS)
    console.rule("PokéAPI: /pokemon-species/pikachu (raw response)")
    raw = get_json(f"{POKEAPI_URL}/pokemon-species/pikachu")
    if raw is not None:
        console.print(raw)

    # 3. Connect them
    console.rule("Connecting PokéAPI → Bulbapedia")
    rows = []
    for name in POKEMON:
        time.sleep(PAUSE_SECONDS)
        row = connect(name)
        if row is not None:
            rows.append(row)

    table = Table(title="PokéAPI vs. Bulbapedia")
    for column in ["English name", "Gen", "Match", "Words", "Unique links",
                   "PokéAPI langs", "Bulbapedia langs"]:
        table.add_column(column)
    for row in rows:
        table.add_row(
            row["english_name"],
            row["generation"].replace("generation-", ""),
            row["match_status"],
            str(row.get("word_count", "—")),
            str(row.get("unique_internal_link_count", "—")),
            str(len(row["pokeapi_name_languages"])),
            str(len(row.get("bulbapedia_language_links", []))),
        )
    console.print(table)

    # 4. Save only the item data (not raw responses)
    with open("pokeapi_bulbapedia_data.json", "w", encoding="utf-8") as file:
        json.dump(rows, file, ensure_ascii=False, indent=2)

    csv_columns = ["pokeapi_id", "english_name", "generation", "types", "is_legendary",
                   "is_mythical", "match_status", "bulbapedia_title_tried", "bulbapedia_title",
                   "word_count", "character_count", "internal_link_count",
                   "unique_internal_link_count", "pokeapi_name_languages",
                   "bulbapedia_language_links"]
    with open("pokeapi_bulbapedia_data.csv", "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=csv_columns, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            flat = dict(row)
            for key in ["types", "pokeapi_name_languages", "bulbapedia_language_links"]:
                flat[key] = "|".join(row.get(key, []))
            writer.writerow(flat)

    console.print(f"[green]Saved {len(rows)} rows to pokeapi_bulbapedia_data.json and .csv[/green]")


if __name__ == "__main__":
    main()
