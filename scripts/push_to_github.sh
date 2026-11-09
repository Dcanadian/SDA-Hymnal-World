#!/bin/bash
set -e

REPO_DIR="/home/antigravity/SDA-Hymnal"
cd "$REPO_DIR"

git config http.postBuffer 524288000
echo "Pushing commit to origin main..."
git push --progress origin main

echo "Successfully pushed to https://github.com/Dcanadian/SDA-Hymnal-World !"
