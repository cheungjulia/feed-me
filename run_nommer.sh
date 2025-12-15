#!/bin/bash
# Wrapper script for running nommer via launchd
# This script is called by the launchd agent

# Change to the project directory (where this script lives)
cd "$(dirname "$0")"

# Run nommer using uv
# Note: Use absolute path since launchd doesn't load shell profile
# Find your uv path with: which uv
/opt/homebrew/bin/uv run nommer

# Exit with the same status as uv
exit $?

