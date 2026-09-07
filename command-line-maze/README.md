# The Stadium Archive: A Cultural Data Maze

**Creator:** Jack Goby

## Theme

This maze treats sports as cultural data. A stadium stores rituals, records,
shared memories, and ideas about who gets remembered.

## How to play

1. Open a terminal in this folder.
2. On macOS/Linux/WSL, use `ls -la` to show dotfiles. On Windows PowerShell,
   use `Get-ChildItem -Recurse -Force` or run `./hide-dotfiles.ps1` first.
3. Enter `arena` and inspect files with `ls`, `Get-ChildItem`, `cat`, or
   `Get-Content`.
4. Follow the clues. Wrong paths are dead ends.
5. You have solved the maze when you read `final-whistle.txt`.

The hidden clue is part of the route and is intentionally easy to miss.

## Helpful commands

```text
cd arena
ls -la                         # macOS/Linux/WSL
Get-ChildItem -Force           # Windows PowerShell
cat path/to/file.txt           # macOS/Linux/WSL
Get-Content path\to\file.txt  # Windows PowerShell
```

The zip file for submission is `command-line-maze.zip`. This README stays
outside the zip so solvers can read the instructions before unzipping it.