# ProjectExec

## Overview
ProjectExec is a physical operator that implements column projection, evaluating a list of named expressions to produce a new set of output columns. It's essentially the physical implementation of SQL SELECT clauses that specify which columns to output and what expressions to compute.

## When Used
The query planner chooses ProjectExec when:
- SQL SELECT statements specify particular columns or expressions
- Column pruning optimization removes unnecessary columns
- Expression evaluation is needed (computed columns, functions, literals)
- The logical Project operator needs physical execution

## Input Requirements
- **Expected input partitioning**: Any (preserves input partitioning)
- **Expected input ordering**: Any (preserves input ordering) 
- **Number of children**: Unary (exactly one child operator)

## Output Properties
- **Output partitioning**: Same as child's output partitioning (implements `PartitioningPreservingUnaryExecNode`)
- **Output ordering**: Same as child's output ordering (implements `OrderPreservingUnaryExecNode`)
- **Output schema**: Derived from `projectList.map(_.toAttribute)` - each named expression contributes one output attribute

## Algorithm
- Binds project expressions to the child's output schema using `BindReferences.bindReference`
- Performs subexpression elimination when enabled (`conf.subexpressionEliminationEnabled`)
- Evaluates expressions using either partition evaluators (`conf.usePartitionEvaluator`) or per-partition iterators
- Uses `ProjectEvaluatorFactory` to create evaluators that apply expressions to input rows
- Optimizes by deferring evaluation of expressions used only once via `usedInputs` calculation
- Handles non-deterministic expressions specially by forcing their evaluation
- Generates efficient code through whole-stage code generation support

## Memory Usage
- **Spill behavior**: Does not spill to disk (stateless operator)
- **Memory requirements**: Minimal - only holds expression evaluation state
- **Buffering**: No buffering - processes rows one at a time in streaming fashion

## Partitioning Behavior
- **Data distribution**: Preserves existing data distribution unchanged
- **Shuffle requirements**: None - no data movement between partitions
- **Partition count**: Unchanged from input

## Supported Join/Aggregation Types
Not applicable - ProjectExec is a projection operator, not a join or aggregation operator.

## Metrics
ProjectExec does not expose specific SQL metrics in the provided implementation. Metrics are typically handled by parent operators or the overall query execution framework.

## Code Generation
Yes, ProjectExec fully supports whole-stage code generation by implementing `CodegenSupport`:
- Implements `doProduce()` to delegate to child operator
- Implements `doConsume()` to generate projection code
- Supports subexpression elimination in generated code
- Optimizes non-deterministic expression handling in codegen

## Configuration Options
- `spark.sql.codegen.subexpressionElimination.enabled`: Enables subexpression elimination optimization
- `spark.sql.execution.usePartitionEvaluator`: Uses partition evaluators instead of mapPartitionsWithIndexInternal

## Edge Cases
- **Null handling**: Expressions handle nulls according to their individual null semantics
- **Empty partition handling**: Processes empty partitions normally (no special handling needed)
- **Non-deterministic expressions**: Forces evaluation of non-deterministic expressions (like `rand()`) and includes them in `AttributeSet(nonDeterministicAttrs)`
- **Expression reuse**: Optimizes expressions used multiple times through subexpression elimination

## Examples
```
*(5) Project [id#0L, (id#0L * 2) AS doubled#3L]
+- *(4) Filter (id#0L > 100)
   +- *(4) Range (0, 1000000, step=1, splits=8)
```

In this example, ProjectExec evaluates two expressions: the `id` column directly and a computed `doubled` column using the expression `id * 2`.

## See Also
- **FilterExec**: Often used together for SELECT-WHERE combinations
- **GenerateExec**: For exploding/flattening operations  
- **UnaryExecNode**: Parent class for single-child operators
- **CodegenSupport**: Interface for whole-stage code generation