# Plan: Establish .ai as AI Coder Context System

## Summary

Build the `.ai/` folder into a reliable, single-source-of-truth system that any AI coding agent can read to orient itself, understand the codebase, pick up planned work, and follow consistent protocols.

## Steps

| # | Step | Status | Notes |
|---|------|--------|-------|
| 1 | Consolidate metadata into single `context_base.md` | done | Merged .ai/README.md, context_extended_toc.md, plans/README.md into one entry point |
| 2 | Delete placeholder plans and redundant files | done | Removed plan_a/b/c, redundant READMEs |
| 3 | Audit `context_extended/` files for accuracy | on deck | Compare each file against current codebase; fix stale info |
| 4 | Refine protocols | backlog | Evaluate if commit/review/update_context are sufficient; add new protocols as needed |
| 5 | End-to-end validation | backlog | Start a fresh AI chat, point it at `context_base.md`, confirm it can orient and work effectively |

## Handoff

**Current batch:** Steps 1-2
- Consolidate and clean up — done
- Commit and push

**Next batch:** Step 3
- Read each `context_extended/` file alongside the actual source code
- Fix any stale descriptions, missing features, or incorrect paths

**Then:** Steps 4-5
- Evaluate protocol coverage
- Test the system with a fresh AI session
