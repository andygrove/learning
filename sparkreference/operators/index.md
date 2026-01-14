# Spark Physical Operators Reference

This section documents Apache Spark SQL physical operators - the execution units that process data.

## What are Physical Operators?

Physical operators (also called SparkPlans) are the nodes in the physical query plan that actually execute data processing. Each operator:

- Takes input from child operators (or data sources)
- Applies transformations or aggregations
- Produces output for parent operators
- Reports execution metrics

## Operator Categories

### Joins
- [BroadcastHashJoinExec](broadcast_hash_join_exec.md) - Hash join with broadcast

### Aggregation
- [ObjectHashAggregateExec](object_hash_aggregate_exec.md) - Object-based hash aggregation
- [MergingSessionsExec](merging_sessions_exec.md) - Session window merging
- [UpdatingSessionsExec](updating_sessions_exec.md) - Session window updates

### Basic Operations
- [ProjectExec](project_exec.md) - Column projection
- [SortExec](sort_exec.md) - Data sorting
- [GenerateExec](generate_exec.md) - Explode/flatten arrays
- [ExpandExec](expand_exec.md) - GROUPING SETS expansion

### Limits
- [TakeOrderedAndProjectExec](take_ordered_and_project_exec.md) - Top-N with projection

### Code Generation
- [WholeStageCodegenExec](whole_stage_codegen_exec.md) - Whole-stage codegen wrapper

---

*More operators are documented as they are generated. Run `python scripts/generate_spark_reference.py --type operators` to generate additional pages.*
