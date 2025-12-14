"""Pydantic models for the feed listener."""

from enum import Enum
from pydantic import BaseModel


class Post(BaseModel):
    """Represents a blog post."""
    title: str
    link: str
    description: str
    published: str | None = None
    blog_name: str | None = None


class BlogConfig(BaseModel):
    """Configuration for a single blog."""
    name: str
    rss_url: str


class ObsidianConfig(BaseModel):
    """Obsidian vault configuration."""
    vault_path: str
    output_file: str = "cold brew.md"
    

class AppConfig(BaseModel):
    """Application configuration."""
    keywords: list[str]
    blogs: list[BlogConfig]
    obsidian: ObsidianConfig


class Relevance(str, Enum):
    """Enum for LLM relevance response."""
    YES = "yes"
    NO = "no"


class RelevanceResponse(BaseModel):
    """Structured response from LLM for relevance check."""
    relevance: Relevance

