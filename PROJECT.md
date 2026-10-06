# MiniCloud -> AI Arena Project

## Purpose

This project is primarily an educational portfolio project.

The goal is not to build a typical CRUD app or a thin AI wrapper. The goal is to learn a broad range of computer science fundamentals by building a system where each layer has a concrete reason to exist.

The project has two connected halves:

- **MiniCloud**: a small self-built cloud / PaaS for running jobs, services, workers, and eventually untrusted agent code.
- **AI Arena**: an AI training game where a player teaches and trains agents, then evaluates them in deterministic game environments with strict scores.

The long-term portfolio story is:

> I built a small cloud platform, then used it to run distributed AI training and evaluation for agents competing in deterministic 2D environments.

Even if the game never becomes a commercial product, the implementation should leave behind strong learning in OS, networking, distributed systems, databases, security, machine learning, statistics, testing, and agentic software development.

## Overall Structure

The intended architecture is:

```text
AI Arena
  - deterministic 2D environment
  - human demonstration recorder
  - agent training UI
  - replay viewer
  - ranking / score evaluation
  - model and trajectory artifacts

MiniCloud
  - API server
  - job queue
  - scheduler
  - workers
  - process runner
  - sandboxing
  - logs and metrics
  - artifact storage
  - deployment / service runner

Connection
  - AI Arena submits training and evaluation jobs
  - MiniCloud schedules those jobs across workers
  - workers run episodes, collect results, and store artifacts
  - AI Arena visualizes progress, replays, rankings, and agent evolution
```

The first priority is learning. Build small, visible mechanisms first. Replace them with mature tools only after the underlying problem has been understood.

## MiniCloud

MiniCloud is a small Heroku / Render / Railway-like platform, built as a learning system.

It should eventually support:

- registering code or tasks
- running commands as managed jobs
- starting HTTP services
- issuing routes or local URLs
- collecting logs and exit codes
- enforcing resource limits
- scheduling work across multiple workers
- storing artifacts such as models, logs, and replay data
- running AI Arena training and evaluation workloads

### Phase 1: Remote Job Runner

Start with the simplest useful system:

```text
POST /jobs
{
  "command": "python main.py"
}
```

The server creates a process, tracks it, and exposes status, logs, exit code, and failure information.

Learning targets:

- HTTP API design
- process creation
- stdin / stdout / stderr handling
- exit codes
- signals and cancellation
- async execution
- basic persistence
- job state transitions

### Phase 2: Queue, Scheduler, Worker

Do not start every submitted job immediately. Introduce:

```text
API -> Queue -> Scheduler -> Worker
```

Learning targets:

- producer / consumer design
- queues
- concurrency
- scheduling policy
- retries
- race conditions
- worker lifecycle
- backpressure
- resource-aware execution

The first queue and scheduler should be simple and self-built.

### Phase 3: HTTP Service Deployment

Allow a user program to run as a long-lived HTTP service on an internal port, then route traffic to it.

Learning targets:

- sockets
- ports
- TCP / HTTP
- reverse proxy basics
- health checks
- service lifecycle
- routing
- local DNS / hostname concepts
- eventually TLS concepts

### Phase 4: Container / Sandbox Understanding

Before relying entirely on Docker or Kubernetes, understand the underlying mechanisms.

Learning targets:

- process isolation
- filesystem isolation
- permissions
- Linux namespaces
- cgroups
- chroot-like isolation
- resource limits
- untrusted code risks

On Windows, development may use pragmatic substitutes, but the design notes should explain the Linux concepts behind the target behavior.

### Phase 5: Database Service

Add managed database concepts only after the job runner and service runner exist.

Learning targets:

- relational schema design
- transactions
- isolation
- indexes
- credentials
- connection pooling
- service provisioning

PostgreSQL is appropriate here. The goal is not to write a production database, but to understand how an application platform provisions and manages one.

### Phase 6: Multiple Workers / Distributed System

Move from one machine to multiple workers.

Learning targets:

- worker registration
- heartbeat
- failure detection
- job reassignment
- service discovery
- load balancing
- consistency trade-offs
- observability

This phase turns MiniCloud into a small orchestration system and creates the natural infrastructure for AI Arena training.

## AI Arena

AI Arena is not mainly a game-development project. The game should be visually simple and technically deterministic. The real depth should come from the learning system, evaluation loop, and infrastructure behind it.

The current preferred direction is:

> A deterministic 2D time-attack environment where the player first demonstrates movement, then trains agents that gradually become better than the human and eventually discover near-TAS-level routes.

### Core Experience

The loop should be:

```text
PLAY
  -> record human demonstration
TEACH
  -> choose useful runs, feedback, and training settings
TRAIN
  -> behavior cloning, reinforcement learning, population training
WATCH
  -> replay the agent's attempts and best runs
IMPROVE
  -> adjust data, rewards, exploration, compute allocation
COMPETE
  -> compare time, consistency, and generalization
```

The player begins as a teacher, becomes a coach, then becomes a designer of training environments and learning strategy.

## 2D Time-Attack Specification

The environment should be deterministic:

```text
same initial state + same input sequence = same result
```

Use a fixed tick rate, initially 60 Hz. Every tick records and applies a structured action.

### Actions

Keep inputs small but expressive:

- left
- right
- jump
- down
- dash

Depth should come from timing, duration, combinations, and physics rather than a large move list.

### Movement Physics

The movement system should make individual inputs matter.

Important mechanics:

- horizontal acceleration, max speed, and friction
- different ground and air acceleration
- jump height based on button hold duration
- short hops
- dash as directional acceleration
- slope interaction
- wall contact
- wall jump / wall kick emerging from state and input
- slide or crouch preserving momentum
- edge jumps
- dash cancel-like behavior through landing or collisions

The goal is not to make polished platformer content. The goal is to create a simple physics system with a large optimization space.

### Stage Elements

Use simple elements:

- floor
- wall
- slope
- pit
- moving platform
- bounce surface
- different friction surfaces
- checkpoint
- goal

Enemies and heavy content production are not necessary at first.

### Scoring

The main metric is clear time.

Optional supporting metrics:

- completion rate
- consistency across runs
- checkpoint splits
- input efficiency
- generalization across generated stages
- improvement over human personal best

Leaderboards may include:

- Human best
- Agent best
- Human -> AI improvement percentage
- hidden-test or generated-stage score

## Learning Pipeline

The learning system is the center of AI Arena.

Preferred progression:

```text
Human Demonstration
  -> state/action dataset
Behavior Cloning
  -> weak initial policy
Reinforcement Learning
  -> self-practice and improvement
Population Training
  -> many agents with varied parameters
Trajectory Optimization
  -> local search over the best input sequences
Record
  -> replay, compare, preserve artifacts
```

### Stage 1: Demonstration

The player records a few runs. The system turns them into `(state, action)` examples.

The first AI should be weak. It may move awkwardly, fail jumps, fall into pits, or copy the player's bad habits. This makes learning visible.

### Stage 2: Behavior Cloning

Train an initial policy from human demonstrations.

This should be treated as a starting point, not the final AI. A human-copying agent should eventually hit a ceiling.

### Stage 3: Reinforcement Learning

Let agents run many episodes and learn from reward signals.

Possible reward components:

- goal reached
- elapsed time penalty
- death penalty
- checkpoint reward
- progress reward
- novelty reward

The reward system should be inspectable because reward design is part of the player's strategy and part of the learning value.

### Stage 4: Player Control Over Training

The player should influence learning through understandable controls:

- which human runs become training data
- which failures are useful
- which best runs are preserved
- exploration level
- risk tolerance
- imitation vs self-exploration ratio
- training budget
- reward weights
- checkpoint focus
- compute allocation

Advanced mode can expose more direct parameters, but the default UI should remain game-like.

### Stage 5: Population Training

Train many agents in parallel with slightly different parameters.

Example:

```text
64 agents
  -> run many episodes
  -> keep top 8
  -> mutate settings
  -> create next generation
```

This creates an AI育成 game feel while introducing population-based training, evolution strategies, hyperparameters, variance, and selection pressure.

### Stage 6: Trajectory Optimization

After an agent finds a strong route, optimize the actual input sequence.

Example:

```text
jump at tick 183
  -> try 182 / 184
dash at tick 347
  -> try 346 / 348 / 349
```

This pushes the system toward AI-assisted TAS-like discovery and makes deterministic replay essential.

## MiniCloud Connection

AI Arena gives MiniCloud a concrete reason to exist.

Training and evaluation should be executed as MiniCloud jobs:

```text
AI Arena
  -> training request
MiniCloud API
  -> queue
Scheduler
  -> workers
Workers
  -> episodes / evaluation / trajectory search
Result Aggregator
  -> artifacts, metrics, rankings, replays
```

This connection naturally requires:

- distributed job execution
- queueing
- scheduling
- worker isolation
- resource limits
- artifact storage
- logs
- metrics
- failure handling
- eventually user-submitted agent code sandboxing

The platform should grow because AI Arena needs it, not because the project wants to imitate cloud tools for their own sake.

## Current Position

The current project direction is fixed enough to begin documentation and early implementation, but not fixed enough to overbuild.

Current decisions:

- Build MiniCloud as the CS foundation.
- Build AI Arena as the AI/ML and product-facing layer.
- Keep game visuals simple.
- Make the environment deterministic and replayable.
- Prefer a 2D time-attack / speedrun-like first environment.
- Keep input actions small: left, right, jump, down, dash.
- Make physics and timing deep enough that every tick can matter.
- Start learning from human demonstrations, but do not stop at imitation.
- Progress into RL, population training, and trajectory optimization.
- Use MiniCloud to run distributed training and evaluation jobs.
- Treat this as a learning-first portfolio project.

Immediate next steps:

1. Choose an initial language and repository structure.
2. Implement the smallest deterministic 2D simulation loop.
3. Define `State`, `Action`, `StepResult`, and replay format.
4. Record and replay human or scripted input sequences.
5. Add a simple baseline agent.
6. Add MiniCloud Phase 1 job runner separately.
7. Connect AI Arena training jobs to MiniCloud only after both sides have minimal working cores.

