"""Main orchestrator for the feed listener."""

import yaml
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

from .models import AppConfig
from .feed_fetcher import fetch_all_feeds
from .post_store import filter_new_posts
from .llm_filter import filter_relevant_posts
from .notifier import write_to_obsidian_file
from .logger import logger
from datetime import date, timedelta


def load_config(config_path: Path | None = None) -> AppConfig:
    """Load configuration from YAML file."""
    if config_path is None:
        config_path = Path(__file__).parent.parent / "config.yaml"
    
    with open(config_path, "r") as f:
        data = yaml.safe_load(f)
    
    return AppConfig(**data)


def run(config_path: Path | None = None) -> None:
    """Run the feed listener pipeline.
    
    1. Load config
    2. Fetch all feeds
    3. Filter to new posts only
    4. Filter by relevance using LLM
    5. Write to Obsidian file
    """
    config = load_config(config_path)
    
    if not config.blogs:
        logger.warning("No blogs configured. Add blogs to config.yaml")
        return
    
    logger.info(f"NEW RUN: Fetching posts from {len(config.blogs)} blog(s) on {(date.today() - timedelta(days=1)).isoformat()}")
    all_posts = fetch_all_feeds(config.blogs)
    new_posts = filter_new_posts(all_posts)
    logger.info(f"Found {len(new_posts)} new posts")
    logger.info(f"New posts: {[post.title for post in new_posts]}")
    
    if not new_posts:
        logger.info("No new posts to process")
        return
    
    relevant_posts = filter_relevant_posts(new_posts, config.keywords)
    logger.info(f"Found {len(relevant_posts)} relevant posts against keywords: {config.keywords}")
    
    if not relevant_posts:
        logger.info("No relevant posts found")
        return
    
    logger.info(f"Writing {len(relevant_posts)} post(s) to Obsidian...")
    write_to_obsidian_file(relevant_posts, config.obsidian)
    logger.info("Done! \n\n")


if __name__ == "__main__":
    run()
