# Lead

## Overview
The `Lead` expression is a window function that returns the value of an expression at a specified number of rows after the current row within a result set partition. It provides access to data from subsequent rows without requiring a self-join, making it useful for comparing current values with future values in ordered datasets.

## Syntax
```sql
LEAD(input [, offset] [, default] [, ignoreNulls])
```

```scala
// DataFrame API
lead(input: Column, offset: Int = 1, defaultValue: Any = null, ignoreNulls: Boolean = false)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| `input` | Expression | The expression whose value should be returned from the lead row |
| `offset` | Expression | Number of rows to look ahead (default: 1). Must evaluate to a positive integer |
| `default` | Expression | Default value to return when the lead row is beyond the partition boundary (default: null) |
| `ignoreNulls` | Boolean | Whether to skip null values when counting offset rows (default: false) |

## Return Type
Returns the same data type as the `input` expression. If no lead row exists and no default is specified, returns null.

## Supported Data Types
Supports all Spark SQL data types for the `input` expression:

- Numeric types (IntegerType, LongType, FloatType, DoubleType, DecimalType)
- String types (StringType, VarcharType, CharType)
- Date and timestamp types (DateType, TimestampType)
- Binary types (BinaryType)
- Complex types (ArrayType, MapType, StructType)
- Boolean type

## Algorithm
- Extends `FrameLessOffsetWindowFunction` which operates without requiring frame boundaries
- Orders rows within each partition according to the window specification's ORDER BY clause
- For each current row, calculates the position of the target row by adding the offset value
- If `ignoreNulls` is true, skips null values when counting offset positions
- Returns the `input` expression value from the target row, or `default` if target row doesn't exist
- Uses efficient offset-based access rather than frame-based scanning for better performance

## Partitioning Behavior
- Preserves input partitioning structure
- Does not require a shuffle operation by itself
- Window operation may trigger shuffle if data needs to be redistributed for proper partitioning
- Operates independently within each partition boundary
- Requires data to be sorted within partitions based on ORDER BY specification

## Edge Cases
- **Null handling**: When `ignoreNulls=false` (default), null values in input are returned as-is and count toward offset calculation
- **Null skipping**: When `ignoreNulls=true`, null values in input column are skipped when determining lead rows
- **Boundary conditions**: When offset extends beyond partition end, returns the specified default value
- **Zero/negative offset**: Offset must be positive; zero or negative values may cause runtime errors
- **Empty partitions**: Returns default value for all rows in empty partitions
- **Missing ORDER BY**: Requires ORDER BY clause in window specification for deterministic results

## Code Generation
Supports Tungsten code generation for improved performance. As a `FrameLessOffsetWindowFunction`, it generates optimized code that avoids the overhead of frame-based window processing and directly accesses rows by calculated offsets.

## Examples
```sql
-- Basic lead usage - get next row's value
SELECT 
  id, 
  value,
  LEAD(value) OVER (ORDER BY id) as next_value
FROM table;

-- Lead with offset of 2 and default value
SELECT 
  id, 
  sales,
  LEAD(sales, 2, 0) OVER (PARTITION BY region ORDER BY date) as sales_2_periods_ahead
FROM sales_data;

-- Ignore nulls when looking ahead
SELECT 
  date,
  price,
  LEAD(price, 1, -1, true) OVER (ORDER BY date) as next_non_null_price
FROM stock_prices;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.expressions.Window
import org.apache.spark.sql.functions._

val windowSpec = Window.partitionBy("region").orderBy("date")

df.select(
  col("date"),
  col("sales"),
  lead("sales", 1).over(windowSpec).as("next_sales"),
  lead("sales", 2, lit(0)).over(windowSpec).as("sales_2_ahead")
)
```

## See Also
- `Lag` - Access previous row values
- `FirstValue` - Get first value in window frame
- `LastValue` - Get last value in window frame
- `RowNumber` - Assign sequential numbers to rows
- Other window functions in `org.apache.spark.sql.catalyst.expressions.windowExpressions`