# 🍜 ᶠᵉᵉᵈ ᵐᵉ /ᐠ-ⱉ-ᐟ\ﾉ

A personal RSS feed reader that uses AI to filter posts based on your interests and saves the good stuff to your Obsidian vault.

**What it does:**
1. Fetches new posts from RSS feeds (blogs, newsletters, YouTube channels)
2. Uses GPT-4o-mini to filter posts that match your interests
3. Writes relevant posts to a file in your Obsidian vault

---

## 📋 Prerequisites

Before you start, you'll need:

1. **An OpenAI API key** - Get one at [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
   - You'll need to add a payment method and add some credits (~$5 is plenty to start)
   - The app uses GPT-4o-mini which costs about $0.15 per million tokens (very cheap)

2. **Obsidian** (optional but recommended) - Download at [obsidian.md](https://obsidian.md)
   - Know where your vault folder is located on your computer

---

## 🚀 Quick Start (Mac/Linux)

### Step 1: Download the code

Open **Terminal** (on Mac: press `Cmd + Space`, type "Terminal", press Enter) and run:

```bash
git clone https://github.com/YOUR_USERNAME/nommer.git
cd nommer
```

### Step 2: Run the setup script

```bash
chmod +x setup.sh
./setup.sh
```

This will:
- Install `uv` (a Python package manager) if you don't have it
- Install all required dependencies
- Create your `.env` file for the API key
- Create your `config.yaml` from the template

### Step 3: Edit your configuration

Open `config.yaml` in any text editor (TextEdit, VS Code, etc.) and customize:

```yaml
# Where to save filtered posts
obsidian:
  vault_path: "/Users/YourName/Documents/MyVault"  # Your Obsidian vault path
  output_file: "filtered-posts.md"                  # File name for saved posts

# Topics you're interested in (AI will filter based on these)
keywords:
  - AI
  - economics
  - technology
  - science

# RSS feeds to follow
blogs:
  - name: "Marginal Revolution"
    rss_url: "https://marginalrevolution.com/feed"
  - name: "Hacker News"
    rss_url: "https://news.ycombinator.com/rss"
```

**Finding your Obsidian vault path:**
- On Mac: Open Finder, navigate to your vault folder, right-click → "Get Info" → copy the path shown under "Where"
- Or: In Obsidian, go to Settings → Files & Links → look at "Vault location"

**Finding RSS feeds:**
- Most blogs have an RSS link in the footer or sidebar
- e.g. for Substack: add `/feed` to the newsletter URL (e.g., `https://example.substack.com/feed`)

### Step 4: Run nommer

```bash
uv run nommer
```

That's it! Check your Obsidian vault for the filtered posts.

---

## 🔄 Running Automatically (Optional)

Want nommer to run automatically every day? Here's how:

### On Mac (using launchd)

1. Create a wrapper script. Edit `run_nommer.sh`:

```bash
#!/bin/bash
cd /path/to/your/nommer
/path/to/uv run nommer
```

Find your uv path by running `which uv` in Terminal.

2. Create a launch agent file at `~/Library/LaunchAgents/com.nommer.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.nommer</string>
    <key>ProgramArguments</key>
    <array>
        <string>/path/to/your/nommer/run_nommer.sh</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/path/to/your/nommer/logs/nommer.log</string>
    <key>StandardErrorPath</key>
    <string>/path/to/your/nommer/logs/nommer.error.log</string>
</dict>
</plist>
```

3. Load the agent:

```bash
launchctl load ~/Library/LaunchAgents/com.nommer.plist
```

### On Linux (using cron)

```bash
crontab -e
```

Add this line to run at 9 AM daily:

```
0 9 * * * cd /path/to/nommer && /path/to/uv run nommer
```

---

## 🛠️ Manual Setup (Alternative)

If you prefer to set things up manually:

1. **Install uv** (if you don't have it):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Set up your API key:**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

4. **Configure the app:**
   ```bash
   cp config.example.yaml config.yaml
   # Edit config.yaml with your settings
   ```

5. **Run:**
   ```bash
   uv run nommer
   ```

---

## 📁 Project Structure

```
nommer/
├── config.yaml          # Your personal configuration (not in git)
├── config.example.yaml  # Template configuration
├── .env                 # Your API key (not in git)
├── .env.example         # Template for API key
├── data/
│   └── posts.db         # Database of seen posts (prevents duplicates)
├── logs/                # Log files
└── src/                 # Source code
```

---

## ❓ Troubleshooting

**"command not found: uv"**
- Run the install script again, or add uv to your PATH:
  ```bash
  source $HOME/.local/bin/env
  ```

**"No module named 'openai'"**
- Make sure you ran `uv sync` to install dependencies

**"Invalid API key"**
- Check your `.env` file has the correct key (starts with `sk-`)
- Make sure there are no extra spaces or quotes around the key

**Posts not appearing in Obsidian**
- Check that `vault_path` in config.yaml points to the correct folder
- Make sure the folder exists and you have write permissions

**No posts being filtered**
- Check the `logs/nommer.log` file for details
- Try broadening your keywords
