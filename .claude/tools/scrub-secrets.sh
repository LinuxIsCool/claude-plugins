#!/bin/bash
# Scrub common secret patterns from Claude Code logs
# Usage: ./scrub-secrets.sh [directory]
# Default: scrubs all .claude/logging directories in the repo

set -euo pipefail

REPO_ROOT="${1:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"

scrub_file() {
  local file="$1"
  sed -i \
    -e 's/ghp_[a-zA-Z0-9]\{36\}/[REDACTED_GITHUB_PAT]/g' \
    -e 's/github_pat_[a-zA-Z0-9_]\{82,\}/[REDACTED_GITHUB_PAT]/g' \
    -e 's/sk-ant-api03-[a-zA-Z0-9_-]\{90,\}/[REDACTED_ANTHROPIC_KEY]/g' \
    -e 's/sk-ant-[a-zA-Z0-9_-]\{20,\}/[REDACTED_ANTHROPIC_KEY]/g' \
    -e 's/npm_[a-zA-Z0-9]\{36\}/[REDACTED_NPM_TOKEN]/g' \
    -e 's/sk-[a-zA-Z0-9]\{48\}/[REDACTED_OPENAI_KEY]/g' \
    -e 's/xoxb-[a-zA-Z0-9-]\{50,\}/[REDACTED_SLACK_TOKEN]/g' \
    -e 's/xoxp-[a-zA-Z0-9-]\{50,\}/[REDACTED_SLACK_TOKEN]/g' \
    -e 's/AKIA[A-Z0-9]\{16\}/[REDACTED_AWS_KEY]/g' \
    -e 's/[0-9]\{12\}-[a-z0-9]\{32\}\.apps\.googleusercontent\.com/[REDACTED_GOOGLE_CLIENT_ID]/g' \
    -e 's/GOCSPX-[a-zA-Z0-9_-]\{28\}/[REDACTED_GOOGLE_CLIENT_SECRET]/g' \
    -e 's/1\/\/[a-zA-Z0-9_-]\{40,\}/[REDACTED_GOOGLE_REFRESH_TOKEN]/g' \
    "$file"
}

export -f scrub_file

echo "Scrubbing secrets from logging directories in: $REPO_ROOT"

find "$REPO_ROOT" -type d -name "logging" -path "*/.claude/*" | while read -r dir; do
  find "$dir" \( -name "*.jsonl" -o -name "*.json" \) -type f | while read -r file; do
    scrub_file "$file"
  done
done

echo "Done. Verify with: git diff --stat"
