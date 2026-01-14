# SortOrder

## Overview
The `SortOrder` expression defines ordering specifications for sorting operations in Apache Spark SQL. It encapsulates a child expression along with sort direction (ascending/descending) and null ordering behavior (nulls first/last), and is used primarily by sort-based operators to determine how data should be ordered.

## Syntax
```sql
-- SQL syntax
ORDER BY expression [ASC|DESC] [NULLS FIRST|NULLS LAST]

-- Examples
ORDER BY col1 ASC NULLS FIRST
ORDER BY col2 DESC NULLS LAST
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
df.orderBy(asc("col1"), desc("col2"))
df.sort(col("col1").asc_nulls_first, col("col2").desc_nulls_last)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The expression to sort by |
| direction | SortDirection | Sort direction: `Ascending` or `Descending` |
| nullOrdering | NullOrdering | Null ordering: `NullsFirst` or `NullsLast` |
| sameOrderExpressions | Seq[Expression] | Set of expressions with equivalent sort order (from equivalence relations) |

## Return Type
`SortOrder` is an unevaluable expression that does not return data directly. It serves as metadata for sorting operations. The `SortPrefix` helper expression returns `LongType` for prefix-based sorting optimization.

## Supported Data Types
All orderable data types are supported:
- **Numeric types**: `BooleanType`, `IntegralType`, `FloatType`, `DoubleType`, `DecimalType`
- **Temporal types**: `DateType`, `TimestampType`, `TimestampNTZType`, `TimeType`, `AnsiIntervalType`  
- **String types**: `StringType`, `BinaryType`
- **Complex types**: Arrays, structs (with orderable elements)

## Algorithm
- **Type validation**: Ensures the child expression has an orderable data type using `TypeUtils.checkForOrderingExpr`
- **Default null ordering**: Automatically assigns `NullsFirst` for ascending sorts and `NullsLast` for descending sorts when not explicitly specified
- **Semantic equivalence**: Uses `sameOrderExpressions` to track expressions that produce equivalent ordering (e.g., from join keys)
- **Satisfaction checking**: The `satisfies()` method determines if one `SortOrder` can fulfill the requirements of another
- **Prefix generation**: `SortPrefix` generates 64-bit prefixes for efficient sorting using radix sort techniques

## Partitioning Behavior
- **Preserves partitioning**: `SortOrder` itself doesn't change partitioning
- **May require shuffle**: Sort operations using `SortOrder` may trigger shuffles if data needs global ordering
- **Range partitioning**: Can be used with range partitioning to maintain sort order across partitions

## Edge Cases
- **Null handling**: Nulls are ordered according to the `nullOrdering` specification (`NullsFirst` or `NullsLast`)
- **Empty input**: No special handling needed - empty datasets remain empty after sorting
- **Non-orderable types**: Type checking prevents creation of `SortOrder` for non-orderable types like `MapType`
- **Decimal overflow**: For `DecimalType`, if precision adjustment fails during prefix generation, uses `Long.MinValue`/`Long.MaxValue` as boundary values
- **NaN handling**: For floating-point types, NaN values are handled by the `DoublePrefixComparator`

## Code Generation
- **SortOrder**: Marked as `Unevaluable` - does not generate code for evaluation
- **SortPrefix**: Supports full Tungsten code generation with optimized prefix computation for each data type
- **Optimized paths**: Uses specialized prefix comparators (`StringPrefixComparator`, `BinaryPrefixComparator`, etc.) for efficient sorting

## Examples
```sql
-- Basic sorting
SELECT * FROM table ORDER BY age DESC NULLS LAST;

-- Multiple columns with different null ordering  
SELECT * FROM table ORDER BY 
  name ASC NULLS FIRST,
  salary DESC NULLS LAST;

-- Complex expressions
SELECT * FROM table ORDER BY 
  CASE WHEN status = 'active' THEN 1 ELSE 2 END ASC;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Basic sorting
df.orderBy(desc("age"))

// Multiple columns with custom null handling
df.sort(col("name").asc_nulls_first, col("salary").desc_nulls_last)

// Using expressions
df.orderBy(when(col("status") === "active", 1).otherwise(2).asc)

// Internal SortOrder creation (Catalyst internals)
val sortOrder = SortOrder(col("name").expr, Ascending, NullsFirst, Seq.empty)
```

## See Also
- **Sort**: Physical operator that uses `SortOrder` specifications
- **TakeOrderedAndProject**: Operator for `ORDER BY` with `LIMIT`
- **SortMergeJoin**: Uses `SortOrder` for join key ordering
- **Window**: Window functions that require ordering
- **RangePartitioning**: Partitioning strategy based on sort order