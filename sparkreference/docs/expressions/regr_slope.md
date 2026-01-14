# RegrSlope

## Overview
`RegrSlope` is a declarative aggregate expression that calculates the slope of the least-squares fit linear equation for non-null pairs of dependent and independent variables. It computes the regression slope using the ratio of population covariance to population variance of the independent variable.

## Syntax
```sql
REGR_SLOPE(y, x)
```

```scala
// DataFrame API
df.agg(expr("regr_slope(y_column, x_column)"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| left (y) | DoubleType | The dependent variable (y-values) for regression calculation |
| right (x) | DoubleType | The independent variable (x-values) for regression calculation |

## Return Type
`DoubleType` - Returns a double precision floating point number representing the slope, or null if the variance of x is zero.

## Supported Data Types

- Input: Both arguments must be `DoubleType` (implicit casting is supported via `ImplicitCastInputTypes`)
- Output: `DoubleType`

## Algorithm

- Maintains internal state using `CovPopulation` for computing covariance between x and y variables
- Maintains internal state using `VariancePop` for computing population variance of x variable  
- Only processes pairs where both x and y values are non-null
- Calculates slope as the ratio: covariance(x,y) / variance(x)
- Returns null when variance of x equals zero (vertical line case)

## Partitioning Behavior
As a declarative aggregate function:

- Requires shuffle operations to collect data across partitions for final aggregation
- Does not preserve partitioning since it produces a single aggregate result
- Uses merge expressions to combine partial aggregates from different partitions

## Edge Cases

- **Null handling**: Ignores pairs where either x or y is null; maintains previous buffer state for such pairs
- **Zero variance**: Returns null when the variance of x is zero (all x values are identical)
- **Empty input**: Returns null when no valid (non-null) pairs are available
- **Numerical stability**: Inherits numerical behavior from underlying `CovPopulation` and `VariancePop` implementations

## Code Generation
This is a `DeclarativeAggregate` expression, which means it supports Catalyst's code generation (Tungsten) by expressing computation through other expressions rather than custom imperative code.

## Examples
```sql
-- Calculate regression slope for sales vs advertising spend
SELECT REGR_SLOPE(sales, advertising_spend) as slope
FROM sales_data;

-- Group by region to get slope per region  
SELECT region, REGR_SLOPE(sales, advertising_spend) as slope
FROM sales_data 
GROUP BY region;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.agg(expr("regr_slope(sales, advertising_spend)").alias("slope"))

// With grouping
df.groupBy("region")
  .agg(expr("regr_slope(sales, advertising_spend)").alias("slope"))
```

## See Also

- `CovPopulation` - Used internally for covariance calculation
- `VariancePop` - Used internally for variance calculation  
- Other regression functions: `regr_intercept`, `regr_r2`, `regr_count`
- Linear regression statistical functions