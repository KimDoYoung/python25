
from datetime import datetime
from mcp.server.fastmcp import FastMCP
import os

NOTE_FILE = os.path.join(os.path.dirname(__file__), "notes.txt")

mcp = FastMCP("AI stick note")

def ensure_file():
    """Ensure the note file exists."""
    # Check if the note file exists, if not, create it
    if not os.path.exists(NOTE_FILE):
        with open(NOTE_FILE, "w", encoding="utf-8") as f:
            f.write("")

@mcp.tool("Add a note")
def add_note(note: str)->str:
    """
        Add a note to the note file.
        Args:
            note (str): The note to add.
        Returns:
            str: Success message.
    """
    ensure_file()
    with open(NOTE_FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {note}\n")
    return "Note added successfully."

@mcp.tool("read notes")
def read_notes()->str:
    """
        Read all notes from the note file.
        Returns:
            str: All notes in the note file.
    """
    ensure_file()
    with open(NOTE_FILE, "r", encoding="utf-8") as f:
        notes = f.readlines()
    if not notes:
        return "No notes found."
    return "".join(notes)

@mcp.resource("notes://latest")
def get_latest_note()->str:
    """
        Get the latest note from the note file.
        Returns:
            str: The latest note in the note file.
    """
    ensure_file()
    with open(NOTE_FILE, "r", encoding="utf-8") as f:
        notes = f.readlines()
    if not notes:
        return "No notes found."
    return notes[-1].strip()

@mcp.prompt()
def note_summary_prompt()->str:
    """
        Prompt for a note summary.
        Returns:
            str: The note summary.
    """
    ensure_file()
    with open(NOTE_FILE, "r", encoding="utf-8") as f:
        notes = f.readlines()
    if not notes:
        return "No notes found."
    return "Please summarize the notes below:\n" + "".join(notes)
