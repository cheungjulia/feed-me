"""RSS feed fetcher module."""

import feedparser
from datetime import date
from dateutil import parser as date_parser

from .models import Post, BlogConfig


def _is_today(published: str | None) -> bool:
    """Check if a published date string is from today.
    
    Uses dateutil.parser which flexibly handles many date formats
    including RFC 2822, ISO 8601, and others.
    """
    if not published:
        return False
    
    try:
        pub_date = date_parser.parse(published).date()
        return pub_date == date.today()
    except (ValueError, TypeError):
        return False


def fetch_feed(rss_url: str, blog_name: str | None = None) -> list[Post]:
    """Fetch posts from a single RSS feed."""
    feed = feedparser.parse(rss_url)
    posts: list[Post] = []
    
    for entry in feed.entries:
        post = Post(
            title=entry.get("title", ""),
            link=entry.get("link", ""),
            description=entry.get("summary", entry.get("description", "")),
            published=entry.get("published"),
            blog_name=blog_name
        )
        posts.append(post)
    
    return posts


def fetch_all_feeds(blogs: list[BlogConfig], today_only: bool = True) -> list[Post]:
    """Fetch posts from multiple blog feeds.
    
    Args:
        blogs: List of blog configurations
        today_only: If True, only return posts published today
    
    Returns:
        Combined list of posts from all feeds
    """
    all_posts: list[Post] = []
    
    for blog in blogs:
        posts = fetch_feed(blog.rss_url, blog_name=blog.name)
        all_posts.extend(posts)
    
    if today_only:
        all_posts = [p for p in all_posts if _is_today(p.published)]
    
    return all_posts
