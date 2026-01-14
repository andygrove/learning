# ReplicateRows

## Overview
ReplicateRows is an internal Spark Catalyst generator expression that replicates a row N times, where N is specified as the first argument. This expression is solely used by the Spark optimizer to rewrite EXCEPT ALL and INTERSECT ALL queries and is not directly accessible through SQL or DataFrame APIs.

## Syntax
This is an internal expression not exposed through public APIs. It would be constructed programmatically as:
```scala
ReplicateRows(Seq(numRowsExpression, column1Expression, column2Expression, ...))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| children.head | Expression evaluating to Long | The number of times to replicate the row (multiplier) |
| children.tail | Seq[Expression] | The column expressions to be replicated in each output row |

## Return Type
Returns an iterator of InternalRow objects, where each row contains the evaluated column values. The output schema is a StructType with fields named "col0", "col1", etc., with data types matching the input expressions.

## Supported Data Types
Supports any data type for the column expressions since it simply evaluates and replicates the values without type-specific operations. The multiplier must evaluate to a Long value.

## Algorithm

- Evaluates the first child expression to get the number of replications (numRows) as a Long
- Evaluates all remaining child expressions once to get the column values
- Creates a range from 0 to numRows and maps each iteration to create a new InternalRow
- Each output row contains the same evaluated column values in an array structure
- Returns an iterator over all the replicated rows

## Partitioning Behavior
As a generator expression that produces multiple output rows from a single input row:

- Does not preserve partitioning since it changes the number of rows
- May require shuffling depending on how it's used in the query plan
- The output rows will be in the same partition as the input row

## Edge Cases

- If numRows is 0 or negative, returns an empty iterator (no rows generated)
- Null values in column expressions are preserved and replicated as-is
- If the multiplier expression evaluates to null, it will cause a ClassCastException when cast to Long
- Large multiplier values could cause memory issues since all rows are generated in memory

## Code Generation
This expression extends CodegenFallback, which means it does not support Tungsten code generation and always falls back to interpreted evaluation mode.

## Examples
```sql
-- Not directly accessible via SQL
-- Used internally for queries like:
SELECT col1, col2 FROM table1
EXCEPT ALL
SELECT col1, col2 FROM table2
```

```scala
// Internal usage only - not available through public DataFrame API
// Would be constructed during query optimization phase
val replicator = ReplicateRows(Seq(
  Literal(3L),           // replicate 3 times
  col("name"),           // first column
  col("age")             // second column
))
```

## See Also

- Generator - parent trait for expressions that produce multiple output rows
- CodegenFallback - trait for expressions that don't support code generation
- EXCEPT ALL and INTERSECT ALL query operators that utilize this expression internally