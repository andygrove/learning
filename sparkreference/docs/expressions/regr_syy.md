# RegrSYY

## Overview
The `RegrSYY` expression computes the sum of squares of the dependent variable (y) in linear regression analysis. It is an aggregate function that calculates the total variation in the y-values, which is a key component in regression statistics and is used to determine how much the dependent variable varies from its mean.

## Syntax
```sql
REGR_SYY(y, x)
```

```scala
// DataFrame API
df.agg(expr("regr_syy(y_column, x_column)"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| left (y) | Double | The dependent variable (y-values) in the regression |
| right (x) | Double | The independent variable (x-values) in the regression |

## Return Type
`DoubleType` - Returns a double precision floating-point number representing the sum of squares of the y-values.

## Supported Data Types

- Input types: `DoubleType` for both arguments
- Implicit casting is supported through `ImplicitCastInputTypes` trait
- Numeric types that can be cast to Double are automatically converted

## Algorithm

- Collects all (x, y) pairs from the input data
- Filters out any pairs where either x or y is null
- Calculates the mean of all y-values
- Computes the sum of squared differences: Σ(yi - ȳ)²
- Returns the total sum of squares for the dependent variable

## Partitioning Behavior
As an aggregate function:

- Does not preserve partitioning - requires data shuffling across partitions
- Requires a shuffle stage to collect all data for final aggregation
- Partial aggregation may be performed within partitions before final computation

## Edge Cases

- **Null handling**: If either x or y is null for a data point, that entire pair is excluded from the calculation
- **Empty input**: Returns null when no valid (non-null) pairs are available
- **Single value**: With only one data point, returns 0.0 (no variation)
- **All nulls**: Returns null if all input pairs contain at least one null value
- **Overflow behavior**: May overflow to infinity with extremely large values or datasets

## Code Generation
This expression uses `RuntimeReplaceableAggregate`, which means:

- It is replaced with equivalent expressions during query planning
- The replacement expression may support Tungsten code generation
- Falls back to the `RegrReplacement` implementation with null-handling logic

## Examples
```sql
-- Calculate sum of squares for sales vs advertising spend
SELECT REGR_SYY(sales_amount, advertising_spend) as syy
FROM quarterly_results;

-- Use in combination with other regression functions
SELECT 
  REGR_SYY(sales, marketing) as sum_squares_y,
  REGR_SXX(sales, marketing) as sum_squares_x,
  REGR_COUNT(sales, marketing) as point_count
FROM campaign_data;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.agg(expr("regr_syy(sales, advertising)").alias("syy"))

// Combined with other aggregations
df.agg(
  expr("regr_syy(y_col, x_col)").alias("sum_squares_y"),
  expr("regr_sxx(y_col, x_col)").alias("sum_squares_x")
)
```

## See Also

- `RegrSXX` - Sum of squares of independent variable
- `RegrSXY` - Sum of products of dependent and independent variables  
- `RegrCount` - Number of non-null pairs in regression
- `RegrR2` - Coefficient of determination
- `RegrSlope` - Slope of linear regression line