# RegrCount

## Overview
`RegrCount` is an aggregate function that counts the number of non-null pairs of values in linear regression analysis. It is implemented as a runtime replaceable aggregate that delegates to the standard `Count` function with both left and right expressions as arguments.

## Syntax
```sql
REGR_COUNT(y, x)
```

```scala
// DataFrame API usage would use the standard count with both columns
df.agg(count(col("y"), col("x")))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| left (y) | NumericType | The dependent variable expression |
| right (x) | NumericType | The independent variable expression |

## Return Type
Returns `LongType` (since it delegates to `Count` function which returns the count as a long integer).

## Supported Data Types

- All numeric data types (ByteType, ShortType, IntegerType, LongType, FloatType, DoubleType, DecimalType)
- Input types are subject to implicit casting to numeric types

## Algorithm

- Delegates execution to `Count(Seq(left, right))` through runtime replacement
- Counts only pairs where both left and right expressions are non-null  
- Leverages the existing Count aggregate implementation for actual computation
- Performs implicit type casting to ensure both inputs are numeric types
- Returns the total count of valid (non-null) value pairs

## Partitioning Behavior
As an aggregate function:

- Requires shuffle operation to collect data for final aggregation
- Does not preserve input partitioning due to aggregation requirements
- Can benefit from partial aggregation in each partition before shuffling

## Edge Cases

- **Null handling**: Pairs where either left or right value is null are excluded from the count
- **Empty input**: Returns 0 for empty datasets or when all pairs contain at least one null value
- **Type coercion**: Non-numeric inputs are subject to implicit casting rules, may result in null values if casting fails
- **Mixed types**: Different numeric types between left and right arguments are handled through implicit casting

## Code Generation
This expression uses runtime replacement rather than direct code generation. The underlying `Count` function supports Tungsten code generation, so the actual execution benefits from generated code performance optimizations.

## Examples
```sql
-- Count non-null pairs for regression analysis
SELECT REGR_COUNT(sales, advertising_spend) 
FROM marketing_data;

-- Use in combination with other regression functions
SELECT 
  REGR_COUNT(y, x) as sample_size,
  REGR_SLOPE(y, x) as slope,
  REGR_INTERCEPT(y, x) as intercept
FROM regression_table;
```

```scala
// DataFrame API equivalent using count with multiple columns
import org.apache.spark.sql.functions._

df.agg(count(col("sales"), col("advertising_spend")))

// In regression analysis context
df.agg(
  count(col("y"), col("x")).alias("sample_size"),
  // other regression functions would go here
)
```

## See Also

- `Count` - The underlying aggregate function used for implementation
- Other regression functions: `RegrSlope`, `RegrIntercept`, `RegrR2`
- `AggregateFunction` - Base class for aggregate expressions
- `RuntimeReplaceableAggregate` - Pattern for functions that delegate to other implementations