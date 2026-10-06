import csv
from pathlib import Path

from rich.console import Console
from rich.table import Table

console = Console()

# Fields to collect for each entry (change these to fit your own topic)
FIELDS = ["Released", "Title", "Box Office"]

# Where the data will be saved
OUTPUT_FILE = Path("movies.csv")


def show_example_data():
    """Show some pre-created example data in a Rich table."""
    console.print("Here is some initial data:", style="bold cyan")

    table = Table(title="Star Wars Movies")
    table.add_column("Released", style="cyan", no_wrap=True)
    table.add_column("Title", style="magenta")
    table.add_column("Box Office", justify="right")
    table.add_row("Dec 20, 2019", "Star Wars: The Rise of Skywalker", "$952,110,690")
    table.add_row("May 25, 2018", "Solo: A Star Wars Story", "$393,151,347")
    table.add_row("Dec 15, 2017", "Star Wars Ep. VIII: The Last Jedi", "$1,332,539,889")
    table.add_row("Dec 16, 2016", "Rogue One: A Star Wars Story", "$1,056,057,273")

    console.print(table)


def get_entry():
    """Ask the user for each field and return the answers as a dictionary."""
    entry = {}
    for field in FIELDS:
        value = console.input(f"Enter the [bold]{field}[/bold]: ").strip()
        while value == "":
            console.print("This field can't be empty.", style="red")
            value = console.input(f"Enter the [bold]{field}[/bold]: ").strip()
        entry[field] = value
    return entry


def show_entry(entry):
    """Print a single entry back to the user in a small table."""
    table = Table(title="Your Entry")
    for field in FIELDS:
        table.add_column(field)
    table.add_row(*[entry[field] for field in FIELDS])
    console.print(table)


def ask_yes_no(question):
    """Keep asking until the user answers y or n. Returns True for yes."""
    while True:
        answer = console.input(f"{question} (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        console.print("Please type y or n.", style="red")


def get_confirmed_entry():
    """Collect an entry and repeat until the user confirms it is correct."""
    while True:
        entry = get_entry()
        show_entry(entry)
        if ask_yes_no("Is this correct?"):
            return entry
        console.print("Okay, let's try that entry again.\n", style="yellow")


def save_entry(entry):
    """Append one confirmed entry to the CSV file, adding a header if the file is new."""
    file_is_new = not OUTPUT_FILE.exists()
    with open(OUTPUT_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if file_is_new:
            writer.writeheader()
        writer.writerow(entry)


def main():
    show_example_data()
    console.print("\n[bold cyan]Now I want you to enter your preferred movies:[/bold cyan]")

    saved_count = 0
    while True:
        entry = get_confirmed_entry()
        save_entry(entry)
        saved_count += 1
        console.print("Saved!\n", style="green")

        if not ask_yes_no("Do you want to add another movie?"):
            break

    console.print(
        f"\n[bold green]{saved_count} entr{'y' if saved_count == 1 else 'ies'} saved to:[/bold green] "
        f"{OUTPUT_FILE.resolve()}"
    )


if __name__ == "__main__":
    main()