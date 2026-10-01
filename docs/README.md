# Documentation Index

This directory separates durable architecture and operating contracts from milestone-specific historical records.

## Canonical documentation

| Document | Purpose |
|---|---|
| [`Architecture.md`](Architecture.md) | Architecture and trust boundaries that remain valid across milestones |
| [`Validation.md`](Validation.md) | Common validation/evidence layers |
| [`Prerequisites.md`](Prerequisites.md) | Common host, Python, Git, and runtime prerequisites |
| [`oneshot-deployment.md`](oneshot-deployment.md) | Progressive one-shot deployment contract and current milestone mapping |
| [`Milestones.md`](Milestones.md) | M0–M21 evolution and current release state |
| [`Documentation-Audit-M21.1.md`](Documentation-Audit-M21.1.md) | Commit-by-commit documentation audit and refactor rationale |

## Current milestone

- [`M21-Embedded-Linux-Platform-Security-Validation.md`](M21-Embedded-Linux-Platform-Security-Validation.md)
- [`Prerequisites-M21.md`](Prerequisites-M21.md)
- [`Deployment-M21.md`](Deployment-M21.md)
- [`Validation-M21.md`](Validation-M21.md)

## Historical milestone records

Milestone-specific files such as `M8-*.md`, `Prerequisites-M8.md`, `Deployment-M8.md`, and `Validation-M8.md` describe the milestone that introduced that capability. They should be read as historical/feature-specific records, not as substitutes for the canonical current workflow.

When a historical document and a current canonical document differ on release status or operating procedure, prefer:

1. the source code and tests at the selected Git tag;
2. `README.md` / `instruction.md` for current orientation and execution;
3. canonical docs in this directory;
4. milestone-specific historical docs for feature detail.
