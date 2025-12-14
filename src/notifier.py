"""Obsidian daily note integration."""

from datetime import date
from pathlib import Path

from .models import Post, ObsidianConfig


def _get_daily_note_path(config: ObsidianConfig) -> Path:
    """Get path to today's daily note."""
    vault = Path(config.vault_path).expanduser()
    daily_folder = vault / config.daily_notes_folder
    daily_folder.mkdir(parents=True, exist_ok=True)
    
    today = date.today().isoformat()  # YYYY-MM-DD
    return daily_folder / f"{today}.md"


def _format_post(post: Post) -> str:
    """Format a post for the daily note."""
    return f"- {post.title}: {post.link}\n"


def write_to_daily_note(posts: list[Post], config: ObsidianConfig) -> None:
    """Write relevant posts to today's Obsidian daily note.
    
    Args:
        posts: List of relevant posts to write
        config: Obsidian configuration
    """
    if not posts:
        return
    
    note_path = _get_daily_note_path(config)
    
    # Build content
    content_parts = ["\n## Updates from RSS Feeds\n"]
    for post in posts:
        content_parts.append(_format_post(post))
    
    content = "\n".join(content_parts)
    
    # Append to daily note (creates if doesn't exist)
    with open(note_path, "a") as f:
        f.write(content)
