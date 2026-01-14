# WholeStageCodegenExec

## Overview
WholeStageCodegenExec compiles a subtree of plans that support codegen together into a single Java function, eliminating virtual function calls and improving CPU efficiency. It acts as a code generation framework that combines multiple physical operators into one generated class that processes data in a pipelined fashion.

## When Used
The query planner chooses this operator when:
- `spark.sql.codegen.wholeStage` is enabled (default: true)
- A subtree of operators all implement `CodegenSupport` and return `supportCodegen = true`
- No expressions contain `CodegenFallback` requirements
- Schema doesn't exceed `spark.sql.codegen.maxFields` limit
- The `CollapseCodegenStages` rule identifies a chain of codegen-compatible operators

## Input Requirements
- **Expected input partitioning**: Inherits from child operator's output partitioning
- **Expected input ordering**: Inherits from child operator's output ordering  
- **Number of children**: Unary operator (exactly one child)

## Output Properties
- **Output partitioning**: Same as child's output partitioning
- **Output ordering**: Same as child's output ordering
- **Output schema**: Identical to child's output schema (pass-through)

## Algorithm
- Generate Java source code by calling `child.produce()` which recursively generates code for the entire subtree
- Compile the generated code into a `BufferedRowIterator` subclass with class name based on `codegenStageId`
- Create an evaluator factory that instantiates the compiled code with runtime references
- Execute by mapping over input RDDs (supports up to 2 input RDDs) using the generated iterator
- Each generated iterator processes rows in a tight loop, calling `processNext()` and `append()` for results
- Handle fallback to interpreted execution if code generation or compilation fails
- Track code generation time and compilation statistics for monitoring

## Memory Usage
- **Spill behavior**: Does not spill to disk itself (inherits child's spill behavior)
- **Memory requirements**: Minimal - only buffers output rows via `BufferedRowIterator.append()`
- **Buffering**: Uses `BufferedRowIterator` to buffer result rows, but actual memory usage depends on child operators

## Partitioning Behavior
- **Data distribution**: Preserves child's partitioning exactly
- **Shuffle requirements**: No shuffling - purely a computational optimization
- **Partition count**: Unchanged from input

## Supported Join/Aggregation Types
Supports any join/aggregation types that the underlying child operators support, including:
- **Joins**: BroadcastHashJoin, ShuffledHashJoin, SortMergeJoin, BroadcastNestedLoopJoin
- **Aggregations**: HashAggregate, SortAggregate
- All other codegen-compatible operators in the subtree

## Metrics
- **pipelineTime**: Total time spent executing the generated pipeline code (in milliseconds)
- Inherits all metrics from child operators
- Global code generation time tracking via `WholeStageCodegenExec.codeGenTime`

## Code Generation
This operator IS the whole-stage code generation implementation. It:
- Generates Java source code for entire operator subtrees
- Compiles code at runtime using Janino compiler
- Falls back to interpreted execution if compilation fails or bytecode size exceeds `spark.sql.codegen.hugeMethodLimit`
- Supports broadcasting large generated code when size exceeds threshold

## Configuration Options
- `spark.sql.codegen.wholeStage` - Enable/disable whole-stage codegen
- `spark.sql.codegen.maxFields` - Maximum fields in schema for codegen
- `spark.sql.codegen.hugeMethodLimit` - Bytecode size limit before disabling codegen
- `spark.sql.codegen.fallback` - Allow fallback to interpreted execution on compilation failure
- `spark.sql.codegen.useIdInClassName` - Include stage ID in generated class names
- `spark.sql.codegen.splitConsumeFuncByOperator` - Split consume functions to avoid long methods

## Edge Cases
- **Compilation failure**: Automatically falls back to child.execute() if code generation or compilation fails
- **Large bytecode**: Disables codegen and uses interpreted execution when compiled code exceeds huge method limit
- **Complex schemas**: Automatically disabled when schema has too many nested fields
- **Expressions with CodegenFallback**: Prevents whole-stage codegen for the subtree

## Examples
```
== Physical Plan ==
*(1) Project [id#0L, (id#0L * 2) AS doubled#3L]
+- *(1) Filter (id#0L > 100)
   +- *(1) Range (0, 1000, step=1, splits=8)

// The *(1) indicates WholeStageCodegenExec with codegenStageId=1
// wrapping Project -> Filter -> Range in a single generated function
```

## See Also
- `InputAdapter` - Bridges non-codegen operators into codegen subtrees
- `CodegenSupport` - Trait implemented by codegen-compatible operators
- `CollapseCodegenStages` - Rule that inserts WholeStageCodegenExec operators