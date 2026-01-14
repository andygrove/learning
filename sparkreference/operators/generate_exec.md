# GenerateExec

## Overview
GenerateExec applies a Generator expression to a stream of input rows, combining the output of each generator evaluation into a new stream of rows. This operation is similar to a `flatMap` in functional programming, with the additional capability to join input rows with their generated output.

## When Used
The query planner chooses GenerateExec when:
- SQL queries contain table-generating functions like `explode()`, `posexplode()`, `stack()`, or `json_tuple()`
- LATERAL VIEW operations are used to unnest arrays or maps
- User-defined table functions (UDTFs) are invoked
- The logical plan contains a `Generate` node that needs physical execution

## Input Requirements
- **Expected input partitioning**: Any partitioning scheme (inherits child's partitioning)
- **Expected input ordering**: No specific ordering requirements
- **Number of children**: Unary operator (exactly one child)

## Output Properties
- **Output partitioning**: Inherits the child's output partitioning unchanged
- **Output ordering**: No guaranteed output ordering
- **Output schema derivation**: Concatenation of `requiredChildOutput` and `generatorOutput` attributes, where the generator output schema is determined during analysis phase

## Algorithm
- Bind the generator expression to the child's output attributes for evaluation
- Initialize any nondeterministic components of the generator with partition index
- For each input row, evaluate the bound generator to produce zero or more output rows
- When `outer=true`, emit at least one row per input (using null values if generator produces empty results)
- Join input row attributes (pruned to required columns) with generator output using JoinedRow
- After processing all input rows, call `generator.terminate()` to handle any final output
- Convert all resulting rows to unsafe row format and update output metrics

## Memory Usage
- **Disk spilling**: No explicit spilling mechanism implemented
- **Memory requirements**: Minimal buffering - processes one input row at a time
- **Buffering behavior**: Uses LazyIterator for deferred evaluation of generator termination results

## Partitioning Behavior
- **Data distribution**: Maintains the same partitioning as input (no repartitioning)
- **Shuffle requirements**: None - operates within existing partitions
- **Partition count changes**: No change in partition count, but individual partitions may grow or shrink based on generator output cardinality

## Supported Join/Aggregation Types
Not applicable - this is a generation operator, not a join or aggregation operator.

## Metrics
- **numOutputRows**: Tracks the total number of rows produced by the generator across all partitions

## Code Generation
Supports whole-stage code generation when `generator.supportCodegen` returns true and the generator does not implement a `terminate()` method. Provides specialized code generation for:
- CollectionGenerator expressions (arrays, maps with inline structs)
- General IterableOnce-returning generators
- Proper null handling and outer join semantics in generated code

## Configuration Options
No specific Spark configuration parameters directly control GenerateExec behavior. Performance may be affected by general memory and code generation settings:
- `spark.sql.codegen.wholeStage` - enables/disables whole-stage code generation
- `spark.sql.adaptive.*` - adaptive query execution settings may affect upstream partitioning

## Edge Cases
- **Null handling**: When generator input is null, produces empty output (or single null row if `outer=true`)
- **Empty partition handling**: Empty partitions still call generator initialization and termination
- **Outer semantics**: When `outer=true` and generator produces no output, emits a row with null values for generator columns
- **Schema projection**: Automatically handles cases where child output differs from required output through projection

## Examples
```
*(5) Generate explode(array_col#10), false, [col#15]
+- *(4) Project [array_col#10]
   +- *(4) Filter isnotnull(array_col#10)
      +- *(4) FileScan parquet [array_col#10]
```

For a LATERAL VIEW query:
```sql
SELECT id, col FROM table LATERAL VIEW explode(array_col) t AS col
```

## See Also
- **ProjectExec**: Often used upstream to prepare generator inputs
- **FilterExec**: May be applied downstream to filter generated results
- **CollectionGenerator**: Base class for array/map exploding generators
- **Generator**: Base expression interface implemented by table functions