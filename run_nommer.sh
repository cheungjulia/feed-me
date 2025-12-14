#!/bin/bash
# Wrapper script for running nommer via launchd
# This script is called by the launchd agent

# Change to the project directory
cd /Users/Julia_Cheung/Git/nommer

# Run nommer using uv
/opt/homebrew/bin/uv run nommer

# Exit with the same status as uv
exit $?

