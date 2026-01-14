# UnionExec

## Overview
UnionExec is a physical operator that combines multiple input plans into a single output plan without removing duplicates, implementing SQL's `UNION ALL` semantics. It concatenates all rows from its children while ensuring schema compatibility by merging data types and nullability across all inputs.

## When Used
The query planner selects UnionExec when:
- Processing `UNION ALL` SQL operations
- Combining multiple subqueries or table scans
- Merging results from different branches of a query plan
- No duplicate elimination is required (unlike `UNION DISTINCT`)

## Input Requirements
- **Expected input partitioning**: Any partitioning scheme
- **Expected input ordering**: No specific ordering requirements
- **Number of children**: Multiple children (2 or more SparkPlan nodes)
- **Schema compatibility**: All children must have the same number of columns with compatible data types

## Output Properties
- **Output partitioning**: Preserves common partitioning if all children share the same partitioning scheme (when `spark.sql.execution.union.outputPartitioning` is enabled), otherwise defaults to `UnknownPartitioning`
- **Output ordering**: No guaranteed output ordering
- **Output schema**: Schema is derived by merging data types using `StructType.unionLikeMerge` and setting nullability to `true` if any child attribute is nullable

## Algorithm
- Transpose all children's output attributes to align columns by position
- Merge data types across corresponding columns using union-like type promotion rules
- Update nullability flags based on whether any child has nullable attributes for each position
- Choose execution strategy based on output partitioning compatibility
- For compatible partitioning, use `SQLPartitioningAwareUnionRDD` to preserve partition structure
- For incompatible partitioning, use standard Spark `union()` operation on child RDDs
- Filter out empty partitions when using partitioning-aware union

## Memory Usage
- **Spilling**: Does not spill to disk as it streams data without buffering
- **Memory requirements**: Minimal memory overhead, only maintains partition metadata
- **Buffering behavior**: No buffering - operates in streaming fashion, passing through rows from children sequentially

## Partitioning Behavior
- **Data distribution**: Concatenates partitions from all children without reshuffling
- **Shuffle requirements**: No shuffle required - purely concatenation operation
- **Partition count changes**: Total partitions equals sum of all children's partition counts (unless using partitioning-aware union with compatible schemes)

## Supported Join/Aggregation Types
Not applicable - UnionExec is a set operation, not a join or aggregation operator.

## Metrics
UnionExec does not define specific SQL metrics beyond the standard physical operator metrics:
- Number of output rows (inherited from SparkPlan)
- Execution time (inherited from SparkPlan)

## Code Generation
UnionExec does not support whole-stage code generation directly. Code generation support depends on its children operators. The union operation itself is implemented at the RDD level rather than through generated code.

## Configuration Options
- **`spark.sql.execution.union.outputPartitioning`**: Controls whether to preserve output partitioning when all children have compatible partitioning schemes
- Inherits general Spark SQL execution configurations that affect child operators

## Edge Cases
- **Null handling**: Automatically promotes nullability to `true` if any child attribute is nullable for the corresponding position
- **Empty partition handling**: Filters out RDDs with empty partitions when using partitioning-aware union to avoid unnecessary overhead
- **Data type compatibility**: Uses `StructType.unionLikeMerge` for automatic type promotion (e.g., int + long = long)
- **Attribute alignment**: Maps attributes by position, not by name

## Examples
```
== Physical Plan ==
Union
:- *(1) Project [id#1L, name#2]
:  +- *(1) Range (1, 100, step=1, splits=4)
+- *(2) Project [id#3L, name#4]
   +- *(2) Range (101, 200, step=1, splits=4)
```

## See Also
- **IntersectExec**: For set intersection operations
- **ExceptExec**: For set difference operations  
- **DeduplicateExec**: For removing duplicates after union operations
- **CoalesceExec**: For reducing partition count after union operations