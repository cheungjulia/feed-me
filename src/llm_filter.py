"""LLM-based relevance filtering using OpenAI structured outputs."""

import os
from openai import OpenAI

from .models import Post, Relevance, RelevanceResponse


def _get_client() -> OpenAI:
    """Get OpenAI client."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    return OpenAI(api_key=api_key)


def check_relevance(post: Post, keywords: list[str]) -> bool:
    """Check if a post is relevant to the given keywords using LLM.
    
    Args:
        post: The post to check
        keywords: List of interest keywords
    
    Returns:
        True if relevant, False otherwise
    """
    client = _get_client()
    
    keywords_str = ", ".join(keywords)
    description = post.description[:500] if post.description else "No description"
    
    prompt = f"""Determine if this blog post is relevant to ANY of these topics: {keywords_str}

Post Title: {post.title}
Post Description: {description}

Respond with your relevance assessment."""

    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format=RelevanceResponse,
        temperature=0
    )
    
    result = response.choices[0].message.parsed
    return result.relevance == Relevance.YES


def filter_relevant_posts(posts: list[Post], keywords: list[str]) -> list[Post]:
    """Filter posts to only those relevant to keywords.
    
    Args:
        posts: List of posts to check
        keywords: List of interest keywords
    
    Returns:
        List of relevant posts
    """
    if not keywords:
        return posts
    
    relevant: list[Post] = []
    for post in posts:
        if check_relevance(post, keywords):
            relevant.append(post)
    
    return relevant
