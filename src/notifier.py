"""Obsidian file integration."""

from datetime import date, timedelta
from pathlib import Path

from .models import Post, ObsidianConfig


def _get_output_path(config: ObsidianConfig) -> Path:
    """Get path to the output file."""
    vault = Path(config.vault_path).expanduser()
    return vault / config.output_file


def _format_post(post: Post) -> str:
    """Format a post for the note."""
    return f"[{post.title}]({post.link}) ({post.blog_name})\n"


def write_to_obsidian_file(posts: list[Post], config: ObsidianConfig) -> None:
    """Write relevant posts to the Obsidian file.
    
    Args:
        posts: List of relevant posts to write
        config: Obsidian configuration
    """
    if not posts:
        return
    
    note_path = _get_output_path(config)
    
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    content_parts = [f"\n## {yesterday}\n"]
    for post in posts:
        content_parts.append(_format_post(post))
    
    content = "".join(content_parts)
    
    with open(note_path, "a") as f:
        f.write(content)
