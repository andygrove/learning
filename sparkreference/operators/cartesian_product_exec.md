# CartesianProductExec

## Overview
The `CartesianProductExec` physical operator implements a cartesian product (cross join) between two datasets, producing all possible combinations of rows from the left and right inputs. This operator extends `BaseJoinExec` and performs an inner join with no join keys, optionally applying a filter condition to the resulting row combinations.

## When Used
The query planner selects this operator when:
- A cross join is explicitly specified in SQL (`CROSS JOIN`)
- An inner join is specified without any join conditions (`JOIN ... ON TRUE` or similar)
- The optimizer determines that a cartesian product followed by filtering is the most efficient execution strategy
- No equi-join conditions are available to use hash-based or sort-based join algorithms

## Input Requirements
- **Expected input partitioning**: Any partitioning scheme (no specific requirements)
- **Expected input ordering**: No ordering requirements
- **Number of children**: Binary operator (exactly two child plans - left and right)

## Output Properties
- **Output partitioning**: The output inherits partitioning characteristics from the cartesian product operation
- **Output ordering**: No guaranteed output ordering
- **Output schema derivation**: Concatenation of left and right schemas (`left.output ++ right.output`)

## Algorithm
- Execute both left and right child plans to obtain RDDs of `UnsafeRow` objects
- Create an `UnsafeCartesianRDD` that handles the cartesian product computation with configurable memory thresholds
- For each partition, generate an `UnsafeRowJoiner` to efficiently combine left and right rows
- If a join condition is specified, create a bound predicate and filter row pairs using a `JoinedRow` wrapper
- Apply the condition filter (if present) before producing output rows
- Join qualifying row pairs using the `UnsafeRowJoiner` and increment the output row counter
- Return the resulting RDD with proper metrics tracking

## Memory Usage
- **Spill to disk**: Yes, uses configurable thresholds for memory management
- **Memory requirements**: Controlled by three configuration parameters for buffer management
- **Buffering behavior**: Uses `UnsafeCartesianRDD` with in-memory threshold, spill threshold, and buffer size spill threshold to manage memory usage and avoid OOM errors

## Partitioning Behavior
- **Data distribution**: Creates M×N partition combinations where M and N are partition counts from left and right inputs
- **Shuffle requirements**: May require shuffle depending on input data distribution
- **Partition count changes**: Output partition count depends on the cartesian product partitioning strategy implemented in `UnsafeCartesianRDD`

## Supported Join/Aggregation Types
- **Join type**: Inner join only (`override def joinType: JoinType = Inner`)
- **Join keys**: None (`leftKeys` and `rightKeys` are both `Nil`)
- This operator specifically handles cross joins without equi-join conditions

## Metrics
- **numOutputRows**: SQL metric tracking the total number of output rows produced by the cartesian product operation

## Code Generation
Based on the source code structure, this operator does not implement whole-stage code generation. It uses interpreted execution with `UnsafeRowJoiner` for row combination and `Predicate.create()` for condition evaluation.

## Configuration Options
- `spark.sql.execution.cartesianProductExecBufferInMemoryThreshold`: Controls when to start spilling from memory
- `spark.sql.execution.cartesianProductExecBufferSpillThreshold`: Controls spill behavior threshold
- `spark.sql.execution.cartesianProductExecBufferSizeSpillThreshold`: Controls buffer size before spilling

## Edge Cases
- **Null handling**: Relies on the join condition evaluation and `UnsafeRowJoiner` for proper null handling
- **Empty partition handling**: If either input has empty partitions, those combinations will produce no output
- **Skew handling**: No built-in skew mitigation; performance can degrade significantly with uneven data distribution due to the multiplicative nature of cartesian products

## Examples
```
== Physical Plan ==
CartesianProduct [condition]
:- Scan ExistingRDD[id#1, name#2]
+- Scan ExistingRDD[dept_id#3, dept_name#4]
```

```sql
-- SQL queries that generate CartesianProductExec:
SELECT * FROM table1 CROSS JOIN table2
SELECT * FROM table1 JOIN table2 ON 1=1
```

## See Also
- `BroadcastNestedLoopJoinExec`: Alternative join operator for non-equi joins with broadcast optimization
- `SortMergeJoinExec`: Preferred for equi-joins with sortable keys  
- `BroadcastHashJoinExec`: Preferred for equi-joins when one side can be broadcast
- `UnsafeCartesianRDD`: The underlying RDD implementation used by this operator