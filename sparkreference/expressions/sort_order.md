# SortOrder

## Overview

SortOrder is a Catalyst expression that represents sort ordering specification for a single column or expression in Apache Spark SQL. It encapsulates the child expression to be sorted, sort direction (ascending/descending), null ordering behavior, and semantically equivalent expressions that have the same sort order.

## Syntax

```sql
-- SQL syntax (used in ORDER BY clauses)
ORDER BY column_expression [ASC|DESC] [NULLS FIRST|NULLS LAST]
```

```scala
// DataFrame API usage
df.sort(col("column_name").asc_nulls_first)
df.orderBy(col("column_name").desc_nulls_last)
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The expression to be sorted |
| direction | SortDirection | Sort direction (Ascending or Descending) |
| nullOrdering | NullOrdering | How null values should be ordered (NullsFirst or NullsLast) |
| sameOrderExpressions | Seq[Expression] | Set of expressions with equivalent sort order derived from operator equivalence relations |

## Return Type

SortOrder itself is `Unevaluable` and does not return a value. It inherits the data type from its child expression for type checking purposes only.

## Supported Data Types

Supports any data type that implements ordering semantics. The `checkInputDataTypes()` method validates that the child expression's data type supports ordering using `TypeUtils.checkForOrderingExpr()`.

## Algorithm

- SortOrder is a metadata expression that specifies sorting behavior rather than computing values
- The child expression provides the actual values to be compared
- Direction and null ordering control the comparison semantics
- Same order expressions enable optimization by recognizing equivalent sort keys
- Used primarily by sort-based operators like Sort, SortMergeJoin, and window functions

## Partitioning Behavior

SortOrder itself does not directly affect partitioning, but it influences operators that use it:
- **Sort operations**: May require shuffle if global ordering is needed
- **SortMergeJoin**: Can preserve partitioning when join keys align with partition keys
- **Window functions**: May require repartitioning based on partition keys vs sort keys

## Edge Cases

- **Null handling**: Behavior determined by `nullOrdering` parameter (NULLS FIRST or NULLS LAST)
- **Expression equivalence**: The `satisfies()` method checks semantic equivalence using `sameOrderExpressions`
- **Type validation**: Fails if child expression's data type doesn't support ordering
- **Empty sameOrderExpressions**: Valid case when no equivalent expressions exist

## Code Generation

SortOrder is marked as `Unevaluable`, so it does not participate in code generation directly. The actual sorting logic is handled by physical operators that consume SortOrder specifications and generate optimized comparison code.

## Examples

```sql
-- Basic ascending sort
SELECT * FROM table ORDER BY col1 ASC NULLS FIRST

-- Descending with nulls last
SELECT * FROM table ORDER BY col2 DESC NULLS LAST

-- Multiple sort orders
SELECT * FROM table ORDER BY col1 ASC, col2 DESC NULLS FIRST
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Ascending with nulls first
df.orderBy(col("col1").asc_nulls_first)

// Descending with nulls last  
df.orderBy(col("col2").desc_nulls_last)

// Multiple sort orders
df.orderBy(col("col1").asc, col("col2").desc_nulls_first)

// Using sort instead of orderBy
df.sort(col("col1").desc)
```

## See Also

- **SortDirection**: Enumeration for Ascending/Descending
- **NullOrdering**: Enumeration for NullsFirst/NullsLast  
- **Sort**: Physical operator that executes sorting
- **SortMergeJoin**: Join operator that uses sort ordering
- **WindowExec**: Window function operator that requires sorted input