# ChatGPT project context

This directory is a local mirror of the ChatGPT project “ポートフォリオ作成”.

- Treat every file under `sources/` as read-only reference material.
- Do not edit, rename, move, or delete synced project files.
- These files may be replaced the next time a task is created from this ChatGPT project.


## Project instructions

This project has no custom instructions.

## Codex project instructions

This repository is being used to turn the ChatGPT planning work for **MiniCloud -> AI Arena** into a Codex-ready development project.

Read `PROJECT.md` before making architectural decisions. It contains the current product and learning direction.

## Highest priority

The highest priority is educational value.

This project is not trying to minimize implementation effort by hiding every hard problem behind mature services. It is trying to expose core computer science ideas through a real system that has a reason to exist.

Prefer implementations that help the human understand:

- operating systems
- processes
- networking
- queues
- schedulers
- databases
- distributed workers
- sandboxing
- security
- machine learning
- statistics
- testing
- system design

Completing a feature is not enough. The user should come away understanding the important mechanism.

## Development principles

- Keep changes small enough to understand and review.
- Prefer explicit, readable implementations over clever abstraction.
- Match the existing style of the repository once code exists.
- Separate exploration, planning, implementation, testing, and review.
- Do not silently change public interfaces or file formats.
- Do not edit, rename, move, or delete files under `sources/`.
- Preserve user changes. Never revert work you did not make unless explicitly asked.
- When unsure whether to optimize for polish or learning, choose learning.

## Library and framework policy

Avoid excessive dependency on high-level libraries where they remove the lesson this project is meant to teach.

Good examples:

- Use PostgreSQL when the goal is to learn schema design, transactions, indexing, and application data modeling.
- Use a normal web framework when the lesson is API shape, scheduler behavior, or worker orchestration.
- Use a proven ML library once the learning target is training loops, datasets, evaluation, or experiments rather than writing tensor primitives.

Avoid, at least in early phases:

- replacing the scheduler with Kubernetes
- replacing the queue with a managed queue before building a simple local one
- replacing the process runner with a full PaaS framework
- hiding all networking behind a black-box reverse proxy before implementing a minimal routing path
- treating Docker as magic without explaining the process, namespace, cgroup, filesystem, and resource-limit concepts behind it
- turning the 2D game into a large game-engine project when the real goal is deterministic simulation and AI training

Mature tools are allowed after the underlying mechanism has been implemented or clearly explained.

## Implementation workflow

Before substantial implementation:

1. Inspect the current files and architecture.
2. Summarize the relevant existing behavior.
3. Identify the smallest useful next step.
4. State the plan when the change is non-trivial.
5. Implement only the scoped change.
6. Run relevant tests or explain why they cannot be run.
7. Review the diff for bugs, missing tests, race conditions, resource leaks, and confusing design.

For code touching MiniCloud, pay special attention to:

- job lifecycle states
- process cleanup
- cancellation
- stdout / stderr capture
- retries
- concurrency
- race conditions
- resource limits
- security boundaries
- failure reporting

For code touching AI Arena, pay special attention to:

- determinism
- fixed-tick simulation
- replay reproducibility
- state/action schema
- scoring correctness
- separation between simulation and rendering
- testability without a UI
- preserving data needed for training and replay

## Testing expectations

Add or update tests when behavior changes.

Minimum expected test areas:

- deterministic simulation gives identical results for identical input
- replay files reproduce the same result
- job state transitions are valid
- failed jobs preserve logs and exit information
- scheduler does not exceed configured concurrency
- reward and score calculations are stable
- serialization formats round-trip correctly

If tests are not yet set up, create the smallest useful test harness rather than skipping verification indefinitely.

## Review expectations

After implementing meaningful code, perform a self-review before finishing.

Look for:

- correctness bugs
- race conditions
- nondeterminism
- resource leaks
- missing cleanup
- unclear failure modes
- security problems
- overuse of dependencies
- places where the user would not understand the mechanism

When reviewing another Codex change, prioritize bugs and risks before style preferences.

## Explanation responsibility

When a change involves important CS concepts, explain them briefly in plain language.

Examples:

- what happens when a process is spawned
- why stdout and stderr need separate handling
- why queues prevent overload
- how a scheduler chooses workers
- why deterministic replay matters for AI training
- why reward design can create unintended behavior
- what resource limits protect against

Do not bury the user in theory. Tie the explanation to the code that was changed.

## Product direction guardrails

MiniCloud is the infrastructure foundation.

AI Arena is the AI/ML and game-facing layer.

The initial AI Arena direction is:

- deterministic 2D time attack
- simple visuals
- fixed tick simulation
- actions: left, right, jump, down, dash
- deep movement through timing, momentum, slopes, wall contact, jump duration, dash, and friction
- human demonstration first
- behavior cloning as a weak initial policy
- reinforcement learning after imitation
- population training for agent generations
- trajectory optimization over input sequences
- replay and scoring as first-class artifacts

Do not turn AI Arena into a generic chat game or LLM-judged battle. Outcomes should be decided by the game engine and numeric evaluation, not by an AI judge.

## Codex operating notes

- Use `rg` or `rg --files` for searching when available.
- Use `apply_patch` for manual file edits.
- Keep generated documentation concise enough to stay useful.
- Keep implementation steps incremental.
- Prefer code that can run locally before designing distributed versions.
- If a command cannot be run because dependencies or services are missing, say exactly what was attempted and what is needed next.
