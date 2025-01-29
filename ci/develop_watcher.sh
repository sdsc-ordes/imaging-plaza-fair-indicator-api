#!/bin/bash
# Usage: */5 * * * * /imaging-plaza/ci/develop_watcher.sh >> /imaging-plaza/ci/develop_watcher.log 2>&1

cd /imaging-plaza/imaging-plaza-fair-indicator-api || exit

# Fetch the latest changes from the remote
git fetch origin develop > /dev/null 2>&1

# Check if local is behind remote
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/develop)

if [ "$LOCAL" != "$REMOTE" ]; then
  echo "$(date '+%Y-%m-%d %H:%M:%S'). Changes detected. Pulling..."
  git pull origin develop
  
  # Stop and remove the old container
  docker stop fair-indicator-api || true
  docker rm fair-indicator-api || true
  
  # Rebuild and run the new container
  docker build -t fair-indicator-api .
  docker run -d --name fair-indicator-api -p 7510:15400 --env-file .env fair-indicator-api
else
  echo "$(date '+%Y-%m-%d %H:%M:%S'). No changes found."
fi
