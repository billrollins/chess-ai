Evaluate recent changes and bump the project version.

## 1. Read current state

- Read VERSION at the project root for the current version (e.g. 0.1.0).
- Read CHANGELOG.md — focus on the [Unreleased] section.

## 2. Determine bump level

Based on the [Unreleased] entries:
- **patch** (0.1.x) — bug fixes, minor tweaks, context/doc updates
- **minor** (0.x.0) — new features, new AI players, new UI components
- **major** (x.0.0) — breaking changes, major architecture shifts

If [Unreleased] is empty or trivial, no bump is needed — stop here.

## 3. Update CHANGELOG.md

Move all [Unreleased] entries under a new version heading:

  ## [X.Y.Z] - YYYY-MM-DD
  (moved entries here, organized under Added/Changed/Fixed/Removed as appropriate)

Leave [Unreleased] empty for the next cycle.

## 4. Update VERSION

Write the new version string to the VERSION file at the project root.

## 5. Prepare commit

Write a commit message to scripts/commit_message.txt, e.g.:
  Bump version to X.Y.Z
