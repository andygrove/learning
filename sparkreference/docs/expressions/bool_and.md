# BoolAnd

## Overview

The `BoolAnd` expression is an aggregate function that returns true if all input boolean values are true, and false otherwise. It implements logical AND aggregation across multiple rows, internally using the `Min` function as its underlying implementation since false (0) is smaller than true (1) in boolean logic.

## Syntax

```sql
bool_and(column)
```

```scala
// DataFrame API
df.agg(expr("bool_and(column)"))
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The boolean expression or column to aggregate |

## Return Type

`BooleanType` - Returns a single boolean value representing the logical AND of all input values.

## Supported Data Types

- `BooleanType` - Only boolean input types are supported due to `ImplicitCastInputTypes` with `inputTypes` set to `Seq(BooleanType)`

## Algorithm

- Internally delegates to the `Min` aggregate function through the `replacement` field
- Leverages the fact that in boolean logic, false (0) < true (1)
- The minimum of all boolean values will be false if any value is false
- Returns true only when all input values are true (minimum would be true)
- Follows standard aggregate function evaluation patterns through Spark Catalyst

## Partitioning Behavior

- Does not preserve partitioning as it is an aggregate function
- Requires shuffle operation to collect all values for final aggregation
- Partial aggregation can be performed within each partition before shuffling
- Final result is computed after combining partial results from all partitions

## Edge Cases

- **Null handling**: Follows standard SQL null semantics - nulls are ignored in the aggregation
- **Empty input**: Returns null for empty input sets (standard SQL aggregate behavior)
- **All nulls**: Returns null when all input values are null
- **Mixed null/boolean**: Ignores null values and aggregates only the non-null boolean values

## Code Generation

This expression supports Tungsten code generation through its replacement with the `Min` function. The `Min` aggregate function has code generation support, so `BoolAnd` inherits this capability through the `RuntimeReplaceableAggregate` trait.

## Examples

```sql
-- Basic usage
SELECT bool_and(col) FROM VALUES (true), (false), (true) AS tab(col);
-- Result: false

-- All true values
SELECT bool_and(col) FROM VALUES (true), (true), (true) AS tab(col);
-- Result: true

-- With nulls
SELECT bool_and(col) FROM VALUES (true), (null), (true) AS tab(col);
-- Result: true (nulls ignored)
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

val df = Seq((true), (false), (true)).toDF("col")
df.agg(expr("bool_and(col)")).show()

// Result: false
```

## See Also

- `BoolOr` - Logical OR aggregate function
- `Min` - The underlying implementation used by BoolAnd
- `Every` - SQL standard equivalent function name
- Aggregate functions in general