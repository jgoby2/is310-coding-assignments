"""
Minecraft Wiki mob scraper for IS 310.

Research question: Do hostile mobs receive more documentation on the
Minecraft Wiki than passive mobs?

Level 1: two category pages (Hostile mobs, Passive mobs) -> list of mob pages
Level 2: each mob's article page -> word, character, and internal-link counts
"""

import csv
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table


BASE_URL = "https://minecraft.wiki"
HOSTILE_CATEGORY_URL = f"{BASE_URL}/w/Category:Hostile_mobs"
PASSIVE_CATEGORY_URL = f"{BASE_URL}/w/Category:Passive_mobs"
HEADERS = {
    "User-Agent": "is310-course-scraper/1.0 (student project; jgoby2@illinois.edu)"
}
REQUEST_DELAY = 1.0  # seconds to wait after every request

# Save the CSV next to this script, no matter which folder you run it from.
RESULTS_OUTPUT = Path(__file__).parent / "minecraft_mobs.csv"

console = Console()


def fetch_soup(url):
    """Download a page and return it as a BeautifulSoup object, or None."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
    except requests.RequestException as error:
        console.print(f"[red]Request failed for {url}: {error}[/red]")
        time.sleep(REQUEST_DELAY)
        return None

    time.sleep(REQUEST_DELAY)

    if response.status_code != 200:
        console.print(f"[red]Could not download {url}: HTTP {response.status_code}[/red]")
        return None

    return BeautifulSoup(response.text, "html.parser")


def scrape_mobs(category_page, mob_type, source_url):
    """Collect mob article links from a category page."""
    mobs = []
    if category_page is None:
        return mobs

    pages_section = category_page.find(id="mw-pages")
    if pages_section is None:
        console.print(f"[yellow]No 'mw-pages' section found on {source_url}[/yellow]")
        return mobs

    for item in pages_section.find_all("li"):
        link = item.find("a", href=True)
        if link is None:
            continue

        href = link["href"]
        # A colon in the page name marks a special namespace, such as
        # editors' sandbox drafts (User:, which robots.txt disallows) or
        # spin-off game pages (Dungeons II:). Normal mob names never have one.
        # Also skip anything that is not a normal article link.
        if ":" in href[3:] or not href.startswith("/w/") or "?" in href:
            continue

        mobs.append({
            "mob": link.get_text(" ", strip=True),
            "mob_type": mob_type,
            "source_url": source_url,
            "mob_url": f"{BASE_URL}{href}",
        })

    return mobs


def get_internal_links(content):
    """Return every link in the article that points to another wiki page."""
    if content is None:
        return []

    links = []
    for link in content.find_all("a", href=True):
        href = link["href"]
        # Minecraft Wiki uses /w/ (Tolkien Gateway used /wiki/).
        # Exclude section links (#) and links with query parameters (?).
        if href.startswith("/w/") and "#" not in href and "?" not in href:
            links.append(href)

    return links


def measure_page(url):
    """Download one mob page and calculate text and link measurements."""
    measurements = {
        "word_count": 0,
        "character_count": 0,
        "internal_link_count": 0,
        "unique_internal_link_count": 0,
    }

    soup = fetch_soup(url)
    if soup is None:
        return measurements

    content = soup.select_one("#mw-content-text .mw-parser-output")
    if content is None:
        return measurements

    article_text = content.get_text(" ", strip=True)
    internal_links = get_internal_links(content)
    unique_internal_links = []
    for href in internal_links:
        if href not in unique_internal_links:
            unique_internal_links.append(href)

    measurements["word_count"] = len(article_text.split())
    measurements["character_count"] = len(article_text)
    measurements["internal_link_count"] = len(internal_links)
    measurements["unique_internal_link_count"] = len(unique_internal_links)
    return measurements


def save_csv(records, output_path):
    if not records:
        console.print(f"[yellow]No records to save to {output_path}[/yellow]")
        return

    with open(output_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)


def print_results_table(records):
    table = Table(title="Hostile and Passive Mob Pages")
    table.add_column("Mob", style="cyan")
    table.add_column("Type", style="green")
    table.add_column("In Both", style="magenta")
    table.add_column("Words", justify="right")
    table.add_column("Characters", justify="right")
    table.add_column("All Links", justify="right")
    table.add_column("Unique Links", justify="right")

    for record in sorted(records, key=lambda r: r["word_count"], reverse=True):
        table.add_row(
            record["mob"],
            record["mob_type"],
            str(record["in_both_categories"]),
            str(record["word_count"]),
            str(record["character_count"]),
            str(record["internal_link_count"]),
            str(record["unique_internal_link_count"]),
        )

    console.print(table)


def print_averages(records):
    """Print the average of each measurement for hostile vs. passive mobs."""
    table = Table(title="Averages by Mob Type")
    table.add_column("Type", style="green")
    table.add_column("Pages", justify="right")
    table.add_column("Avg Words", justify="right")
    table.add_column("Avg Characters", justify="right")
    table.add_column("Avg All Links", justify="right")
    table.add_column("Avg Unique Links", justify="right")

    for mob_type in ["hostile", "passive"]:
        group = [r for r in records if r["mob_type"] == mob_type]
        if not group:
            continue
        count = len(group)
        table.add_row(
            mob_type,
            str(count),
            f"{sum(r['word_count'] for r in group) / count:.0f}",
            f"{sum(r['character_count'] for r in group) / count:.0f}",
            f"{sum(r['internal_link_count'] for r in group) / count:.0f}",
            f"{sum(r['unique_internal_link_count'] for r in group) / count:.0f}",
        )

    console.print(table)


def main():
    console.print("[cyan]Finding hostile mobs...[/cyan]")
    hostile_page = fetch_soup(HOSTILE_CATEGORY_URL)
    hostile_mobs = scrape_mobs(hostile_page, "hostile", HOSTILE_CATEGORY_URL)

    console.print("[cyan]Finding passive mobs...[/cyan]")
    passive_page = fetch_soup(PASSIVE_CATEGORY_URL)
    passive_mobs = scrape_mobs(passive_page, "passive", PASSIVE_CATEGORY_URL)

    # Some mobs (e.g. Skeleton Horse) are in both categories. We keep a row
    # for each category but flag them so they can be filtered out later.
    hostile_urls = {mob["mob_url"] for mob in hostile_mobs}
    passive_urls = {mob["mob_url"] for mob in passive_mobs}
    both_urls = hostile_urls & passive_urls

    all_mobs = hostile_mobs + passive_mobs
    console.print(f"[green]Found {len(all_mobs)} mob entries "
                  f"({len(both_urls)} mobs appear in both categories).[/green]")

    # Download each page only once, even if a mob appears in both categories.
    measured = {}
    results = []
    for number, mob in enumerate(all_mobs, start=1):
        console.print(f"Processing {number}/{len(all_mobs)}: {mob['mob']}")
        if mob["mob_url"] not in measured:
            measured[mob["mob_url"]] = measure_page(mob["mob_url"])

        record = mob.copy()
        record["in_both_categories"] = mob["mob_url"] in both_urls
        record.update(measured[mob["mob_url"]])
        results.append(record)

    print_results_table(results)
    print_averages(results)
    save_csv(results, RESULTS_OUTPUT)
    console.print(f"[green]Saved {len(results)} rows to {RESULTS_OUTPUT}[/green]")


if __name__ == "__main__":
    main()
