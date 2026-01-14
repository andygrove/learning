# RegrAvgX

## Overview
RegrAvgX is an aggregate function that computes the average of the independent variable (x-values) in linear regression analysis. It calculates the mean of the second argument (right expression) for all rows where both the dependent and independent variables are not null.

## Syntax
```sql
REGR_AVGX(y, x)
```

```scala
// DataFrame API usage
df.agg(expr("regr_avgx(y_column, x_column)"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| y | NumericType | The dependent variable (used only for null filtering) |
| x | NumericType | The independent variable whose average will be calculated |

## Return Type
Returns a numeric type corresponding to the average of the independent variable values, or null if no valid pairs exist.

## Supported Data Types

- Numeric types (IntegerType, LongType, FloatType, DoubleType, DecimalType)
- Both arguments must be numeric types due to `inputTypes: Seq(NumericType, NumericType)`

## Algorithm

- Filters out rows where either the left (y) or right (x) expression is null using `And(IsNotNull(left), IsNotNull(right))`
- For remaining valid pairs, extracts only the right (x) values using conditional logic
- Applies the `Average` aggregate function to compute the mean of the x-values
- Returns null if no valid pairs exist after filtering

## Partitioning Behavior
How this expression affects partitioning:

- Does not preserve partitioning as it's an aggregate function that reduces multiple rows to a single value
- Requires shuffle operation when used in distributed computing to collect all valid x-values for averaging

## Edge Cases

- Null handling: Rows where either y or x is null are completely excluded from the calculation
- Empty input: Returns null when no rows remain after null filtering
- All nulls: Returns null if all input rows contain at least one null value
- Single valid pair: Returns the x-value itself as the average

## Code Generation
This expression uses `RuntimeReplaceableAggregate`, which means it's replaced at runtime with a combination of `Average`, `If`, `And`, and `IsNotNull` expressions. Code generation support depends on the underlying replacement expressions, which typically support Tungsten code generation.

## Examples
```sql
-- Calculate average of x-values in linear regression
SELECT REGR_AVGX(sales, advertising_spend) FROM quarterly_data;

-- With grouping
SELECT region, REGR_AVGX(revenue, marketing_cost) 
FROM sales_data 
GROUP BY region;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.agg(expr("regr_avgx(dependent_var, independent_var)").alias("avg_x"))

// With grouping
df.groupBy("category")
  .agg(expr("regr_avgx(y_col, x_col)").alias("average_x_value"))
```

## See Also

- `RegrAvgY` - Average of dependent variable in linear regression
- `Average` - Simple average aggregate function  
- Other linear regression functions in the `regr_*` family
- `IsNotNull` - Null checking expression used internally