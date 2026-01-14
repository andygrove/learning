# PivotFirst

## Overview
`PivotFirst` is an imperative aggregate expression that pivots data by taking the first non-null value for each pivot column value and arranging them into an array. It transforms rows into columns by using one column's values to determine output positions and another column's values as the data to be rearranged.

## Syntax
```sql
-- Used internally by Spark's pivot operations
-- Not directly accessible via SQL syntax
```

```scala
// DataFrame API usage through pivot operations
df.groupBy("groupCol").pivot("pivotCol", pivotValues).agg(first("valueCol"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| pivotColumn | Expression | Column that determines which output position to put valueColumn in |
| valueColumn | Expression | The column that is being rearranged |
| pivotColumnValues | Seq[Any] | The list of pivotColumn values in the order of desired output. Values not listed here will be ignored |
| mutableAggBufferOffset | Int | Offset for mutable aggregation buffer (default: 0) |
| inputAggBufferOffset | Int | Offset for input aggregation buffer (default: 0) |

## Return Type
`ArrayType` containing elements of the same data type as the `valueColumn`.

## Supported Data Types

- **Pivot Column**: Any data type, with special handling for AtomicTypes vs complex types for indexing
- **Value Column**: All Spark data types including primitives, decimals, strings, and complex types
- **Special handling**: DecimalType requires specific precision handling during initialization

## Algorithm

- Creates an index mapping from pivot column values to array positions using HashMap for atomic types or TreeMap for complex types
- For each input row, evaluates the pivot column value and finds its corresponding index position
- Takes the first non-null value from the value column for each pivot position
- Ignores rows where the pivot column value is not in the specified pivot column values list
- Returns an array with values arranged according to the pivot column values order

## Partitioning Behavior
How this expression affects partitioning:

- Does not preserve partitioning as it's an aggregate operation
- Requires shuffle when used in groupBy operations with pivot
- Data must be co-located by grouping keys for proper aggregation

## Edge Cases

- **Null handling**: Null values in the value column are ignored; only first non-null value is taken
- **Missing pivot values**: Rows with pivot column values not in `pivotColumnValues` are ignored
- **Decimal precision**: DecimalType values require special initialization with `setDecimal` instead of `setNullAt`
- **Empty pivot values**: If no matching pivot values are found, positions remain null in the output array
- **Duplicate values**: Only the first encountered non-null value for each pivot position is retained

## Code Generation
This expression uses imperative aggregation and falls back to interpreted mode rather than supporting Tungsten code generation, as indicated by extending `ImperativeAggregate`.

## Examples
```sql
-- Internal usage through pivot operations
SELECT * FROM (
  SELECT year, course, earnings 
  FROM courseSales
) PIVOT (
  FIRST(earnings) FOR course IN ('dotNET', 'Java')
)
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

val df = spark.table("courseSales")
val pivoted = df
  .groupBy("year")
  .pivot("course", Seq("dotNET", "Java"))
  .agg(first("earnings"))

// Results in array format internally processed by PivotFirst
```

## See Also

- `ImperativeAggregate` - Base class for imperative aggregation expressions
- `first()` function - Related first value aggregation function
- `pivot()` operation - High-level DataFrame pivot operation that uses PivotFirst internally