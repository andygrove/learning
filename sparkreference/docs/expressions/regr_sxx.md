# RegrSXX

## Overview
The `RegrSXX` expression computes the sum of squares of the independent variable in linear regression analysis. It is an aggregate function that calculates the sum of squared deviations of the X values from their mean, which is used as a building block for regression statistics.

## Syntax
```sql
REGR_SXX(y, x)
```

```scala
// DataFrame API usage
df.agg(expr("regr_sxx(y_column, x_column)"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| left (y) | DoubleType | The dependent variable (Y values) - used for null filtering |
| right (x) | DoubleType | The independent variable (X values) - the variable for which sum of squares is calculated |

## Return Type
`DoubleType` - Returns a double precision floating point number representing the sum of squares of the X values.

## Supported Data Types

- Numeric types that can be implicitly cast to `DoubleType`
- Both arguments must be convertible to double precision floating point numbers

## Algorithm

- Implements `RuntimeReplaceableAggregate`, delegating computation to `RegrReplacement`
- Filters out rows where either left (Y) or right (X) values are null
- Uses the right expression (X values) as input to the replacement aggregate
- Returns null if any input pair contains null values
- Calculates the sum of squared deviations using the replacement implementation

## Partitioning Behavior
As an aggregate function:

- Requires data shuffling for global aggregation across partitions
- Does not preserve existing partitioning schemes
- Partial aggregation may occur within partitions before final shuffle

## Edge Cases

- **Null handling**: Returns null if any row contains null values in either Y or X columns
- **Empty input**: Behavior depends on the underlying `RegrReplacement` implementation
- **Single value**: May return zero if only one non-null pair exists
- **Numeric precision**: Subject to double precision floating point limitations and potential precision loss

## Code Generation
This expression uses `RuntimeReplaceableAggregate`, which means:

- The actual computation is delegated to the replacement expression
- Code generation support depends on the underlying `RegrReplacement` implementation
- No direct Tungsten code generation in this class itself

## Examples
```sql
-- Calculate sum of squares for regression analysis
SELECT REGR_SXX(sales, advertising_spend) as sxx
FROM sales_data;

-- Use in combination with other regression functions
SELECT 
    REGR_SXX(y, x) as sum_squares_x,
    REGR_SXY(y, x) as sum_products,
    REGR_SYY(y, x) as sum_squares_y
FROM regression_table;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

val df = spark.table("sales_data")
val result = df.agg(
  expr("regr_sxx(sales, advertising_spend)").alias("sum_squares_x")
)

// Multiple regression statistics
val stats = df.agg(
  expr("regr_sxx(y, x)").alias("sxx"),
  expr("regr_sxy(y, x)").alias("sxy"),
  expr("regr_syy(y, x)").alias("syy")
)
```

## See Also

- `RegrSXY` - Sum of products of X and Y deviations
- `RegrSYY` - Sum of squares of Y deviations  
- `RegrSlope` - Slope of linear regression line
- `RegrIntercept` - Y-intercept of linear regression line
- Other regression aggregate functions in the `agg_funcs` group