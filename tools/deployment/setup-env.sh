#!/bin/bash
# Import all environment variables from .env to Vercel

while IFS='=' read -r key value; do
  # Skip comments and empty lines
  if [[ ! "$key" =~ ^#.*$ ]] && [[ -n "$key" ]]; then
    # Remove any quotes from value
    value=$(echo "$value" | sed 's/^"\(.*\)"$/\1/' | sed "s/^'\(.*\)'$/\1/")
    echo "Adding $key to Vercel..."
    echo "$value" | vercel env add "$key" production --yes 2>/dev/null || true
  fi
done < .env

echo "Environment variables configured!"
