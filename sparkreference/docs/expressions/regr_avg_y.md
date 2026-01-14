# RegrAvgY

## Overview
RegrAvgY is an aggregate function that computes the average of the dependent variable (y values) in linear regression analysis. It calculates the arithmetic mean of the first expression values where both expressions are non-null, effectively filtering out rows where either the dependent or independent variable is null.

## Syntax
```sql
REGR_AVGY(y, x)
```

```scala
// DataFrame API usage
df.agg(expr("regr_avgy(dependent_var, independent_var)"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| y | Numeric | The dependent variable (y values) for which to calculate the average |
| x | Numeric | The independent variable (x values) used for null filtering |

## Return Type
Returns a numeric data type corresponding to the input y expression's data type. Returns null if no valid pairs exist.

## Supported Data Types

- Byte, Short, Integer, Long
- Float, Double
- Decimal with any precision and scale
- Any numeric type that can be implicitly cast

## Algorithm

- Filters input rows to include only those where both x and y expressions are non-null
- Applies the Average aggregate function to the filtered y values
- Uses implicit casting to handle different numeric input types
- Returns null for the filtered y values when either input is null in a given row
- Implemented as a runtime replaceable aggregate that transforms into Average with conditional logic

## Partitioning Behavior
How this expression affects partitioning:

- Does not preserve partitioning as it's an aggregate function that reduces data
- May require shuffle operations to collect data for final aggregation depending on the execution plan
- Follows standard Spark aggregate partitioning behavior with partial and final aggregation phases

## Edge Cases

- **Null handling**: Rows where either x or y is null are excluded from the average calculation
- **Empty input**: Returns null when no valid (non-null) pairs exist
- **All nulls**: Returns null if all input pairs contain at least one null value
- **Mixed precision**: Automatically handles implicit casting between different numeric types
- **Single valid pair**: Returns the y value when only one valid pair exists

## Code Generation
This expression supports Spark's Tungsten code generation through its replacement expression (Average with conditional filtering). The code generation is inherited from the underlying Average aggregate function implementation.

## Examples
```sql
-- Calculate average of sales amounts for valid price-sales pairs
SELECT REGR_AVGY(sales_amount, price) as avg_sales
FROM sales_data;

-- Result: 1500.0 (average of non-null sales_amount where price is also non-null)
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

val df = spark.createDataFrame(Seq(
  (100.0, 10.0),
  (200.0, 20.0),
  (null, 30.0),
  (400.0, null)
)).toDF("sales", "price")

df.agg(expr("regr_avgy(sales, price)")).show()
// Result: 150.0 (average of 100.0 and 200.0, nulls excluded)
```

## See Also

- `regr_avgx` - Average of independent variable in linear regression
- `avg` / `mean` - Standard average aggregate function
- `regr_slope` - Slope of linear regression line
- `regr_intercept` - Y-intercept of linear regression line