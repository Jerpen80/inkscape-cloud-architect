REPO_URL="https://github.com/mipmip/inkscape-cloud-architect"

make_command "release" "Cut a release (args: major|minor|patch). Bumps version, updates CHANGELOG, tags, pushes, GitHub Release."
release(){
  set -euo pipefail

  local bump="${1:-}"
  case "$bump" in
    major|minor|patch) ;;
    *)
      echo "Usage: ./RUNME.sh release <major|minor|patch>"
      return 1
      ;;
  esac

  local changelog="$RUNME_DIR/CHANGELOG.md"
  if [[ ! -f "$changelog" ]]; then
    echo "Error: CHANGELOG.md not found"
    return 1
  fi

  # 2.2 Detect VCS (jj vs git)
  local vcs
  if jj root >/dev/null 2>&1; then
    vcs="jj"
  elif git rev-parse --git-dir >/dev/null 2>&1; then
    vcs="git"
  else
    echo "Error: not a git or jj repository"
    return 1
  fi
  echo "VCS: $vcs"

  # 2.3 Read current version from the latest git tag, bump per semver
  local cur
  cur=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")
  local cur_num="${cur#v}"
  local major minor patch
  IFS='.' read -r major minor patch <<< "$cur_num"
  major="${major:-0}"; minor="${minor:-0}"; patch="${patch:-0}"
  case "$bump" in
    major) major=$((major + 1)); minor=0; patch=0 ;;
    minor) minor=$((minor + 1)); patch=0 ;;
    patch) patch=$((patch + 1)) ;;
  esac
  local new_ver="${major}.${minor}.${patch}"
  local new_tag="v${new_ver}"
  echo "Current: $cur  ->  New: $new_tag"

  if git rev-parse "$new_tag" >/dev/null 2>&1; then
    echo "Error: tag $new_tag already exists"
    return 1
  fi

  # 2.4 Validate [Unreleased] has entries
  local unreleased
  unreleased=$(awk '
    /^## \[Unreleased\]/ { grab=1; next }
    /^## \[/ && grab { exit }
    /^\[Unreleased\]:/ { exit }
    grab { print }
  ' "$changelog")
  if ! echo "$unreleased" | grep -qE '\S'; then
    echo "Error: [Unreleased] section has no entries — nothing to release"
    return 1
  fi

  # 2.5 Replace [Unreleased] with the new version heading + fresh [Unreleased]
  local today
  today=$(date +%Y-%m-%d)
  local tmp
  tmp=$(mktemp)
  awk -v ver="$new_ver" -v date="$today" '
    /^## \[Unreleased\]/ && !done {
      print "## [Unreleased]"
      print ""
      print "## [" ver "] - " date
      done=1
      next
    }
    { print }
  ' "$changelog" > "$tmp"

  # 2.6 Update comparison links
  # [Unreleased] now compares from the new tag; add a link for the new version.
  awk -v ver="$new_ver" -v prev="${cur#v}" -v repo="$REPO_URL" '
    /^\[Unreleased\]:/ {
      print "[Unreleased]: " repo "/compare/v" ver "...HEAD"
      print "[" ver "]: " repo "/compare/v" prev "...v" ver
      next
    }
    { print }
  ' "$tmp" > "$changelog"
  rm -f "$tmp"

  echo "Updated CHANGELOG.md for $new_tag"

  # Extract the new version's section for the GitHub Release body
  local body
  body=$(awk -v ver="$new_ver" '
    $0 ~ "^## \\[" ver "\\]" { grab=1; next }
    /^## \[/ && grab { exit }
    /^\[/ && grab { exit }
    grab { print }
  ' "$changelog")

  # 2.7 Commit and tag (git and jj paths)
  local commit_sha
  if [[ "$vcs" == "jj" ]]; then
    jj commit -m "release: $new_tag"
    # the just-finalized release commit is now @- ; advance main onto it
    commit_sha=$(jj log -r @- --no-graph -T 'commit_id' 2>/dev/null | head -1)
    jj bookmark set main -r "$commit_sha"
    jj git export
    git tag -a "$new_tag" -m "Release $new_tag" "$commit_sha"
  else
    git add -A
    git commit -m "release: $new_tag"
    git tag -a "$new_tag" -m "Release $new_tag"
  fi
  echo "Committed and tagged $new_tag"

  # 2.8 Push commit and tags
  if [[ "$vcs" == "jj" ]]; then
    jj git push --bookmark main
    git push origin "$new_tag"
  else
    git push
    git push origin "$new_tag"
  fi
  echo "Pushed $new_tag"

  # 2.9 GitHub Release
  if command -v gh >/dev/null 2>&1; then
    printf '%s\n' "$body" | gh release create "$new_tag" \
      --title "$new_tag" --notes-file - 2>&1 || \
      echo "Warning: gh release create failed (tag is pushed; create the release manually)"
  else
    echo "Warning: gh not found — skipping GitHub Release (tag is pushed)"
  fi

  # 2.10 Summary
  echo ""
  echo "==================== RELEASE $new_tag ===================="
  echo "  version:  $cur -> $new_tag"
  echo "  vcs:      $vcs"
  echo "  changelog updated, committed, tagged, pushed"
  echo "  release:  $REPO_URL/releases/tag/$new_tag"
  echo "=========================================================="
}
