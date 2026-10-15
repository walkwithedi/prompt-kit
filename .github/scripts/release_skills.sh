#!/usr/bin/env bash
# Release each skill that changed: bash .github/scripts/release_skills.sh [skill ...]
# A skill is a folder under skills/. With no arguments every skill is checked.
# For each skill: take its latest tag "<skill>-vYYYY.MM.DD[.N]"; when skills/<skill>/ is unchanged
# since that tag, skip it. Otherwise create a release versioned with today's date (Asia/Shanghai)
# whose asset is <skill>-v<version>.zip (scripts/build_skill.py: <skill>/SKILL.md only), with the
# commits that touched the folder since the last release as its notes. These releases are not marked latest.
# Then, on a full run (no arguments), the whole kit: when skills/, README.md, README.zh-CN.md or
# LICENSE changed since the latest tag "prompt-kit-vYYYY.MM.DD[.N]", or there is none, release
# prompt-kit-v<version>.zip (git archive of those paths under prompt-kit/) together with every
# skill's upload zip as <skill>.zip, marked latest.
# Environment: DRY_RUN=1 builds and prints the plan without calling gh; FORCE=1 releases unchanged
# skills too; OUT_DIR sets the build folder.
set -euo pipefail
log(){ echo "[release] $*" >&2; }

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"
SHA="$(git rev-parse HEAD)"
TODAY="$(TZ=Asia/Shanghai date +%Y.%m.%d)"
OUT_DIR="${OUT_DIR:-$(mktemp -d)}"
DRY_RUN="${DRY_RUN:-0}"
FORCE="${FORCE:-0}"
REPO="${GITHUB_REPOSITORY:-}"
mkdir -p "$OUT_DIR"

FULL_RUN=1
if [ "$#" -gt 0 ]; then
  FULL_RUN=0
  SKILLS=("$@")
else
  SKILLS=()
  for d in skills/*/; do
    d="${d%/}"; SKILLS+=("${d#skills/}")
  done
fi
log "commit=$SHA date=$TODAY skills=${SKILLS[*]} DRY_RUN=$DRY_RUN FORCE=$FORCE out=$OUT_DIR"

# Next free version: YYYY.MM.DD for the first release of the day, then .2, .3 ...
next_version(){
  local name="$1" ver="$TODAY" n=1
  while git rev-parse -q --verify "refs/tags/$name-v$ver" >/dev/null; do
    n=$((n + 1)); ver="$TODAY.$n"
  done
  echo "$ver"
}

FAILED=0
for skill in "${SKILLS[@]}"; do
  if [ ! -f "skills/$skill/SKILL.md" ]; then
    echo "::error::$skill is not a skill folder (no skills/$skill/SKILL.md)" >&2; FAILED=1; continue
  fi
  LAST=$(git tag -l "$skill-v[0-9]*" --sort=-v:refname | head -n1)
  if [ -n "$LAST" ]; then
    if [ "$FORCE" != 1 ] && git diff --quiet "$LAST" "$SHA" -- "skills/$skill/"; then
      log "$skill: unchanged since $LAST, skipped"; continue
    fi
    RANGE="$LAST..$SHA"
  else
    RANGE="$SHA"
  fi
  VER=$(next_version "$skill")
  TAG="$skill-v$VER"
  ZIP=$(python3 scripts/build_skill.py "$OUT_DIR" "$skill" --version "$VER" --log-level WARNING)
  log "$skill: last=${LAST:-none} new=$TAG asset=$ZIP ($(unzip -Z1 "$ZIP" | tr '\n' ' '))"

  NOTES="$OUT_DIR/$TAG.notes.md"
  {
    echo "$TAG.zip holds $skill/SKILL.md from commit ${SHA:0:7}; upload it on the Skills page of claude.ai settings. See skills/$skill/README.md."
    echo
    echo "$TAG.zip 内含提交 ${SHA:0:7} 的 $skill/SKILL.md，可在 claude.ai 设置的 Skills 页面上传；用法见 skills/$skill/README.zh-CN.md。"
    echo
    if [ -n "$LAST" ]; then echo "Changes since $LAST:"; else echo "Changes:"; fi
    echo
    git log --no-merges --format='- %s (%h)' "$RANGE" -- "skills/$skill/" | head -n 50
  } > "$NOTES"

  if [ "$DRY_RUN" = 1 ]; then
    log "$skill: DRY_RUN, no release. Notes:"; cat "$NOTES" >&2; continue
  fi
  if ! gh release create "$TAG" "$ZIP" \
      --repo "$REPO" --target "$SHA" --title "$TAG" --notes-file "$NOTES" --latest=false; then
    echo "::error::$skill: creating release $TAG failed" >&2; FAILED=1; continue
  fi
  git tag "$TAG" "$SHA"   # recorded locally so a second release today in this run gets the next number
  log "$skill: released ${GITHUB_SERVER_URL:-https://github.com}/$REPO/releases/tag/$TAG"
done

# Whole kit: only on a full run, so a hand-picked list of skills never releases it
BUNDLE=prompt-kit
BUNDLE_PATHS=(skills README.md README.zh-CN.md LICENSE)
if [ "$FULL_RUN" != 1 ]; then
  log "$BUNDLE: skills given, skipped"
  exit "$FAILED"
fi
LAST=$(git tag -l "$BUNDLE-v[0-9]*" --sort=-v:refname | head -n1)
if [ -n "$LAST" ] && [ "$FORCE" != 1 ] && git diff --quiet "$LAST" "$SHA" -- "${BUNDLE_PATHS[@]}"; then
  log "$BUNDLE: unchanged since $LAST, skipped"
  exit "$FAILED"
fi
if [ -n "$LAST" ]; then RANGE="$LAST..$SHA"; else RANGE="$SHA"; fi
VER=$(next_version "$BUNDLE")
TAG="$BUNDLE-v$VER"
ZIP="$OUT_DIR/$TAG.zip"
git archive --format=zip --prefix="$BUNDLE/" -o "$ZIP" "$SHA" "${BUNDLE_PATHS[@]}"
log "$BUNDLE: last=${LAST:-none} new=$TAG asset=$ZIP ($(unzip -Z1 "$ZIP" | wc -l) entries)"
# Each skill's upload zip as well, so the latest release offers every single skill
ASSETS=("$ZIP")
SKILL_DIR="$OUT_DIR/$TAG-skills"
for skill in "${SKILLS[@]}"; do
  [ -f "skills/$skill/SKILL.md" ] || continue
  BUILT=$(python3 scripts/build_skill.py "$SKILL_DIR" "$skill" --version "$VER" --log-level WARNING)
  mv "$BUILT" "$SKILL_DIR/$skill.zip"
  ASSETS+=("$SKILL_DIR/$skill.zip")
done
log "$BUNDLE: assets ${ASSETS[*]##*/}"

NOTES="$OUT_DIR/$TAG.notes.md"
{
  echo "$TAG.zip holds every skill folder (SKILL.md, prompt.md, READMEs) with the root READMEs and LICENSE from commit ${SHA:0:7}, laid out as in the repository under $BUNDLE/. Each <skill>.zip holds <skill>/SKILL.md from the same commit; upload it on the Skills page of claude.ai settings."
  echo
  echo "$TAG.zip 内含提交 ${SHA:0:7} 的全部 skill 目录（SKILL.md、prompt.md、README）及根目录 README 与 LICENSE，按仓库结构放在 $BUNDLE/ 下。各 <skill>.zip 内含同一提交的 <skill>/SKILL.md，可在 claude.ai 设置的 Skills 页面上传。"
  echo
  if [ -n "$LAST" ]; then echo "Changes since $LAST:"; else echo "Changes:"; fi
  echo
  git log --no-merges --format='- %s (%h)' "$RANGE" -- "${BUNDLE_PATHS[@]}" | head -n 50
} > "$NOTES"

if [ "$DRY_RUN" = 1 ]; then
  log "$BUNDLE: DRY_RUN, no release. Notes:"; cat "$NOTES" >&2
elif gh release create "$TAG" "${ASSETS[@]}" \
    --repo "$REPO" --target "$SHA" --title "$TAG" --notes-file "$NOTES" --latest; then
  git tag "$TAG" "$SHA"
  log "$BUNDLE: released ${GITHUB_SERVER_URL:-https://github.com}/$REPO/releases/tag/$TAG"
else
  echo "::error::$BUNDLE: creating release $TAG failed" >&2; FAILED=1
fi
exit "$FAILED"
