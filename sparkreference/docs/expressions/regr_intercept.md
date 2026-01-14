# RegrIntercept

## Overview
`RegrIntercept` is a declarative aggregate expression that computes the y-intercept of the least-squares linear regression line for non-null pairs of values. It calculates the intercept using covariance and variance computations internally, representing where the regression line crosses the y-axis when x equals zero.

## Syntax
```sql
regr_intercept(y, x)
```

```scala
// DataFrame API usage
df.agg(expr("regr_intercept(dependent_var, independent_var)"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| left (y) | DoubleType | The dependent variable (y-values) for regression calculation |
| right (x) | DoubleType | The independent variable (x-values) for regression calculation |

## Return Type
`DoubleType` - Returns a double precision floating point value representing the y-intercept, or null if calculation is not possible.

## Supported Data Types
Input data types are restricted to numeric types that can be implicitly cast to `DoubleType`:

- DoubleType (native)
- FloatType
- IntegerType  
- LongType
- ShortType
- ByteType
- DecimalType

## Algorithm
The expression evaluates the regression intercept using the following approach:

- Computes population covariance between y and x values using `CovPopulation`
- Calculates population variance of x values using `VariancePop`
- Applies the linear regression formula: intercept = y_avg - (covariance / x_variance) * x_avg
- Only processes non-null pairs where both x and y values are present
- Returns null if variance of x is zero (vertical line case)

## Partitioning Behavior
As a declarative aggregate function, `RegrIntercept` has specific partitioning requirements:

- Does not preserve partitioning as it aggregates data across partitions
- Requires shuffle operations for merging partial aggregates from different partitions
- Uses merge expressions to combine intermediate results during shuffle phase

## Edge Cases

- **Null handling**: Ignores pairs where either x or y is null, only processes complete pairs
- **Zero variance**: Returns null when x variance is zero (all x values are identical)
- **Empty input**: Returns null when no valid pairs are available for computation  
- **Insufficient data**: Returns null for datasets with less than one valid pair
- **Numerical precision**: Subject to floating-point precision limitations in covariance and variance calculations

## Code Generation
This expression extends `DeclarativeAggregate`, which supports Catalyst's code generation framework. The aggregate buffer operations and evaluation expressions are code-generated for optimal performance in Tungsten execution.

## Examples
```sql
-- Calculate regression intercept for sales vs advertising spend
SELECT regr_intercept(sales_amount, advertising_spend) as intercept
FROM sales_data;

-- Use in window functions for grouped analysis
SELECT region, regr_intercept(revenue, quarter) OVER (PARTITION BY region) 
FROM quarterly_revenue;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.agg(expr("regr_intercept(sales, advertising)").alias("intercept"))

// With grouping
df.groupBy("category")
  .agg(expr("regr_intercept(price, demand)").alias("price_intercept"))
```

## See Also

- `RegrSlope` - Computes the slope of linear regression line
- `CovPopulation` - Population covariance calculation used internally
- `VariancePop` - Population variance calculation used internally
- `RegrR2` - Coefficient of determination for regression analysis