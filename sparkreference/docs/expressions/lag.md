# Lag

## Overview

The `Lag` expression is a window function that accesses data from a previous row in the result set relative to the current row within a partition. It returns the value of the specified expression from a row that is a given number of rows before the current row, or a default value if no such row exists.

## Syntax

```sql
LAG(input_expression [, offset [, default_value [, ignore_nulls]]])
  OVER (PARTITION BY ... ORDER BY ...)
```

```scala
// DataFrame API
import org.apache.spark.sql.expressions.Window
import org.apache.spark.sql.functions.lag

df.withColumn("lagged_value", 
  lag($"column_name", offset, default_value)
    .over(Window.partitionBy($"partition_col").orderBy($"order_col")))
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| `input` | Expression | The expression whose value should be returned from the previous row |
| `inputOffset` | Expression | The number of rows to look back (must be a positive integer, defaults to 1) |
| `default` | Expression | The value to return when no previous row exists (defaults to NULL) |
| `ignoreNulls` | Boolean | Whether to skip NULL values when counting rows (defaults to false) |

## Return Type

Returns the same data type as the `input` expression. If no previous row exists and no default is specified, returns NULL.

## Supported Data Types

Supports all Spark SQL data types for the input expression, including:
- Numeric types (IntegerType, LongType, DoubleType, DecimalType, etc.)
- String types (StringType)
- Date and timestamp types (DateType, TimestampType)
- Boolean type
- Complex types (ArrayType, MapType, StructType)

## Algorithm

- Calculates the target row position by subtracting the offset from the current row's position within the partition
- The offset is internally converted to a negative value using `UnaryMinus` to represent looking backward
- If the target position is valid (>= 0), returns the value from that row
- If the target position is invalid (< 0), returns the default value
- When `ignoreNulls` is true, skips NULL values when counting rows for offset calculation

## Partitioning Behavior

- **Preserves partitioning**: Yes, operates within existing partitions
- **Requires shuffle**: No, but requires data to be ordered within partitions
- Extends `FrameLessOffsetWindowFunction`, meaning it doesn't use traditional window frames
- Requires an ORDER BY clause in the window specification to determine row ordering

## Edge Cases

- **Null handling**: When `ignoreNulls` is false (default), NULL values are included in row counting
- **Empty partition**: Returns the default value for all rows
- **Offset larger than partition size**: Returns the default value
- **Negative or zero offset**: Invalid usage, offset must be positive
- **First rows in partition**: When looking back beyond the first row, returns the default value
- **Foldable offset expressions**: The offset is pre-evaluated and converted to a literal if it's a constant expression

## Code Generation

This expression extends `FrameLessOffsetWindowFunction` which supports Tungsten code generation for efficient execution. The code generation optimizes the row access pattern for better performance compared to interpreted mode.

## Examples

```sql
-- Basic lag usage
SELECT 
  id, 
  value,
  LAG(value, 1) OVER (ORDER BY id) AS prev_value
FROM table_name;

-- Lag with default value
SELECT 
  id, 
  value,
  LAG(value, 2, 0) OVER (PARTITION BY category ORDER BY id) AS prev_value_2_rows
FROM table_name;

-- Lag with ignore nulls
SELECT 
  id, 
  value,
  LAG(value, 1, -1, true) OVER (ORDER BY id) AS prev_non_null_value
FROM table_name;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.expressions.Window
import org.apache.spark.sql.functions._

val windowSpec = Window.partitionBy($"category").orderBy($"timestamp")

df.withColumn("prev_value", lag($"value", 1).over(windowSpec))
  .withColumn("prev_value_with_default", lag($"value", 2, lit(0)).over(windowSpec))
```

## See Also

- `Lead` - Access data from subsequent rows
- `First` - Get the first value in a window frame  
- `Last` - Get the last value in a window frame
- `RowNumber` - Get the row number within a partition
- Other window functions in `org.apache.spark.sql.catalyst.expressions`