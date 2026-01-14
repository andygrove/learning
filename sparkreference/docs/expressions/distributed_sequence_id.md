# DistributedSequenceID

## Overview
The `DistributedSequenceID` expression generates increasing 64-bit integers consecutive from 0. This expression is specifically designed for use with Pandas API on Spark and guarantees that generated IDs are consecutive integers starting from 0 across distributed partitions.

## Syntax
This expression is not directly available in SQL syntax as it's marked as `NonSQLExpression`. It's primarily used internally by the Pandas API on Spark.

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| None | - | This expression takes no arguments |

## Return Type
`LongType` - Returns 64-bit long integers.

## Supported Data Types
This expression does not accept input data as it's a leaf expression that generates values internally.

## Algorithm
The specific algorithm implementation is not visible in this source file as it extends `Unevaluable`, indicating the actual evaluation logic is handled elsewhere in the Spark execution engine:

- Generates consecutive 64-bit integers starting from 0
- Maintains ordering across distributed partitions
- Ensures no gaps in the sequence
- Coordinates sequence generation across multiple executors
- Returns non-nullable long values

## Partitioning Behavior
Based on its distributed nature and consecutive ID guarantee:

- Likely requires coordination across partitions to maintain consecutive ordering
- May impact partition-wise operations due to cross-partition dependencies
- The consecutive guarantee suggests potential performance implications in distributed environments

## Edge Cases

- **Null handling**: Returns non-nullable values (`nullable = false`)
- **Empty input**: As a leaf expression, it doesn't depend on input data
- **Overflow behavior**: Uses 64-bit longs, so overflow would occur after 2^63-1 values
- **Distributed coordination**: Must handle failures and ensure no duplicate IDs across executors

## Code Generation
This expression is marked as `Unevaluable`, which means:

- It does not support direct code generation (Tungsten)
- The actual evaluation is handled by specialized execution logic
- Falls back to interpreted mode through the Spark execution engine

## Examples
```sql
-- Not available in SQL as this is a NonSQLExpression
-- Used internally by Pandas API on Spark
```

```scala
// Internal usage example (not for direct user consumption)
// This expression is created internally by Pandas API operations
val seqId = DistributedSequenceID()
// Returns: Expression that generates consecutive IDs starting from 0
```

## See Also

- `MonotonicallyIncreasingID` - Similar expression that generates increasing but not necessarily consecutive IDs
- `RowNumber` window function - For generating row numbers within partitions
- Pandas API on Spark documentation for index operations