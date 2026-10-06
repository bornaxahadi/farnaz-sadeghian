#!/usr/bin/env bash
# Rebuilds the whole site (all 10 languages) from _src/ and writes it into the repo root.
# Needs: python3, node, esbuild (npm i -g esbuild). Run from anywhere: bash _src/build.sh
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
W="$(mktemp -d)"
cp "$REPO"/_src/*.part "$REPO"/_src/i18n.js "$REPO"/_src/build2.py "$REPO"/_src/seo_alts.py "$W"/
mkdir -p "$W/fonts" "$W/dist"
cp "$REPO"/fonts/*.woff2 "$W/fonts/" && cp "$REPO/_src/fonts.css" "$W/fonts/fonts.css"
cp -r "$REPO/img" "$W/img"
cp "$REPO/media-kit.pdf" "$W/dist/"
( cd "$W" && python3 build2.py )
# copy the generated site over the repo root (never deletes anything else in the repo)
cp -r "$W"/dist/. "$REPO"/
rm -rf "$W"
echo "Built. Review 'git diff', then commit _src/ together with the generated files."
