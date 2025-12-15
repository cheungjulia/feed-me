"""Post deduplication store using SQLite."""

import hashlib
import sqlite3
from pathlib import Path

from .models import Post

DATA_DIR = Path(__file__).parent.parent / "data"
DB_PATH = DATA_DIR / "posts.db"


def _get_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    """Get SQLite connection, creating table if needed."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS seen_posts (
            hash TEXT PRIMARY KEY,
            source TEXT,
            link TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    return conn


def _hash_url(url: str) -> str:
    """Generate hash for a URL."""
    return hashlib.sha256(url.encode()).hexdigest()[:16]


def _is_seen(conn: sqlite3.Connection, post_hash: str) -> bool:
    """Check if a post hash has been seen."""
    cursor = conn.execute("SELECT 1 FROM seen_posts WHERE hash = ?", (post_hash,))
    return cursor.fetchone() is not None


def _mark_seen(conn: sqlite3.Connection, post: Post) -> None:
    """Mark a post as seen with metadata."""
    post_hash = _hash_url(post.link)
    conn.execute(
        "INSERT OR IGNORE INTO seen_posts (hash, source, link) VALUES (?, ?, ?)",
        (post_hash, post.blog_name, post.link)
    )


def filter_new_posts(posts: list[Post]) -> list[Post]:
    """Filter out already-seen posts, returning only new ones.
    
    Also marks new posts as seen for future runs.
    """
    conn = _get_connection()
    new_posts: list[Post] = []
    
    try:
        for post in posts:
            post_hash = _hash_url(post.link)
            
            if not _is_seen(conn, post_hash):
                new_posts.append(post)
                _mark_seen(conn, post)
        
        conn.commit()
    finally:
        conn.close()
    
    return new_posts


def clear_seen_posts() -> None:
    """Clear all seen post hashes (useful for testing)."""
    if DB_PATH.exists():
        DB_PATH.unlink()
