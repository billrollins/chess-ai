# Changelog

## [Unreleased]

- Consolidated .ai metadata into single context_base.md entry point
- Restructured version/changelog to project root
- Replaced commit protocol with scripts/commit.bat
- Merged review_code + update_context into single review_and_update protocol
- Added version_bump, start_session protocols
- Git-hash-based change tracking via .ai/context/.last_update

## [0.1.0] - 2026-03-12

### Added

- Chess platform with 2-player hot-seat, 1vAI, 2AI modes
- Custom AI players: RandomAI, GreedyMaterialAI
- Game storage as PGN files + SQLite
- Replay viewer for saved games
- .ai context system for AI-assisted development
