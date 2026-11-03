#!/usr/bin/env bash
# Release each skill that changed: bash .github/scripts/release_skills.sh [skill ...]
# A skill is a folder under skills/. With no arguments every skill is checked.
# Versions and whether to release come from scripts/versions.py plan: a skill's version is the
# newest entry of the version notes in its README.md and README.zh-CN.md (vX.Y, the same in both),
# and its tags are "<skill>-vX.Y.Z". When skills/<skill>/ changed since the last release: a higher
# X.Y releases vX.Y.0; an unchanged X.Y with only README changes releases vX.Y.(Z+1); SKILL.md or
# prompt.md changed without a higher X.Y fails without releasing. The last release is the latest
# by commit order among the old date tags "<skill>-vYYYY.MM.DD[.N]" and the new tags; after a date
# tag, or with none, the release is vX.Y.0. Each release has <tag>.zip (scripts/build_skill.py:
# <skill>/SKILL.md only) and the commits that touched the folder since the last release as notes;
# these releases are not marked latest.
# Then, on a full run (no arguments), the whole kit by the same rules, versioned from the version
# notes of the root READMEs and watching skills/, README.md, README.zh-CN.md and LICENSE: it
# releases prompt-kit-vX.Y.Z.zip (git archive of those paths under prompt-kit/) together with every
# skill's upload zip as <skill>.zip, marked latest.
# Environment: DRY_RUN=1 builds and prints the plan without calling gh; FORCE=1 releases unchanged
# skills too (as a README-only change); OUT_DIR sets the build folder. A failing skill does not
# stop the others; the script exits non-zero at the end.
set -euo pipefail
log(){ echo "[release] $*" >&2; }

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"
SHA="$(git rev-parse HEAD)"
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
log "commit=$SHA skills=${SKILLS[*]} DRY_RUN=$DRY_RUN FORCE=$FORCE out=$OUT_DIR"

FAILED=0
PLAN_ARGS=(plan --head "$SHA")
[ "$FORCE" = 1 ] && PLAN_ARGS+=(--force)
[ "$FULL_RUN" = 1 ] && PLAN_ARGS+=(--kit)
PLAN="$(python3 scripts/versions.py "${PLAN_ARGS[@]}" "${SKILLS[@]}")"
log "plan (name, action, new tag, last tag, reason):"
echo "$PLAN" >&2
KIT_LINE=""

while IFS=$'\t' read -r skill action TAG LAST msg <&3; do
  [ -n "$skill" ] || continue
  if [ "$skill" = prompt-kit ]; then KIT_LINE="$action"$'\t'"$TAG"$'\t'"$LAST"$'\t'"$msg"; continue; fi
  [ "$TAG" = - ] && TAG=""
  [ "$LAST" = - ] && LAST=""
  case "$action" in
    skip) log "$skill: $msg, skipped"; continue ;;
    error) echo "::error::$msg" >&2; FAILED=1; continue ;;
  esac
  if [ -n "$LAST" ]; then RANGE="$LAST..$SHA"; else RANGE="$SHA"; fi
  VER="${TAG#"$skill"-v}"
  ZIP=$(python3 scripts/build_skill.py "$OUT_DIR" "$skill" --version "$VER" --log-level WARNING)
  log "$skill: last=${LAST:-none} new=$TAG ($msg) asset=$ZIP ($(unzip -Z1 "$ZIP" | tr '\n' ' '))"

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
  git tag "$TAG" "$SHA"   # recorded locally for the rest of this run
  log "$skill: released ${GITHUB_SERVER_URL:-https://github.com}/$REPO/releases/tag/$TAG"
done 3<<< "$PLAN"

# Whole kit: only on a full run, so a hand-picked list of skills never releases it
BUNDLE=prompt-kit
BUNDLE_PATHS=(skills README.md README.zh-CN.md LICENSE)
if [ "$FULL_RUN" != 1 ]; then
  log "$BUNDLE: skills given, skipped"
  exit "$FAILED"
fi
IFS=$'\t' read -r action TAG LAST msg <<< "$KIT_LINE"
[ "$TAG" = - ] && TAG=""
[ "$LAST" = - ] && LAST=""
case "$action" in
  skip) log "$BUNDLE: $msg, skipped"; exit "$FAILED" ;;
  error) echo "::error::$msg" >&2; exit 1 ;;
esac
if [ -n "$LAST" ]; then RANGE="$LAST..$SHA"; else RANGE="$SHA"; fi
VER="${TAG#"$BUNDLE"-v}"
ZIP="$OUT_DIR/$TAG.zip"
git archive --format=zip --prefix="$BUNDLE/" -o "$ZIP" "$SHA" "${BUNDLE_PATHS[@]}"
log "$BUNDLE: last=${LAST:-none} new=$TAG ($msg) asset=$ZIP ($(unzip -Z1 "$ZIP" | wc -l) entries)"
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
