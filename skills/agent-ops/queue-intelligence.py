# skills/agent-ops/queue-intelligence.py
"""

PURPOSE:
Queue intelligence engine implementing §17.11 advanced orchestration:
dependency DAG construction and validation, complexity estimation,
automatic batch suggestions, and conflict detection. Does NOT edit the CSV —
produces reports for human review and decision-making.
Invoked by: scripts/queue-graph.sh (make queue:graph) and
scripts/queue-analyze.sh (make queue:analyze).

DEPENDS ON:
- csv (stdlib) — queue and archive parsing
- pathlib (stdlib) — file paths
- collections (stdlib) — defaultdict, deque for graph operations
- subprocess (stdlib) — git history queries for complexity
- argparse (stdlib) — CLI modes
- dataclasses — data classes for graph nodes and results
- re (stdlib) — pattern matching in summary text

DEPENDED ON BY:
- scripts/queue-graph.sh → make queue:graph
- scripts/queue-analyze.sh → make queue:analyze
- skills/agent-ops/queue-intelligence.md — references this as machinery

CLASSES:

  QueueNode:
    PURPOSE: Represents a queue item as a node in the dependency DAG.
    FIELDS:
      - id: str — queue item ID
      - category: str — work category
      - summary: str — elaborative summary
      - dependencies: list[str] — direct dependency IDs
      - batch: str — batch assignment (optional)
      - phase: str — phase within batch (optional)
      - notes: str — current notes
    NOTES: Immutable (frozen=True) to prevent accidental mutation during analysis.

  DependencyDAG:
    PURPOSE: Directed acyclic graph of queue item dependencies.
    FIELDS:
      - nodes: dict[str, QueueNode] — all items by ID
      - edges: dict[str, list[str]] — adjacency list (item -> [items it depends on])
      - done_ids: set[str] — IDs from queuearchive with status=done
    METHODS:
      - find_cycles() -> list[list[str]] — detect circular dependencies; returns cycles as path lists
      - topological_sort() -> list[str] — items in dependency-safe order (Kahn's algorithm)
      - find_ready_nodes() -> list[str] — IDs where all dependencies are in done_ids
      - get_blocked_reasons(item_id: str) -> list[str] — dependency IDs blocking this item
      - transitive_depth(item_id: str) -> int — longest path from root to item_id

  ComplexityEstimate:
    PURPOSE: Advisory complexity score for a single queue item.
    FIELDS:
      - item_id: str
      - score: Literal["S", "M", "L", "XL"] — simple size estimate
      - factors: list[str] — reasons for the score (for human transparency)
      - numeric: int — 1-10 numeric version for sorting

  BatchSuggestion:
    PURPOSE: Suggested grouping of items into a batch.
    FIELDS:
      - batch_label: str — suggested batch identifier
      - item_ids: list[str] — items in this suggested batch
      - rationale: str — why these items are grouped

  ConflictWarning:
    PURPOSE: Warning about potential merge conflicts between items.
    FIELDS:
      - item_a: str — first item ID
      - item_b: str — second item ID
      - overlap_hint: str — description of the likely overlap (e.g., "both mention auth/router.py")

FUNCTIONS:

  load_queue(queue_path: Path) -> dict[str, QueueNode]:
    PURPOSE: Load queue.csv into QueueNode dict keyed by ID.
    STEPS:
      1. csv.DictReader on queue_path
      2. For each row: parse dependencies column (comma-separated, strip whitespace, filter empty)
      3. Return dict[id, QueueNode]
    RETURNS: dict[str, QueueNode]
    RAISES: FileNotFoundError, ValueError on schema error

  load_done_ids(archive_path: Path) -> set[str]:
    PURPOSE: Return set of IDs with status=done from queuearchive.csv.
    STEPS:
      1. csv.DictReader on archive_path
      2. Collect IDs where status field == "done"
    RETURNS: set[str]

  build_dag(nodes: dict[str, QueueNode], done_ids: set[str]) -> DependencyDAG:
    PURPOSE: Construct DependencyDAG from loaded nodes.
    STEPS:
      1. Validate all dependency references point to known IDs or done_ids
      2. Build adjacency list
      3. Return DependencyDAG instance
    RAISES: ValueError if unknown dependency IDs found

  estimate_complexity(node: QueueNode, git_log: str | None = None) -> ComplexityEstimate:
    PURPOSE: Estimate complexity of a queue item.
    STEPS:
      1. Heuristics from summary: count mentions of modules/files (proxy for file impact)
      2. Category heuristics: infrastructure/security → higher than documentation
      3. Dependency depth from DAG (transitive_depth)
      4. If git_log provided: count recent changes to mentioned files
      5. Map to S/M/L/XL: S=1-2, M=3-4, L=5-6, XL=7-10
    RETURNS: ComplexityEstimate
    NOTES: Advisory only — does not affect queue ordering

  suggest_batches(nodes: dict[str, QueueNode]) -> list[BatchSuggestion]:
    PURPOSE: Group items into suggested batches based on §17.11.3.
    STEPS:
      1. Group items that mention the same module path in summary
      2. Group schema change + API endpoint pairs
      3. Group test + implementation pairs (same entity name)
      4. Group items with shared prerequisite dependencies
      5. Return BatchSuggestion list (humans confirm by editing CSV)
    RETURNS: list[BatchSuggestion]

  detect_conflicts(nodes: dict[str, QueueNode]) -> list[ConflictWarning]:
    PURPOSE: Flag pairs of items likely to touch the same files (§17.11.4).
    STEPS:
      1. Extract file hints from each item summary (mentions of module paths, file names)
      2. Compare all pairs of items for overlapping file mentions
      3. Items with 2+ overlapping hints → ConflictWarning
    RETURNS: list[ConflictWarning]

  render_graph(dag: DependencyDAG) -> str:
    PURPOSE: Render the dependency DAG as Mermaid flowchart syntax.
    STEPS:
      1. Emit "graph TD" header
      2. For each edge: emit "ID_A --> ID_B"
      3. For done items: emit special style class
      4. For ready items: emit highlight class
    RETURNS: Mermaid graph string

  render_analysis_report(
    dag: DependencyDAG,
    complexity: dict[str, ComplexityEstimate],
    batches: list[BatchSuggestion],
    conflicts: list[ConflictWarning]
  ) -> str:
    PURPOSE: Render the full analysis as a Markdown report.
    STEPS:
      1. Section 1: Ready items (no blocked dependencies)
      2. Section 2: Blocked items with reasons
      3. Section 3: Complexity estimates table
      4. Section 4: Suggested batches
      5. Section 5: Conflict warnings
    RETURNS: Markdown string

  main() -> None:
    PURPOSE: CLI entry point with --mode graph|analyze|validate.
    STEPS:
      1. Parse args: --mode, --queue-path, --archive-path, --format
      2. Load queue and archive
      3. Build DAG; check for cycles (exit 1 if found)
      4. Run requested analysis mode
      5. Print output

CONSTANTS:
  - CATEGORY_COMPLEXITY_WEIGHTS: dict[str, int] — base complexity by category
    e.g., {"infrastructure": 3, "security": 3, "documentation": 1, "core-api": 2}

DESIGN DECISIONS:
- Uses stdlib only (no networkx) for portability — implements Kahn's algorithm in-house
- Cycle detection uses DFS with visited/stack coloring
- Batch suggestions are advisory: humans edit CSV, system does not
- Conflict detection uses keyword matching (not AST) for speed and portability
- Complexity estimation is transparent: factors list explains the score
"""
