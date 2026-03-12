# Plan: Establish .ai as AI Coder Context System

## Summary

Build the `.ai/` folder into a reliable, single-source-of-truth system that any AI coding agent can read to orient itself, understand the codebase, pick up planned work, and follow consistent protocols.

## Steps

| # | Step | Status | Notes |
|---|------|--------|-------|
| 1 | Consolidate metadata into single `context_base.md` | done | Merged .ai/README.md, context_extended_toc.md, plans/README.md into one entry point |
| 2 | Delete placeholder plans and redundant files | done | Removed plan_a/b/c, redundant READMEs |
| 3 | Audit `context_extended/` files for accuracy | on deck | Compare each file against current codebase; fix stale info |
| 4 | Refine protocols | done | Merged review+update, added version_bump + start_session, moved commit to bat script |
| 5 | End-to-end validation | on deck | Start a fresh AI chat, point it at `context_base.md`, confirm it can orient and work effectively |

## Handoff

**Completed:** Steps 1, 2, 4
- Consolidated context_base.md as single entry point
- Deleted placeholder plans and redundant files
- Overhauled protocols: merged review+update, added version_bump + start_session, moved commit to scripts/commit.bat
- Moved VERSION and CHANGELOG.md to project root

**Next batch:** Steps 3, 5
- Audit each `context_extended/` file against current source code
- Test the system end-to-end with a fresh AI session
