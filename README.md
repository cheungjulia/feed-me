# nommer

RSS feed listener with LLM-based relevance filtering. Fetches posts from blogs, filters by your interests using GPT-4o-mini, and writes relevant posts to your Obsidian daily notes.

## Setup

```bash
uv sync
cp config.example.yaml config.yaml  # Edit with your settings
```

Set your OpenAI API key in `.env`:
```
OPENAI_API_KEY=your-key
```

## Usage

```bash
uv run nommer
```

## Config

```yaml
obsidian:
  vault_path: "~/path/to/vault"
  daily_notes_folder: "Daily Notes"

keywords:
  - AI
  - economics

blogs:
  - name: "Blog Name"
    rss_url: "https://example.com/feed"
```

