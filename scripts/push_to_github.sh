#!/bin/bash
set -e

REPO_DIR="/home/antigravity/SDA-Hymnal"
cd "$REPO_DIR"

TOKEN=$(sed -n 's/.*"access_token":"\([^"]*\)".*/\1/p' /home/antigravity/.gemini/jetski/plugin_data/github/token.json 2>/dev/null || echo "$GH_TOKEN")

if [ -n "$TOKEN" ]; then
    echo "Pushing using authenticated GitHub token..."
    git push "https://x-access-token:${TOKEN}@github.com/Dcanadian/SDA-Hymnal-World.git" main
else
    echo "Pushing using default origin..."
    git push -u origin main
fi

echo "Successfully pushed to https://github.com/Dcanadian/SDA-Hymnal-World !"
