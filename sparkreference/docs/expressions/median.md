# Median

## Overview
The `Median` expression calculates the median (50th percentile) value of a numeric column across all rows in a group. It is implemented as a runtime replaceable aggregate function that internally delegates to the `Percentile` expression with a fixed percentile value of 0.5.

## Syntax
```sql
SELECT MEDIAN(column_name) FROM table_name;
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The input expression/column to calculate the median for |

## Return Type
The return type matches the input data type of the child expression, following the same type rules as the underlying `Percentile` expression.

## Supported Data Types
Based on the implementation delegating to `Percentile`, the supported data types include:

- Numeric types (IntegerType, LongType, FloatType, DoubleType, DecimalType)
- Date and timestamp types
- Interval types (as shown in the example with INTERVAL MONTH)

## Algorithm
The median calculation follows these steps:

- Delegates internally to the `Percentile` expression with a fixed percentile value of 0.5
- Inherits the percentile calculation algorithm which sorts all values and finds the middle value
- For even number of elements, returns the average of the two middle values
- For odd number of elements, returns the exact middle value
- Maintains the same partitioning and aggregation behavior as the underlying percentile implementation

## Partitioning Behavior
As an aggregate function, the median expression has the following partitioning characteristics:

- Does not preserve input partitioning since it requires aggregation across partitions
- Requires a shuffle operation to collect all values for accurate median calculation
- Acts as a blocking operation that needs to see all data before producing results

## Edge Cases

- **Null handling**: Null values are ignored in the median calculation, following standard SQL aggregate behavior
- **Empty input**: Returns null when applied to an empty dataset or all-null values
- **Single value**: Returns that single value as the median
- **Duplicate values**: Properly handles datasets with duplicate values in the median calculation
- **Type precision**: Maintains input type precision for the result

## Code Generation
This expression supports Spark's Tungsten code generation through its underlying `Percentile` implementation, as it extends `RuntimeReplaceableAggregate` which allows the catalyst optimizer to replace it with the equivalent percentile expression during query planning.

## Examples
```sql
-- Calculate median of a numeric column
SELECT MEDIAN(salary) FROM employees;

-- Calculate median with interval data type
SELECT MEDIAN(col) FROM VALUES (INTERVAL '0' MONTH), (INTERVAL '10' MONTH) AS tab(col);
-- Result: 0-5

-- Calculate median grouped by department
SELECT department, MEDIAN(salary) FROM employees GROUP BY department;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Calculate median of a column
df.select(expr("median(salary)")).show()

// Calculate median with grouping
df.groupBy("department").agg(expr("median(salary)").alias("median_salary")).show()
```

## See Also

- `Percentile` - The underlying expression that implements the actual percentile calculation
- `ApproxPercentile` - For approximate percentile calculations with better performance
- `PercentRank` - For calculating percentile ranks instead of percentile values
- Other aggregate functions like `avg`, `min`, `max` for statistical operations