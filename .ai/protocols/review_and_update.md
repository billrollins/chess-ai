Review recent code changes and update .ai/context/ to match.

## 1. Determine what changed

Read .ai/context/.last_update for the commit hash of the last context sync.
- If the file exists: run `git diff <hash>..HEAD --name-only` to get changed files.
- If the file doesn't exist: treat all source files as changed (full scan).

## 2. Map changed files to context docs

Use this mapping to decide which context_extended/ files need review:

  backend/app/game/       --> game_engine.md
  backend/app/api/        --> api_routes.md
  backend/app/players/    --> ai_players.md
  backend/app/storage/    --> storage.md
  backend/main.py         --> architecture.md
  frontend/src/           --> frontend.md
  scripts/, PlayChess.bat --> scripts_tooling.md
  Structural changes      --> architecture.md
  Key path changes        --> context_base.md

## 3. Review code in changed files

For each changed source file, review for:
1. Correctness — logic, edge cases, error handling
2. Consistency — naming, patterns, style
3. Security — input validation, injection risks
4. Performance — unnecessary work, leaks

Report any findings. Suggest fixes only where important.

## 4. Update context docs

Read the relevant context_extended/ files (from the mapping above) alongside the changed source code. Update any descriptions, paths, or behaviors that have drifted. Keep context concise — no code blocks unless essential.

If key paths, tech stack, or project overview changed, update context_base.md.

## 5. Record the sync point

Write the current HEAD commit hash to .ai/context/.last_update.

## 6. Note changes for changelog

If any meaningful work was done since the last CHANGELOG.md entry, add a bullet under [Unreleased] in CHANGELOG.md at the project root.
