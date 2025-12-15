#!/bin/bash
# Interactive setup script for nommer
# Run this after cloning the repository

set -e

echo "🍜 Welcome to nommer setup!"
echo "============================"
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv (Python package manager)..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    echo ""
    echo "✅ uv installed! You may need to restart your terminal or run:"
    echo "   source \$HOME/.local/bin/env"
    echo ""
    echo "After that, run this setup script again."
    exit 0
fi

echo "✅ uv is installed"
echo ""

# Install dependencies
echo "📦 Installing Python dependencies..."
uv sync
echo "✅ Dependencies installed"
echo ""

# Check for .env file
if [ ! -f .env ]; then
    echo "🔑 Setting up your OpenAI API key..."
    echo ""
    echo "You need an OpenAI API key to use nommer."
    echo "Get one at: https://platform.openai.com/api-keys"
    echo ""
    read -p "Enter your OpenAI API key: " api_key
    echo "OPENAI_API_KEY=$api_key" > .env
    echo "✅ API key saved to .env"
else
    echo "✅ .env file already exists"
fi
echo ""

# Check for config.yaml
if [ ! -f config.yaml ]; then
    echo "⚙️  Setting up your configuration..."
    cp config.example.yaml config.yaml
    echo "✅ Created config.yaml from template"
    echo ""
    echo "📝 IMPORTANT: Edit config.yaml to add:"
    echo "   1. Your Obsidian vault path"
    echo "   2. Your interests/keywords"  
    echo "   3. RSS feeds you want to follow"
    echo ""
    echo "   Open config.yaml in any text editor to customize it."
else
    echo "✅ config.yaml already exists"
fi
echo ""

echo "============================"
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Edit config.yaml with your settings"
echo "  2. Run: uv run nommer"
echo ""
echo "To run nommer automatically on a schedule, see the README."
echo ""

