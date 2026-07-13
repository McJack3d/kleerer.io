#!/usr/bin/env bash
# kleerer. — offline backup of the private data archive to external storage.
#
# First run (creates a full mirror — contains ALL history):
#   ./backup.sh /Volumes/YOUR_DRIVE/kleerer-backup
#
# Every following run (fast incremental update):
#   ./backup.sh /Volumes/YOUR_DRIVE/kleerer-backup
#
# A git *mirror* contains every commit, every snapshot, every day ever recorded.
# Even if GitHub disappeared or the account were compromised, this copy restores
# everything:  git clone /path/kleerer-data.git  →  full archive back.
# Suggested cadence: weekly, or whenever you plug the drive in.
set -euo pipefail

DEST="${1:?usage: ./backup.sh /path/to/external/drive/folder}"
REPO_DATA="https://github.com/McJack3d/kleerer-data.git"
REPO_SITE="https://github.com/McJack3d/kleerer.io.git"

mkdir -p "$DEST"
for REPO in "$REPO_DATA" "$REPO_SITE"; do
  NAME="$(basename "$REPO")"
  TARGET="$DEST/$NAME"
  if [ -d "$TARGET" ]; then
    echo "→ updating mirror $NAME"
    git -C "$TARGET" remote update --prune
  else
    echo "→ creating mirror $NAME (first run)"
    git clone --mirror "$REPO" "$TARGET"
  fi
done

echo
echo "Backup complete → $DEST"
echo "Verify anytime with:  git -C \"$DEST/kleerer-data.git\" log --oneline -3"
